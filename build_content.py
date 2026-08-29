"""
Regenerate all served content from the input/ source folder.

This is the single command to run after editing anything in input/.
It performs four steps, in order:

  1. Convert input/Glossaire CareSets*.xlsx -> input/ClinicalGlossary.csv
  2. Sync  input/models/  ->  _resources/models/   (the models Jekyll serves)
  3. Generate the glossary CodeSystems from input/*.csv  -> _resources/glossary/
  4. Apply input/glossary_mappings.csv -> element.code in _resources/models/

The workbook is the source for the clinical glossary, so step 1 regenerates
ClinicalGlossary.csv from it. OperationalGlossary.csv has no workbook behind it
and is still edited by hand.

Everything under _resources/ is GENERATED. Never hand-edit it; edit input/.

Usage:
  python build_content.py
"""

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
INPUT_MODELS = ROOT / "input" / "models"
SERVED_MODELS = ROOT / "_resources" / "models"


def sync_models():
    """Mirror input/models/ into _resources/models/ (recursive, prune stale)."""
    print(f"[2/4] Syncing models: {INPUT_MODELS} -> {SERVED_MODELS}")
    if not INPUT_MODELS.exists():
        print(f"  ERROR: {INPUT_MODELS} does not exist.")
        return 1

    SERVED_MODELS.mkdir(parents=True, exist_ok=True)

    # Source files relative to input/models (includes draft/ subfolder)
    src_files = {p.relative_to(INPUT_MODELS)
                 for p in INPUT_MODELS.rglob("*.json")}

    # Remove served files that no longer exist in the source
    for served in SERVED_MODELS.rglob("*.json"):
        rel = served.relative_to(SERVED_MODELS)
        if rel not in src_files:
            served.unlink()
            print(f"  removed stale {rel}")

    # Copy/refresh every source file
    for rel in sorted(src_files):
        dst = SERVED_MODELS / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(INPUT_MODELS / rel, dst)
    print(f"  synced {len(src_files)} model file(s)")
    return 0


def run(label, args):
    print(f"{label}: {' '.join(args)}")
    result = subprocess.run([sys.executable, *args], cwd=ROOT)
    return result.returncode


def main():
    # Model generation from the logical-model workbooks is NOT run here on
    # purpose. It rewrites every model from models/xls/, so a stale or
    # partly-filled workbook would silently wipe definitions. Run it when the
    # models change, look at the diff, then run this:
    #     python import_logical_model_xlsx.py
    print("[1/4] Converting the glossary workbook to CSV")
    rc = run("  run", ["import_glossary_xlsx.py"])
    if rc:
        return rc

    rc = sync_models()
    if rc:
        return rc

    print("[3/4] Generating glossary CodeSystems")
    rc = run("  run", ["generate_glossary.py"])
    if rc:
        return rc

    print("[4/4] Applying glossary mappings to models")
    rc = run("  run", ["add_glossary_mappings.py"])
    if rc:
        return rc

    print("\nDone. Served content regenerated under _resources/.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
