"""
Two-way sync between glossary CSVs and FHIR CodeSystem JSONs, plus a
proposed-changes staging workflow.

Each glossary has TWO CSVs:
  - <Name>.csv           = current glossary, the source of truth for the JSON
  - <Name>-proposed.csv  = staging area for new/changed terms awaiting review;
                           this file NEVER goes to the JSON directly

Workflow:
  1. Edit *-proposed.csv with new terms or proposed updates.
  2. `--preview` shows what merging proposed into current would change.
  3. `--accept` actually merges proposed into current, empties proposed,
     and regenerates the JSON.
  4. With no flag, current.csv -> JSON (no proposed involved).

Conflict policy: if a code in proposed already exists in current with
different fields, it is SKIPPED with a warning (current wins). Resolve
manually and re-run.

Usage:
  python generate_glossary.py                       # current.csv -> JSON, all glossaries
  python generate_glossary.py clinical              # current.csv -> JSON, one glossary
  python generate_glossary.py operational --preview # diff current vs current+proposed
  python generate_glossary.py operational --accept  # merge proposed -> current, regen JSON
  python generate_glossary.py --to-csv              # JSON -> current.csv, all glossaries
  python generate_glossary.py --list                # List available glossaries
"""

import argparse
import csv
import difflib
import json
import re
import shutil
from datetime import datetime
from pathlib import Path

# Glossary configurations
# Each glossary has: csv_file, output_file, id, url, name, title, description
GLOSSARIES = {
    "clinical": {
        "csv_file": "ClinicalGlossary.csv",
        "proposed_csv_file": "ClinicalGlossary-proposed.csv",
        "output_file": "_resources/glossary/CodeSystem-glossary.json",
        "id": "clinical-glossary",
        "url": "http://example.org/CodeSystem/BeSafeShareGlossary",
        "name": "ClinicalGlossary",
        "title": "BeSafeShare Clinical Glossary",
        "description": "Clinical terms and definitions used across Belgian CareSets for semantic interoperability of healthcare data elements."
    },
    "operational": {
        "csv_file": "OperationalGlossary.csv",
        "proposed_csv_file": "OperationalGlossary-proposed.csv",
        "output_file": "_resources/glossary/CodeSystem-operational-glossary.json",
        "id": "operational-glossary",
        "url": "http://example.org/CodeSystem/BeSafeShareOperationalGlossary",
        "name": "OperationalGlossary",
        "title": "BeSafeShare Operational Glossary",
        "description": "Operational terms and definitions used in the BeSafeShare ecosystem for project management and governance."
    }
}

CSV_FIELDNAMES = ["Term", "Status", "Synonym", "FR", "EN", "NL"]

# Read version from VERSION file
def get_version():
    version_file = Path(__file__).parent / "VERSION"
    if version_file.exists():
        return version_file.read_text().strip()
    return "0.1"

GLOSSARY_VERSION = get_version()

# Status definitions. Lifecycle: proposed -> accepted (or rejected); active is
# legacy/equivalent to accepted; rejected/removed terms stay in the CodeSystem
# until a future cycle that physically removes them (terms are append-only).
STATUS_DEFINITIONS = {
    "proposed": "The concept has been proposed and is pending review",
    "accepted": "The concept has been reviewed and accepted for use",
    "rejected": "The concept has been reviewed and rejected",
    "draft": "The concept is in draft status and pending review",
    "active": "The concept is active and in use"
}


def read_csv_rows(csv_path):
    """Read a glossary CSV into a list of row dicts (or [] if missing/empty)."""
    if not csv_path.exists():
        return []
    with open(csv_path, 'r', encoding='utf-8-sig', newline='') as f:
        return [row for row in csv.DictReader(f, delimiter=';')
                if row.get('Term', '').strip()]


def write_csv_rows(csv_path, rows):
    """Write a list of row dicts as a glossary CSV."""
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES, delimiter=';',
                                quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(rows)


def merge_proposed(current_rows, proposed_rows):
    """Merge proposed rows into current rows.

    Returns (merged_rows, added_codes, conflicts) where conflicts is a list of
    (code, current_row, proposed_row) tuples. Existing-code conflicts are
    SKIPPED - current wins. New codes are appended.
    """
    current_codes = {r['Term']: r for r in current_rows if r.get('Term')}
    added = []
    conflicts = []
    merged = list(current_rows)

    for row in proposed_rows:
        code = row.get('Term', '').strip()
        if not code:
            continue
        if code in current_codes:
            existing = current_codes[code]
            differs = any((existing.get(k, '') or '') != (row.get(k, '') or '')
                          for k in CSV_FIELDNAMES if k != 'Term')
            if differs:
                conflicts.append((code, existing, row))
            continue
        merged.append(row)
        added.append(code)

    return merged, added, conflicts


