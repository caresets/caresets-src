"""
Identify, and strip, the id / extension / modifierExtension elements a logical
model carries only because of what it is based on.

A logical model whose baseDefinition is FHIR's `Element` inherits three
elements it never asked for: `<Model>.id`, `<Model>.extension` and
`<Model>.modifierExtension`. They appear in the snapshot, never in the
differential, and they are not part of the business model. A model based on
`Base` has none at the root, but any group typed BackboneElement inside it
carries the same three one level down (`<Model>.names.id`, ...), for the same
reason.

This module does two things:

  identify(sd)   -> a report: the base, and every such element, split into
                    root-level (from Element) and nested (from BackboneElement)
  strip(sd)      -> the same StructureDefinition without them, plus the report

Used by build_content.py when it copies input/models/ into _resources/models/,
so the served models never carry them at any level (the model viewer shows
every snapshot element it is given), and as a script over a folder:

  python preprocess_models.py                          report on _resources/models/
  python preprocess_models.py --dir input/models       another folder
  python preprocess_models.py --strip --all-levels     rewrite a folder in place

The same module lives in the caresets-app as server/preprocess.py; keep the two
in step.
"""

import argparse
import copy
import glob
import io
import json
import os
import sys

NOISE = ("id", "extension", "modifierExtension")
ELEMENT_BASES = {"Element", "BackboneElement"}


def base_of(sd):
    return (sd.get("baseDefinition") or "").split("|")[0].rstrip("/").rsplit("/", 1)[-1]


def _noise_paths(sd, section):
    out = []
    for e in (sd.get(section) or {}).get("element", []):
        path = e.get("path") or ""
        parts = path.split(".")
        if len(parts) >= 2 and parts[-1] in NOISE:
            out.append({"path": path, "level": "root" if len(parts) == 2 else "nested"})
    return out


def identify(sd):
    """What the model is based on and which inherited elements it carries."""
    base = base_of(sd)
    snap = _noise_paths(sd, "snapshot")
    diff = _noise_paths(sd, "differential")
    return {
        "name": sd.get("name") or sd.get("id"),
        "base": base,
        "elementBased": base in ELEMENT_BASES,
        "root": [n["path"] for n in snap if n["level"] == "root"],
        "nested": [n["path"] for n in snap if n["level"] == "nested"],
        "inDifferential": [n["path"] for n in diff],
    }


def strip(sd, all_levels=False):
    """Return (cleaned copy, report). Nothing is removed from the differential
    unless it is there too, which the publisher's models never do."""
    report = identify(sd)
    remove = set(report["root"])
    if all_levels or report["elementBased"]:
        remove |= set(report["nested"])
    remove |= set(report["inDifferential"]) & remove
    if not remove:
        report["removed"] = []
        return sd, report
    out = copy.deepcopy(sd)
    for section in ("snapshot", "differential"):
        block = out.get(section)
        if block and block.get("element"):
            block["element"] = [e for e in block["element"] if (e.get("path") or "") not in remove]
    report["removed"] = sorted(remove)
    return out, report


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--dir", default=os.path.join(here, "_resources", "models"),
                    help="folder of StructureDefinition-*.json (default: the served models)")
    ap.add_argument("--strip", action="store_true", help="rewrite the files without the elements")
    ap.add_argument("--all-levels", action="store_true",
                    help="also strip the nested ones in models based on Base")
    args = ap.parse_args(argv)

    sys.stdout.reconfigure(encoding="utf-8")
    files = sorted(glob.glob(os.path.join(args.dir, "*.json")))
    element_based, base_based_nested, changed = [], [], 0
    for fn in files:
        with io.open(fn, encoding="utf-8-sig") as fh:
            sd = json.load(fh)
        if sd.get("resourceType") != "StructureDefinition" or sd.get("kind") != "logical":
            continue
        cleaned, rep = strip(sd, args.all_levels)
        if rep["elementBased"]:
            element_based.append(rep)
        elif rep["nested"]:
            base_based_nested.append(rep)
        if args.strip and rep["removed"]:
            with io.open(fn, "w", encoding="utf-8", newline="\n") as fh:
                json.dump(cleaned, fh, ensure_ascii=False, indent=2)
            changed += 1

    print("Based on Element (%d): the root id/extension/modifierExtension come from the base"
          % len(element_based))
    for r in element_based:
        print("  %-34s base=%-8s root=%d nested=%d%s" % (
            r["name"], r["base"], len(r["root"]), len(r["nested"]),
            "  -> stripped %d" % len(r["removed"]) if args.strip and r["removed"] else ""))
    print("\nBased on Base but with nested ones from BackboneElement groups (%d)%s"
          % (len(base_based_nested), "" if args.all_levels else "  [reported only; --all-levels strips them]"))
    for r in base_based_nested:
        print("  %-34s base=%-8s nested=%d  %s%s" % (
            r["name"], r["base"], len(r["nested"]),
            ", ".join(p.split(".", 1)[1] for p in r["nested"][:3]) + (" …" if len(r["nested"]) > 3 else ""),
            "  -> stripped %d" % len(r["removed"]) if args.strip and r["removed"] else ""))
    if args.strip:
        print("\n%d file(s) rewritten" % changed)
    else:
        print("\n(nothing written; add --strip to rewrite)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
