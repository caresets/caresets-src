"""
Add glossary code mappings to FHIR StructureDefinition models.

This script reads mappings from a CSV file and either:
1. Adds the 'code' property to elements in the model files (default)
2. Generates a FHIR ConceptMap resource (with --conceptmap flag)

Usage:
  python add_glossary_mappings.py                  # Add to element.code
  python add_glossary_mappings.py --conceptmap     # Generate ConceptMap
"""

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path

GLOSSARY_SYSTEM = "http://example.org/CodeSystem/BeSafeShareGlossary"


def load_mappings_from_csv(csv_path):
    """Load mappings from CSV file."""
    mappings = {}
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            model = row.get('Model', '').strip()
            element_suffix = row.get('ElementSuffix', '').strip()
            glossary_code = row.get('GlossaryCode', '').strip()

            if not all([model, element_suffix, glossary_code]):
                continue

            if model not in mappings:
                mappings[model] = {}
            mappings[model][element_suffix] = glossary_code

    return mappings


def add_to_element_code(mappings, models_dir):
    """Add glossary codes to element.code in model files."""
    for filename, element_mappings in mappings.items():
        filepath = models_dir / filename
        if not filepath.exists():
            print(f"Warning: {filename} not found, skipping")
            continue

        print(f"\nProcessing {filename}...")

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Process both snapshot and differential elements
        updated_count = 0
        for section in ["snapshot", "differential"]:
            if section not in data:
                continue

            elements = data[section].get("element", [])
            for element in elements:
                element_id = element.get("id", "")
                element_path = element.get("path", "")

                # Check if this element matches any of our mappings
                for suffix, glossary_code in element_mappings.items():
                    # Match by checking if the element id ends with the suffix
                    expected_suffix = f".{suffix}"
                    if element_id.endswith(expected_suffix) or element_path.endswith(expected_suffix):
                        # Check if code already exists
                        if "code" in element:
                            # Check if our glossary code is already there
                            existing_codes = [c.get("code") for c in element["code"]]
                            if glossary_code in existing_codes:
                                continue
                            # Add to existing codes
                            element["code"].append({
                                "system": GLOSSARY_SYSTEM,
                                "code": glossary_code
                            })
                        else:
                            # Add new code array
                            element["code"] = [{
                                "system": GLOSSARY_SYSTEM,
                                "code": glossary_code
                            }]
                        updated_count += 1
                        print(f"  Added {glossary_code} to {element_id}")

        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"  Updated {updated_count} elements in {filename}")


def generate_conceptmap(mappings, models_dir, output_path):
    """Generate a FHIR ConceptMap resource from the mappings."""
    # Build groups by source model
    groups = []

    for filename, element_mappings in mappings.items():
        filepath = models_dir / filename
        if not filepath.exists():
            print(f"Warning: {filename} not found, skipping")
            continue

        # Load the model to get its URL
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        model_url = data.get("url", f"http://example.org/StructureDefinition/{data.get('id', filename)}")
        model_name = data.get("name", filename.replace("StructureDefinition-", "").replace(".json", ""))

        # Build elements for this group
        elements = []
        for element_suffix, glossary_code in element_mappings.items():
            elements.append({
                "code": element_suffix,
                "display": f"{model_name}.{element_suffix}",
                "target": [{
                    "code": glossary_code,
                    "display": glossary_code,
                    "equivalence": "equivalent"
                }]
            })

        if elements:
            groups.append({
                "source": model_url,
                "target": GLOSSARY_SYSTEM,
                "element": elements
            })

    # Build the ConceptMap
    conceptmap = {
        "resourceType": "ConceptMap",
        "id": "model-to-glossary",
        "url": "http://example.org/ConceptMap/model-to-glossary",
        "version": "1.0.0",
        "name": "ModelToGlossaryConceptMap",
        "title": "Model Elements to Glossary Mapping",
        "status": "active",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "description": "Maps logical model elements to the BeSafeShare Glossary concepts",
        "sourceUri": "http://example.org/StructureDefinition",
        "targetUri": GLOSSARY_SYSTEM,
        "group": groups
    }

    # Write output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(conceptmap, f, indent=2, ensure_ascii=False)

    print(f"\nGenerated ConceptMap with {len(groups)} groups")
    print(f"Output: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Add glossary mappings to FHIR models or generate a ConceptMap"
    )
    parser.add_argument(
        "--conceptmap",
        action="store_true",
        help="Generate a ConceptMap instead of modifying element.code"
    )
    parser.add_argument(
        "--csv",
        type=str,
        default="input/glossary_mappings.csv",
        help="Path to the mappings CSV file (default: input/glossary_mappings.csv)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="_resources/glossary/ConceptMap-model-to-glossary.json",
        help="Output path for ConceptMap (default: _resources/glossary/ConceptMap-model-to-glossary.json)"
    )

    args = parser.parse_args()

    script_dir = Path(__file__).parent
    csv_path = script_dir / args.csv
    models_dir = script_dir / "_resources" / "models"

    if not csv_path.exists():
        print(f"Error: CSV file not found: {csv_path}")
        return 1

    print(f"Loading mappings from {csv_path}...")
    mappings = load_mappings_from_csv(csv_path)
    print(f"Loaded {sum(len(v) for v in mappings.values())} mappings for {len(mappings)} models")

    if args.conceptmap:
        output_path = script_dir / args.output
        generate_conceptmap(mappings, models_dir, output_path)
    else:
        add_to_element_code(mappings, models_dir)

    return 0


if __name__ == '__main__':
    exit(main())