def parse_csv_concepts(csv_path):
    """Parse concepts from a glossary CSV file."""
    concepts = []
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')

        for row in reader:
            term = row.get('Term', '').strip()
            if not term:
                continue

            synonym = row.get('Synonym', '').strip()
            status = row.get('Status', '').strip()
            display = synonym if synonym else term

            concept = {
                "code": term,
                "display": display,
            }

            # Add status as a property if present
            if status:
                concept["property"] = [
                    {
                        "code": "status",
                        "valueCode": status
                    }
                ]

            # Add designations for each language
            designations = []
            for lang_code, col_name in [('en', 'EN'), ('fr', 'FR'), ('nl', 'NL')]:
                value = row.get(col_name, '').strip()
                if value:
                    designations.append({
                        "language": lang_code,
                        "value": value
                    })

            if designations:
                concept["designation"] = designations

            concepts.append(concept)

    return concepts


def build_codesystem(concepts, config, date_str=None):
    """Build a full FHIR CodeSystem dict from a list of concepts."""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    return {
        "resourceType": "CodeSystem",
        "id": config["id"],
        "url": config["url"],
        "version": GLOSSARY_VERSION,
        "name": config["name"],
        "title": config["title"],
        "status": "active",
        "date": date_str,
        "description": config["description"],
        "content": "complete",
        "property": [
            {
                "code": "status",
                "description": "The approval status of the concept",
                "type": "code"
            }
        ],
        "filter": [
            {
                "code": "status",
                "description": "Filter by approval status",
                "operator": ["="],
                "value": " | ".join(STATUS_DEFINITIONS.keys())
            }
        ],
        "count": len(concepts),
        "concept": concepts
    }


def csv_rows_to_concepts(rows):
    """Convert CSV row dicts into FHIR concept dicts (same shape as parse_csv_concepts)."""
    concepts = []
    for row in rows:
        term = (row.get('Term') or '').strip()
        if not term:
            continue
        synonym = (row.get('Synonym') or '').strip()
        status = (row.get('Status') or '').strip()
        concept = {
            "code": term,
            "display": synonym if synonym else term,
        }
        if status:
            concept["property"] = [{"code": "status", "valueCode": status}]
        designations = []
        for lang_code, col_name in [('en', 'EN'), ('fr', 'FR'), ('nl', 'NL')]:
            value = (row.get(col_name) or '').strip()
            if value:
                designations.append({"language": lang_code, "value": value})
        if designations:
            concept["designation"] = designations
        concepts.append(concept)
    return concepts


def generate_codesystem(glossary_key, config, script_dir, mode="full"):
    """Generate a CodeSystem from a glossary CSV file.

    mode: "full" replaces the entire CodeSystem, "incremental" only adds new codes.
    """
    csv_path = script_dir / config["csv_file"]
    output_path = script_dir / config["output_file"]

    if not csv_path.exists():
        print(f"Warning: CSV file not found: {csv_path}")
        return False

    # Snapshot the previous CodeSystem (for diff report) and back it up.
    previous_codesystem = None
    if output_path.exists():
        with open(output_path, 'r', encoding='utf-8') as f:
            previous_codesystem = json.load(f)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = output_path.with_suffix(f".{timestamp}.backup.json")
        shutil.copy(output_path, backup_path)
        print(f"  Backup created: {backup_path.name}")

    csv_concepts = parse_csv_concepts(csv_path)

    if mode == "incremental" and output_path.exists():
        # Load existing CodeSystem and merge
        with open(output_path, 'r', encoding='utf-8') as f:
            codesystem = json.load(f)

        existing_codes = {c["code"] for c in codesystem.get("concept", [])}
        new_concepts = [c for c in csv_concepts if c["code"] not in existing_codes]

        if not new_concepts:
            print(f"  No new concepts to add (all {len(csv_concepts)} CSV terms already present)")
            return True

        codesystem["concept"].extend(new_concepts)
        codesystem["count"] = len(codesystem["concept"])
        codesystem["date"] = datetime.now().strftime("%Y-%m-%d")

        print(f"  Incremental: added {len(new_concepts)} new concepts, skipped {len(csv_concepts) - len(new_concepts)} existing")
    else:
        codesystem = build_codesystem(csv_concepts, config)

    # Write output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(codesystem, f, indent=2, ensure_ascii=False)

    print(f"  Total concepts: {codesystem['count']}")
    print(f"  Output: {output_path}")

    # Emit a markdown diff report when there was a previous version.
    if previous_codesystem is not None:
        write_diff_report(glossary_key, config, script_dir,
                          previous_codesystem, codesystem)
    return True


