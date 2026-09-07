"""
Import published StructureDefinitions into input/models/.

This is how models arrive: they are authored as workbooks, generated into
StructureDefinitions, published as part of the eHealth package, and the
published export comes back here as a zip.

  models/xls/*.xlsx  ->  import_logical_model_xlsx.py  ->  models/generated/
        |
        |   (published upstream)
        v
  caresets-structuredefinitions-<date>.zip
        |   import_models_zip.py        <- this script
        v
  input/models/            published models
  input/models/draft/      models still marked draft in the export

Two things it is careful about, both learned the hard way:

  * A model is identified by the `name`, `url` and `id` inside the file, never
    by its filename. The same model is `BeModelVaccination.json` in the export
    and `StructureDefinition-be-model-vaccination.json` here; writing the
    export's filename would leave the old file in place as a silent duplicate,
    with glossary_mappings.csv still pointing at the stale copy. Existing
    filenames are kept.

  * Placement follows the export's own `stage` field in index.json - published
    or draft - rather than a guess, so a model promoted out of draft upstream
    moves here too, instead of existing in both folders.

Usage:
  python import_models_zip.py path/to/export.zip
  python import_models_zip.py path/to/export.zip --dry-run
  python import_models_zip.py path/to/unpacked/folder
"""

import argparse
import glob
import io
import json
import os
import sys
import zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
PUBLISHED_DIR = os.path.join("input", "models")
DRAFT_DIR = os.path.join("input", "models", "draft")


def load_source(path):
    """(filename -> parsed json) for every StructureDefinition, plus the index."""
    docs, index = {}, None
    if os.path.isdir(path):
        for p in glob.glob(os.path.join(path, "**", "*.json"), recursive=True):
            try:
                d = json.load(io.open(p, encoding="utf-8"))
            except ValueError:
                continue
            if d.get("resourceType") == "StructureDefinition":
                docs[os.path.basename(p)] = d
            elif os.path.basename(p) == "index.json":
                index = d
        return docs, index

    with zipfile.ZipFile(path) as z:
        for n in z.namelist():
            if not n.lower().endswith(".json"):
                continue
            try:
                d = json.loads(z.read(n))
            except ValueError:
                continue
            if isinstance(d, dict) and d.get("resourceType") == "StructureDefinition":
                docs[os.path.basename(n)] = d
            elif os.path.basename(n) == "index.json":
                index = d
    return docs, index


def index_existing():
    """Every model already here, by each identifier it can be matched on."""
    by_key, paths = {}, {}
    for p in glob.glob(os.path.join(ROOT, PUBLISHED_DIR, "**", "*.json"), recursive=True):
        try:
            d = json.load(io.open(p, encoding="utf-8"))
        except ValueError:
            continue
        if d.get("resourceType") != "StructureDefinition":
            continue
        rel = os.path.relpath(p, ROOT).replace("\\", "/")
        paths[d.get("name")] = rel
        for k in (d.get("name"), d.get("url"), d.get("id")):
            if k:
                by_key.setdefault(str(k).lower(), rel)
    return by_key, paths


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", help="the export .zip, or an unpacked folder")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not os.path.exists(args.source):
        sys.exit("Not found: %s" % args.source)

    docs, index = load_source(args.source)
    if not docs:
        sys.exit("No StructureDefinitions in %s" % args.source)

    stage = {}
    if index:
        for m in index.get("models", []) or []:
            if m.get("name"):
                stage[m["name"]] = (m.get("stage") or "").lower()

    by_key, _ = index_existing()
    sys.stdout.reconfigure(encoding="utf-8")
    print("Source : %s" % args.source)
    print("Models : %d" % len(docs))
    print("Index  : %s\n" % ("yes, stage taken from it" if index else
                             "MISSING - everything treated as published"))

    actions = []
    for fname, doc in sorted(docs.items(), key=lambda kv: kv[1].get("name") or kv[0]):
        name = doc.get("name") or os.path.splitext(fname)[0]
        published = stage.get(name, "published") != "draft"
        dest_dir = PUBLISHED_DIR if published else DRAFT_DIR

        old_rel = None
        for k in (doc.get("name"), doc.get("url"), doc.get("id")):
            if k and str(k).lower() in by_key:
                old_rel = by_key[str(k).lower()]
                break

        base = os.path.basename(old_rel) if old_rel else "StructureDefinition-%s.json" % name
        dest_rel = "%s/%s" % (dest_dir.replace("\\", "/"), base)

        prev = json.load(io.open(os.path.join(ROOT, old_rel), encoding="utf-8")) if old_rel else None
        if prev == doc and old_rel == dest_rel:
            actions.append(("unchanged", name, dest_rel, doc.get("version")))
            continue
        ver = ("%s -> %s" % (prev.get("version"), doc.get("version"))) if prev else doc.get("version")
        if old_rel is None:
            kind = "new"
        elif old_rel != dest_rel:
            kind = "moved"
        else:
            kind = "updated"
        actions.append((kind, name, dest_rel if kind != "moved" else "%s -> %s" % (old_rel, dest_rel), ver))

        if args.dry_run:
            continue
        os.makedirs(os.path.join(ROOT, dest_dir), exist_ok=True)
        with io.open(os.path.join(ROOT, dest_rel), "w", encoding="utf-8", newline="\n") as fh:
            json.dump(doc, fh, ensure_ascii=False, indent=2)
        if old_rel and old_rel != dest_rel:
            os.remove(os.path.join(ROOT, old_rel))

    for kind in ("new", "moved", "updated", "unchanged"):
        rows = [a for a in actions if a[0] == kind]
        if not rows:
            continue
        print("%s (%d)" % (kind.upper(), len(rows)))
        for _, name, where, ver in rows:
            print("  %-32s %-18s %s" % (name, ver or "", where))
        print()

    here = {n for n in index_existing()[1] if n}
    incoming = {d.get("name") for d in docs.values()}
    only_here = sorted(n for n in here if n and n not in incoming)
    if only_here:
        print("Not in this export, left untouched (%d): %s" % (len(only_here), ", ".join(only_here)))

    if args.dry_run:
        print("\n--dry-run: nothing written")
    else:
        print("Next: python build_content.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
