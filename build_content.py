"""
Regenerate all served content from the input/ source folder.

This is the single command to run after editing anything in input/.
It performs three steps, in order:

  1. Sync  input/models/  ->  _resources/models/   (the models Jekyll serves)
  2. Generate the glossary CodeSystems from input/*.csv  -> _resources/glossary/
  3. Apply input/glossary_mappings.csv -> element.code in _resources/models/

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
    print(f"[1/3] Syncing models: {INPUT_MODELS} -> {SERVED_MODELS}")
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
    rc = sync_models()
    if rc:
        return rc

    print("[2/3] Generating glossary CodeSystems")
    rc = run("  run", ["generate_glossary.py"])
    if rc:
        return rc

    print("[3/3] Applying glossary mappings to models")
    rc = run("  run", ["add_glossary_mappings.py"])
    if rc:
        return rc

    print("\nDone. Served content regenerated under _resources/.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