def preview_proposed_changes(glossary_key, config, script_dir):
    """Show what merging the proposed CSV into the current CSV would change.

    Writes a `*-preview.md` diff report. Does not modify any file.
    """
    csv_path = script_dir / config["csv_file"]
    proposed_path = script_dir / config["proposed_csv_file"]

    if not csv_path.exists():
        print(f"  Warning: current CSV not found: {csv_path}")
        return False

    current_rows = read_csv_rows(csv_path)
    proposed_rows = read_csv_rows(proposed_path) if proposed_path.exists() else []

    if not proposed_rows:
        print(f"  No proposed updates ({proposed_path.name} is empty or missing).")
        return True

    merged_rows, added, conflicts = merge_proposed(current_rows, proposed_rows)

    if conflicts:
        print(f"  WARNING: {len(conflicts)} conflicting code(s) - shown in diff but skipped on --accept:")
        for code, _, _ in conflicts:
            print(f"    - {code}")
        print("  Resolve manually in the proposed CSV (rename or remove the row).")

    current_cs = build_codesystem(csv_rows_to_concepts(current_rows), config)
    merged_cs = build_codesystem(csv_rows_to_concepts(merged_rows), config)

    print(f"  Would add {len(added)} new term(s) to {config['csv_file']}.")
    write_diff_report(glossary_key, config, script_dir,
                      current_cs, merged_cs, preview=True, conflicts=conflicts)
    print("  (No files modified - re-run with --accept to apply.)")
    return True


def accept_proposed_changes(glossary_key, config, script_dir):
    """Merge the proposed CSV into the current CSV, clear proposed, regen JSON."""
    csv_path = script_dir / config["csv_file"]
    proposed_path = script_dir / config["proposed_csv_file"]

    if not csv_path.exists():
        print(f"  Warning: current CSV not found: {csv_path}")
        return False

    current_rows = read_csv_rows(csv_path)
    proposed_rows = read_csv_rows(proposed_path) if proposed_path.exists() else []

    if not proposed_rows:
        print(f"  No proposed updates ({proposed_path.name} is empty or missing). "
              "Nothing to accept.")
        return True

    merged_rows, added, conflicts = merge_proposed(current_rows, proposed_rows)
    conflict_codes = {code for code, _, _ in conflicts}

    if conflicts:
        print(f"  WARNING: {len(conflicts)} conflicting code(s) - skipped (current wins):")
        for code in conflict_codes:
            print(f"    - {code}")
        print("  Those rows remain in the proposed CSV - resolve and re-run.")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Back up + overwrite current CSV with merged rows.
    backup_current = csv_path.with_suffix(f".{timestamp}.backup.csv")
    shutil.copy(csv_path, backup_current)
    write_csv_rows(csv_path, merged_rows)
    print(f"  Current CSV updated: +{len(added)} term(s) "
          f"(backup: {backup_current.name})")

    # Back up + clear proposed CSV (keep conflicting rows so the user can fix).
    if proposed_path.exists():
        backup_proposed = proposed_path.with_suffix(f".{timestamp}.backup.csv")
        shutil.copy(proposed_path, backup_proposed)
        remaining = [r for r in proposed_rows
                     if (r.get('Term') or '').strip() in conflict_codes]
        write_csv_rows(proposed_path, remaining)
        if remaining:
            print(f"  Proposed CSV: kept {len(remaining)} unresolved conflict row(s) "
                  f"(backup: {backup_proposed.name})")
        else:
            print(f"  Proposed CSV cleared (backup: {backup_proposed.name})")

    # Regenerate JSON from the now-merged current CSV.
    print()
    print(f"  Regenerating JSON from updated {config['csv_file']}...")
    return generate_codesystem(glossary_key, config, script_dir)


