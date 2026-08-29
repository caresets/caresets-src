#!/usr/bin/env python
"""Render a definition-quality review report (.md) and its machine sidecar
(.findings.json) from a single findings JSON, so the two cannot drift apart.

Input JSON:
{
  "scope": "Glossaire v1 - status Active",
  "source": "input/Glossaire CareSets V1 28-08-2026.xlsx",
  "sheet": "Glossaire v1",
  "terms_reviewed": 23,
  "intro": "optional extra paragraph",
  "findings": [
    {"row": 5, "term": "BodyLaterality", "lang": "fr",
     "rules": [3, 4], "severity": "major",
     "current": "la lateralite du corps .",
     "problem": "...",
     "proposed": "...",                    # or {"fr": "...", "nl": "..."}
     "description_move": "...",            # optional
     "note": "..."}                        # optional
  ]
}

`lang` is fr | nl | en | meta. A `meta` finding is cross-cutting (term naming,
column misuse, a synonym that contradicts another entry) and is applied by hand,
not by apply_decisions.py.

Usage:
    python render_report.py FINDINGS.json --out glossary-changes/definition-quality-<ts>.md
"""
import argparse
import datetime as dt
import json
import os
import re
import sys

SEV_ORDER = {"major": 0, "missing": 1, "minor": 2}
LANG_LABEL = {"fr": "FR", "nl": "NL", "en": "EN", "meta": "cross-cutting"}
# Findings read in row order, so the report can be walked alongside the sheet.
# Within a row, the cross-cutting note comes first: it is context for the
# per-language findings that follow it.
LANG_ORDER = {"meta": 0, "fr": 1, "nl": 2, "en": 3}
RULE_NAMES = {
    1: "substitution",
    2: "grammatical category",
    3: "non-circularity",
    4: "genus + differentia",
    5: "positive formulation",
    6: "one concept",
    7: "no requirements/examples",
    8: "necessary and sufficient",
    9: "understandable terms",
    10: "concept-system consistency",
}

HOWTO = """## How to review this file

For every finding, edit its `decision` block:

- `status: accept` - take the proposed wording as it stands.
- `status: revise` - put **your** wording on the `fr:`, `nl:` and/or `en:` line;
  it is used verbatim, nothing is rewritten on top of it.
- `status: reject` - leave the current definition alone.
- `status: pending` - undecided; nothing is applied.

Anything on `comment:` is read back but never written into the glossary. Nothing
outside these blocks is parsed, so notes in the margins are safe.

When you are done, hand the file back: it is read with `collect_decisions.py`,
then applied to a **new copy** of the workbook - the source `.xlsx` is never
edited in place.
"""


def quote(text):
    text = (text or "").strip()
    if not text:
        return "> *(empty)*"
    return "\n".join("> " + ln if ln.strip() else ">" for ln in text.splitlines())


