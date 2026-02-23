"""
Generate FHIR CodeSystems from glossary CSV files.

Reads CSV files with glossary terms and translations (FR, EN, NL)
and generates FHIR R4 CodeSystem JSON files.

Glossary configuration is defined in GLOSSARIES dict below.
CSV files should be placed in the root directory.

Usage:
  python generate_glossary.py              # Generate all glossaries
  python generate_glossary.py clinical     # Generate specific glossary
  python generate_glossary.py --list       # List available glossaries
"""

import argparse
import csv
import json
import shutil
from datetime import datetime
from pathlib import Path

# Glossary configurations
# Each glossary has: csv_file, output_file, id, url, name, title, description
GLOSSARIES = {
    "clinical": {
        "csv_file": "GlossaryTerms.csv",
        "output_file": "_resources/glossary/CodeSystem-glossary.json",
        "id": "clinical-glossary",
        "url": "http://example.org/CodeSystem/BeSafeShareGlossary",
        "name": "ClinicalGlossary",
        "title": "BeSafeShare Clinical Glossary",
        "description": "Clinical terms and definitions used across Belgian CareSets for semantic interoperability of healthcare data elements."
    },
    "operational": {
        "csv_file": "OperationalGlossary.csv",
        "output_file": "_resources/glossary/CodeSystem-operational-glossary.json",
        "id": "operational-glossary",
        "url": "http://example.org/CodeSystem/BeSafeShareOperationalGlossary",
        "name": "OperationalGlossary",
        "title": "BeSafeShare Operational Glossary",
        "description": "Operational terms and definitions used in the BeSafeShare ecosystem for project management and governance."
    }
}

# Read version from VERSION file
def get_version():
    version_file = Path(__file__).parent / "VERSION"
    if version_file.exists():
        return version_file.read_text().strip()
    return "0.1"

GLOSSARY_VERSION = get_version()

# Status definitions
STATUS_DEFINITIONS = {
    "accepted": "The concept has been reviewed and accepted for use",
    "rejected": "The concept has been reviewed and rejected",
    "draft": "The concept is in draft status and pending review",
    "active": "The concept is active and in use"
}


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


def generate_codesystem(glossary_key, config, script_dir, mode="full"):
    """Generate a CodeSystem from a glossary CSV file.

    mode: "full" replaces the entire CodeSystem, "incremental" only adds new codes.
    """
    csv_path = script_dir / config["csv_file"]
    output_path = script_dir / config["output_file"]

    if not csv_path.exists():
        print(f"Warning: CSV file not found: {csv_path}")
        return False

    # Backup existing CodeSystem if it exists
    if output_path.exists():
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
        # Full replacement
        codesystem = {
            "resourceType": "CodeSystem",
            "id": config["id"],
            "url": config["url"],
            "version": GLOSSARY_VERSION,
            "name": config["name"],
            "title": config["title"],
            "status": "active",
            "date": datetime.now().strftime("%Y-%m-%d"),
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
            "count": len(csv_concepts),
            "concept": csv_concepts
        }

    # Write output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(codesystem, f, indent=2, ensure_ascii=False)

    print(f"  Total concepts: {codesystem['count']}")
    print(f"  Output: {output_path}")
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
        "--list",
        action="store_true",
        help="List available glossaries"
    )

    args = parser.parse_args()

    if args.list:
        list_glossaries()
        return 0

    script_dir = Path(__file__).parent

    print(f"\nGlossary Generator v{GLOSSARY_VERSION}")
    print(f"Mode: {args.mode}")
    print("=" * 60)

    if args.glossary:
        # Generate specific glossary
        if args.glossary not in GLOSSARIES:
            print(f"Error: Unknown glossary '{args.glossary}'")
            list_glossaries()
            return 1

        print(f"\nGenerating: {args.glossary}")
        generate_codesystem(args.glossary, GLOSSARIES[args.glossary], script_dir, args.mode)
    else:
        # Generate all glossaries
        print("\nGenerating all glossaries...")
        for key, config in GLOSSARIES.items():
            print(f"\n[{key}]")
            generate_codesystem(key, config, script_dir, args.mode)

    print("\nDone!")
    return 0


if __name__ == '__main__':
    exit(main())