FIELD_LABELS = [
    ("display", "Display"),
    ("status", "Status"),
    ("en", "EN"),
    ("fr", "FR"),
    ("nl", "NL"),
]


def concept_fields(concept):
    """Flatten a CodeSystem concept into a comparable dict of fields."""
    status = ""
    for prop in concept.get("property", []):
        if prop.get("code") == "status":
            status = prop.get("valueCode", "")
            break
    designations = {d.get("language"): d.get("value", "")
                    for d in concept.get("designation", [])}
    return {
        "code": concept.get("code", ""),
        "display": concept.get("display", ""),
        "status": status,
        "en": designations.get("en", ""),
        "fr": designations.get("fr", ""),
        "nl": designations.get("nl", ""),
    }


def compare_codesystems(old_cs, new_cs):
    """Return a dict with added/removed/modified concept lists."""
    old_index = {c["code"]: concept_fields(c) for c in old_cs.get("concept", [])}
    new_index = {c["code"]: concept_fields(c) for c in new_cs.get("concept", [])}

    added_codes = [c for c in new_index if c not in old_index]
    removed_codes = [c for c in old_index if c not in new_index]

    modified = []
    for code in new_index:
        if code not in old_index:
            continue
        old_fields = old_index[code]
        new_fields = new_index[code]
        changed = [(k, label, old_fields[k], new_fields[k])
                   for (k, label) in FIELD_LABELS
                   if old_fields[k] != new_fields[k]]
        if changed:
            modified.append((code, changed))

    return {
        "added": [new_index[c] for c in added_codes],
        "removed": [old_index[c] for c in removed_codes],
        "modified": modified,
        "total_old": len(old_index),
        "total_new": len(new_index),
    }


def render_field_value(value):
    """Format a single field value for markdown (strip newlines, mark empty)."""
    if value == "":
        return "_(empty)_"
    return value.replace("\r\n", " ").replace("\n", " ")


_TOKEN_RE = re.compile(r"(\s+)")


def word_level_diff(old, new):
    """Return inline markdown with <del>/<ins> tags showing word-level changes.

    Tokenises on whitespace (preserving the whitespace tokens) so the rendered
    output reads naturally - only altered words are wrapped in del/ins.
    """
    old = old or ""
    new = new or ""
    if old == new:
        return new
    old_tokens = _TOKEN_RE.split(old)
    new_tokens = _TOKEN_RE.split(new)
    matcher = difflib.SequenceMatcher(a=old_tokens, b=new_tokens, autojunk=False)
    out = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        old_part = "".join(old_tokens[i1:i2])
        new_part = "".join(new_tokens[j1:j2])
        if tag == "equal":
            out.append(new_part)
        elif tag == "delete":
            out.append(f"<del>{old_part}</del>")
        elif tag == "insert":
            out.append(f"<ins>{new_part}</ins>")
        elif tag == "replace":
            out.append(f"<del>{old_part}</del><ins>{new_part}</ins>")
    return "".join(out)


def render_diff_block(old, new):
    """Render a single before/after pair as inline track-changes markdown."""
    if not old and new:
        return f"<ins>{new}</ins>"
    if old and not new:
        return f"<del>{old}</del>"
    return word_level_diff(old, new)


def render_concept_block(fields):
    """Render a concept's full set of fields as a bullet list."""
    lines = []
    for key, label in FIELD_LABELS:
        lines.append(f"- **{label}:** {render_field_value(fields[key])}")
    return "\n".join(lines)


def row_fields(row):
    """Convert a CSV row dict into the same flat field shape as concept_fields."""
    return {
        "code": (row.get('Term') or '').strip(),
        "display": (row.get('Synonym') or '').strip() or (row.get('Term') or '').strip(),
        "status": (row.get('Status') or '').strip(),
        "en": (row.get('EN') or '').strip(),
        "fr": (row.get('FR') or '').strip(),
        "nl": (row.get('NL') or '').strip(),
    }