def rules_str(rules):
    if not rules:
        return "-"
    return ", ".join("%d (%s)" % (r, RULE_NAMES.get(r, "?")) for r in rules)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("findings")
    ap.add_argument("--out", required=True)
    ap.add_argument("--preserve-decisions", dest="preserve",
                    help="an existing report whose ```decision blocks are carried into the new "
                         "one, matched by finding id. Use whenever findings are added to a review "
                         "that is already being worked through, so recorded decisions survive the "
                         "re-render. Ids must be explicit in the findings JSON for this to be safe.")
    args = ap.parse_args()

    kept = {}
    if args.preserve:
        with open(args.preserve, encoding="utf-8") as fh:
            old = fh.read()
        for m in re.finditer(
            r"^```decision[ \t]+(?P<id>[A-Za-z0-9_.-]+)[ \t]*\n(?P<body>.*?)^```[ \t]*$",
            old, re.MULTILINE | re.DOTALL,
        ):
            kept[m.group("id")] = m.group("body").rstrip("\n")

    with open(args.findings, encoding="utf-8") as fh:
        data = json.load(fh)
    findings = data["findings"]

    def sort_key(f):
        return (
            f.get("row") or 0,
            LANG_ORDER.get(f.get("lang"), 9),
            SEV_ORDER.get(f.get("severity"), 9),
        )

    findings.sort(key=sort_key)
    for i, f in enumerate(findings, start=1):
        f["id"] = f.get("id") or "F-%03d" % i

    by_lang = {}
    for f in findings:
        by_lang[f["lang"]] = by_lang.get(f["lang"], 0) + 1
    counts = " / ".join(
        "%s %d" % (LANG_LABEL[k], by_lang[k])
        for k in ("fr", "nl", "en", "meta")
        if k in by_lang
    )

    ts = dt.datetime.now()
    out = []
    out.append("# Definition quality review - %s\n" % data.get("scope", ""))
    out.append("- Generated: %s" % ts.strftime("%Y-%m-%d %H:%M:%S"))
    out.append("- Source: `%s`, sheet `%s`" % (data.get("source"), data.get("sheet")))
    out.append("- EN source: `input/ClinicalGlossary.csv`, `input/OperationalGlossary.csv`")
    out.append("- Checklist: `input/Definition quality checklist.md`")
    out.append(
        "- Terms reviewed: **%s** / Findings: **%d** (%s)\n"
        % (data.get("terms_reviewed", "?"), len(findings), counts)
    )
    if data.get("intro"):
        out.append(data["intro"] + "\n")
    out.append(HOWTO)

    by_rule = {}
    for f in findings:
        for r in f.get("rules") or []:
            by_rule[r] = by_rule.get(r, 0) + 1
    by_sev = {}
    for f in findings:
        by_sev[f.get("severity")] = by_sev.get(f.get("severity"), 0) + 1

    out.append("## Findings by rule\n")
    out.append(
        "Severity: "
        + " / ".join(
            "**%s** %d" % (k, by_sev[k]) for k in ("major", "missing", "minor") if k in by_sev
        )
        + "\n"
    )
    out.append("| Rule | | Findings |")
    out.append("|------|--|----------|")
    for r in sorted(by_rule):
        out.append("| %d | %s | %d |" % (r, RULE_NAMES.get(r, "?"), by_rule[r]))
    out.append("")

    out.append("## Summary\n")
    out.append("| ID | Term | Row | Lang | Rules | Severity | Issue |")
    out.append("|----|------|-----|------|-------|----------|-------|")
    for f in findings:
        issue = (f.get("problem") or "").strip().splitlines()[0]
        if len(issue) > 90:
            issue = issue[:87].rstrip() + "..."
        out.append(
            "| %s | %s | %s | %s | %s | %s | %s |"
            % (
                f["id"],
                f.get("term", ""),
                f.get("row", ""),
                LANG_LABEL[f["lang"]],
                ", ".join(str(r) for r in f.get("rules") or []) or "-",
                f.get("severity", ""),
                issue.replace("|", "\\|"),
            )
        )
    out.append("")

    out.append("## Findings\n")
    last_term = object()
    for f in findings:
        if f.get("term") != last_term:
            last_term = f.get("term")
            out.append("---\n")
        head = "### %s - `%s`" % (f["id"], f.get("term", ""))
        if f.get("row"):
            head += " (row %s)" % f["row"]
        head += " - %s" % LANG_LABEL[f["lang"]]
        out.append(head + "\n")
        out.append(
            "**Rules:** %s / **Severity:** %s\n"
            % (rules_str(f.get("rules")), f.get("severity", ""))
        )
        if f.get("current") is not None:
            out.append("**Current**\n")
            out.append(quote(f["current"]) + "\n")
        out.append("**Problem**\n")
        out.append(f.get("problem", "").strip() + "\n")
        prop = f.get("proposed")
        if isinstance(prop, str):
            prop = {f["lang"]: prop}
        if prop:
            out.append("**Proposed**\n")
            for lang in ("fr", "nl", "en", "meta"):
                if prop.get(lang):
                    label = "" if len(prop) == 1 else "%s: " % lang.upper()
                    out.append(quote(label + prop[lang]) + "\n")
        if f.get("description_move"):
            out.append("**Move to the `Description` column:** %s\n" % f["description_move"])
        if f.get("note"):
            out.append("**Note:** %s\n" % f["note"])
        out.append("```decision %s" % f["id"])
        if f["id"] in kept:
            out.append(kept[f["id"]])
        else:
            out.append("status: pending        # accept | reject | revise")
            for lang in ("fr", "nl", "en"):
                out.append("%s:" % lang)
            out.append("comment:")
        out.append("```\n")

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(out))

    sidecar = os.path.splitext(args.out)[0] + ".findings.json"
    slim = []
    for f in findings:
        prop = f.get("proposed")
        if isinstance(prop, str):
            prop = {f["lang"]: prop}
        slim.append(
            {
                "id": f["id"],
                "row": f.get("row"),
                "term": f.get("term"),
                "lang": f["lang"],
                "rules": f.get("rules"),
                "severity": f.get("severity"),
                "current": f.get("current"),
                "proposed": prop or {},
                "description_move": f.get("description_move"),
            }
        )
    with open(sidecar, "w", encoding="utf-8") as fh:
        json.dump(slim, fh, ensure_ascii=False, indent=2)

    sys.stdout.reconfigure(encoding="utf-8")
    print("Report : %s (%d findings)" % (args.out, len(findings)))
    if args.preserve:
        carried = sum(1 for f in findings if f["id"] in kept)
        print("Carried over %d of %d recorded decision block(s) from %s"
              % (carried, len(kept), args.preserve))
        lost = sorted(set(kept) - {f["id"] for f in findings})
        if lost:
            print("  ! %d decision(s) had no matching finding and were DROPPED: %s"
                  % (len(lost), ", ".join(lost)))
    print("Sidecar: %s" % sidecar)


if __name__ == "__main__":
    main()
