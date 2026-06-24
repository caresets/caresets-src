"""
Versioned backups of the input/ source content.

A snapshot of the entire input/ folder is stored under backups/v<VERSION>/,
where <VERSION> comes from the VERSION file. Re-running for the same version
refreshes that snapshot; bumping VERSION creates a new one and preserves the
old, giving one restorable backup per released version.

Runs automatically on every publish (see .github/workflows/publish.yml) and
can be run by hand whenever the content changes.

Usage:
  python backup_content.py                 # snapshot input/ -> backups/v<VERSION>/
  python backup_content.py --list          # list available version backups
  python backup_content.py --restore 0.1   # restore backups/v0.1/ -> input/
"""

import argparse
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent
INPUT = ROOT / "input"
BACKUPS = ROOT / "backups"


def get_version():
    vf = ROOT / "VERSION"
    return vf.read_text().strip() if vf.exists() else "0.1"


def snapshot():
    version = get_version()
    dest = BACKUPS / f"v{version}"
    if not INPUT.exists():
        print(f"ERROR: {INPUT} does not exist; nothing to back up.")
        return 1

    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(INPUT, dest)

    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    count = sum(1 for _ in dest.rglob("*") if _.is_file())
    (dest / "BACKUP_INFO.txt").write_text(
        f"version: {version}\n"
        f"created: {stamp}\n"
        f"files:   {count}\n"
    )
    print(f"Backed up input/ -> {dest.relative_to(ROOT)} ({count} files, {stamp})")
    return 0


def list_backups():
    if not BACKUPS.exists():
        print("No backups yet.")
        return 0
    versions = sorted(p for p in BACKUPS.iterdir() if p.is_dir())
    if not versions:
        print("No backups yet.")
        return 0
    print("Available version backups:")
    for v in versions:
        info = v / "BACKUP_INFO.txt"
        created = ""
        if info.exists():
            for line in info.read_text().splitlines():
                if line.startswith("created:"):
                    created = line.split(":", 1)[1].strip()
        print(f"  {v.name}{('  (' + created + ')') if created else ''}")
    return 0


def restore(version):
    version = version.lstrip("v")
    src = BACKUPS / f"v{version}"
    if not src.exists():
        print(f"ERROR: backup {src.relative_to(ROOT)} not found. Use --list.")
        return 1

    # Safety: snapshot the current input/ before overwriting it.
    if INPUT.exists():
        safety = BACKUPS / "_pre-restore"
        if safety.exists():
            shutil.rmtree(safety)
        shutil.copytree(INPUT, safety)
        print(f"Saved current input/ -> {safety.relative_to(ROOT)} (in case you need to undo)")
        shutil.rmtree(INPUT)

    shutil.copytree(src, INPUT)
    # Drop the backup's metadata file from the restored input/
    info = INPUT / "BACKUP_INFO.txt"
    if info.exists():
        info.unlink()
    print(f"Restored {src.relative_to(ROOT)} -> input/")
    print("Now run:  python build_content.py")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Versioned backups of input/ content")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--list", action="store_true", help="list available backups")
    group.add_argument("--restore", metavar="VERSION", help="restore a version into input/")
    args = parser.parse_args()

    if args.list:
        return list_backups()
    if args.restore:
        return restore(args.restore)
    return snapshot()


if __name__ == "__main__":
    raise SystemExit(main())