def render_diff_report(glossary_key, config, comparison, old_cs, new_cs,
                       preview=False, conflicts=None):
    """Build the full markdown report string."""
    added = comparison["added"]
    removed = comparison["removed"]
    modified = comparison["modified"]
    conflicts = conflicts or []

    lines = []
    title_prefix = "PREVIEW: Glossary changes" if preview else "Glossary changes"
    lines.append(f"# {title_prefix} - {config['title']}")
    lines.append("")
    if preview:
        lines.append("> **Preview only** - the JSON has NOT been modified. "
                     "Re-run without `--preview` to apply.")
        lines.append("")
    lines.append(f"- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"- Glossary key: `{glossary_key}`")
    lines.append(f"- Previous version: `{old_cs.get('version', '?')}` "
                 f"(date `{old_cs.get('date', '?')}`)")
    lines.append(f"- New version: `{new_cs.get('version', '?')}` "
                 f"(date `{new_cs.get('date', '?')}`)")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Concepts before: **{comparison['total_old']}**")
    lines.append(f"- Concepts after: **{comparison['total_new']}**")
    lines.append(f"- Added: **{len(added)}**")
    lines.append(f"- Removed: **{len(removed)}**")
    lines.append(f"- Modified: **{len(modified)}**")
    if conflicts:
        lines.append(f"- Conflicts (skipped on accept): **{len(conflicts)}**")
    lines.append("")

    if added:
        lines.append(f"## Added ({len(added)})")
        lines.append("")
        for fields in added:
            lines.append(f"### + `{fields['code']}`")
            lines.append("")
            lines.append(render_concept_block(fields))
            lines.append("")

    if removed:
        lines.append(f"## Removed ({len(removed)})")
        lines.append("")
        for fields in removed:
            lines.append(f"### - `{fields['code']}`")
            lines.append("")
            lines.append(render_concept_block(fields))
            lines.append("")

    if modified:
        lines.append(f"## Modified ({len(modified)})")
        lines.append("")
        for code, changes in modified:
            lines.append(f"### ~ `{code}`")
            lines.append("")
            for _key, label, old_value, new_value in changes:
                lines.append(f"**{label}:**")
                lines.append("")
                lines.append(render_diff_block(old_value, new_value))
                lines.append("")

    if conflicts:
        lines.append(f"## Conflicts ({len(conflicts)}) - will NOT be applied on `--accept`")
        lines.append("")
        lines.append("These codes already exist in the current glossary with different "
                     "field values. The current version wins; the proposed change is "
                     "shown below for review. To apply, rename the proposed code or "
                     "remove the current row first.")
        lines.append("")
        for code, current_row, proposed_row in conflicts:
            current_fields = row_fields(current_row)
            proposed_fields = row_fields(proposed_row)
            lines.append(f"### ! `{code}`")
            lines.append("")
            for key, label in FIELD_LABELS:
                old_value = current_fields[key]
                new_value = proposed_fields[key]
                if old_value == new_value:
                    continue
                lines.append(f"**{label}:**")
                lines.append("")
                lines.append(render_diff_block(old_value, new_value))
                lines.append("")

    if not (added or removed or modified or conflicts):
        lines.append("_No content changes detected._")
        lines.append("")

    return "\n".join(lines)


def write_diff_report(glossary_key, config, script_dir,
                      previous_codesystem, new_codesystem, preview=False,
                      conflicts=None):
    """Compare previous vs new CodeSystem and write a markdown diff report.

    preview=True writes the report under a `-preview` filename so it does not
    get confused with reports recording an applied change.
    conflicts: optional list of (code, current_row, proposed_row) tuples,
    rendered as a separate section.
    """
    comparison = compare_codesystems(previous_codesystem, new_codesystem)
    conflicts = conflicts or []

    if not (comparison["added"] or comparison["removed"]
            or comparison["modified"] or conflicts):
        print("  No content changes - skipping diff report.")
        return None

    report = render_diff_report(glossary_key, config, comparison,
                                previous_codesystem, new_codesystem,
                                preview=preview, conflicts=conflicts)

    reports_dir = script_dir / "glossary-changes"
    reports_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    suffix = "-preview" if preview else ""
    report_path = reports_dir / f"{glossary_key}-{timestamp}{suffix}.md"
    report_path.write_text(report, encoding='utf-8')

    label = "Preview diff" if preview else "Diff report"
    summary = (f"+{len(comparison['added'])} / -{len(comparison['removed'])} / "
               f"~{len(comparison['modified'])}")
    if conflicts:
        summary += f" / !{len(conflicts)} conflicts"
    print(f"  {label}: {report_path.relative_to(script_dir)} ({summary})")
    return report_path


def codesystem_to_csv_rows(codesystem):
    """Convert a CodeSystem dict's concepts into CSV row dicts."""
    rows = []
    for concept in codesystem.get("concept", []):
        code = concept.get("code", "")
        display = concept.get("display", "")
        synonym = display if display and display != code else ""

        status = ""
        for prop in concept.get("property", []):
            if prop.get("code") == "status":
                status = prop.get("valueCode", "")
                break

        designations = {d.get("language"): d.get("value", "")
                        for d in concept.get("designation", [])}

        rows.append({
            "Term": code,
            "Status": status,
            "Synonym": synonym,
            "FR": designations.get("fr", ""),
            "EN": designations.get("en", ""),
            "NL": designations.get("nl", ""),
        })
    return rows


def write_csv_from_codesystem(glossary_key, config, script_dir):
    """Extract a CodeSystem JSON back into its source CSV."""
    csv_path = script_dir / config["csv_file"]
    json_path = script_dir / config["output_file"]

    if not json_path.exists():
        print(f"Warning: JSON file not found: {json_path}")
        return False

    with open(json_path, 'r', encoding='utf-8') as f:
        codesystem = json.load(f)

    rows = codesystem_to_csv_rows(codesystem)

    if csv_path.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = csv_path.with_suffix(f".{timestamp}.backup.csv")
        shutil.copy(csv_path, backup_path)
        print(f"  Backup created: {backup_path.name}")

    fieldnames = ["Term", "Status", "Synonym", "FR", "EN", "NL"]
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';',
                                quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(rows)

    print(f"  Total concepts: {len(rows)}")
    print(f"  Output: {csv_path}")
    return True


def list_glossaries():
    """List all available glossaries."""
    print("\nAvailable glossaries:")
    print("-" * 60)
    for key, config in GLOSSARIES.items():
        print(f"  {key:15} - {config['title']}")
        print(f"                  CSV: {config['csv_file']}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Generate FHIR CodeSystems from glossary CSV files"
    )
    parser.add_argument(
        "glossary",
        nargs="?",
        help="Specific glossary to generate (default: all)"
    )
    parser.add_argument(
        "--mode",
        choices=["full", "incremental"],
        default="full",
        help="full: replace entire CodeSystem from CSV (default). "
             "incremental: only add new terms not already in the CodeSystem."
    )
    parser.add_argument(
        "--to-csv",
        action="store_true",
        help="Reverse direction: extract concepts from JSON back into CSV "
             "(used when concepts were edited directly in the JSON)."
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Diff current.csv vs (current.csv + proposed.csv) and write a "
             "`*-preview.md` report under glossary-changes/. No file is modified."
    )
    parser.add_argument(
        "--accept",
        action="store_true",
        help="Merge proposed.csv into current.csv (skips conflicts), clears "
             "proposed.csv, and regenerates the JSON. Backs up both CSVs."
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available glossaries"
    )

    args = parser.parse_args()

    if args.list:
        list_glossaries()
        return 0

    script_dir = Path(__file__).parent

    exclusive = [args.to_csv, args.preview, args.accept]
    if sum(bool(x) for x in exclusive) > 1:
        print("Error: --to-csv, --preview and --accept are mutually exclusive.")
        return 1

    if args.to_csv:
        direction = "JSON -> CSV"
    elif args.preview:
        direction = "PREVIEW: current vs current+proposed (no files modified)"
    elif args.accept:
        direction = "ACCEPT: merge proposed into current, then regen JSON"
    else:
        direction = f"CSV -> JSON ({args.mode})"

    print(f"\nGlossary Generator v{GLOSSARY_VERSION}")
    print(f"Direction: {direction}")
    print("=" * 60)

    def dispatch(key, config):
        if args.to_csv:
            write_csv_from_codesystem(key, config, script_dir)
        elif args.preview:
            preview_proposed_changes(key, config, script_dir)
        elif args.accept:
            accept_proposed_changes(key, config, script_dir)
        else:
            generate_codesystem(key, config, script_dir, args.mode)

    if args.glossary:
        if args.glossary not in GLOSSARIES:
            print(f"Error: Unknown glossary '{args.glossary}'")
            list_glossaries()
            return 1

        print(f"\nProcessing: {args.glossary}")
        dispatch(args.glossary, GLOSSARIES[args.glossary])
    else:
        print("\nProcessing all glossaries...")
        for key, config in GLOSSARIES.items():
            print(f"\n[{key}]")
            dispatch(key, config)

    print("\nDone!")
    return 0


if __name__ == '__main__':
    exit(main())
