"""
Build a ConceptMap from the confirmed model-to-glossary mappings.

The mapping between a logical model element and a glossary concept is a
statement *about* the two, not a property of either. Writing it into
`element.code` puts it inside the StructureDefinition, which means the models
handed over for publication are no longer the models that were imported, and a
change of mapping becomes a change of model. A ConceptMap keeps the mapping as
its own resource: the StructureDefinitions stay exactly as published, and the
mapping can be versioned, reviewed and republished on its own.

  input/glossary_mappings.csv   confirmed rows, targets that are approved terms
        |
        v
  ConceptMap-model-to-glossary.json     one group per (model, glossary)

Element codes are the real ElementDefinition paths, read from the models rather
than assembled from the CSV: an element's path is not always the model's name
(BeModelVaccination's elements live under be-model-vaccination), so a path built
by hand would not resolve.

  python make_conceptmap.py --dry-run
  python make_conceptmap.py
"""

import argparse
import csv
import io
import json
import os
import sys
import time

import glossary_terms

ROOT = os.path.dirname(os.path.abspath(__file__))
MAPPINGS = os.path.join("input", "glossary_mappings.csv")
MODELS = os.path.join("input", "models")
OUT = os.path.join("_resources", "glossary", "ConceptMap-model-to-glossary.json")

CANONICAL = "http://example.org/ConceptMap/model-to-glossary"
# R4 spells the relationship `equivalence` on the target; R5 renamed it to
# `relationship` with a different value set. The models are 4.0.1.
EQUIVALENCE = "equivalent"


def confirmed(path):
    """(model, suffix) -> code, for confirmed rows pointing at approved terms."""
    terms = glossary_terms.load()
    drafted = glossary_terms.workbook_terms()
    rows, held = [], []
    with io.open(path, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh, delimiter=";"):
            model = (r.get("Model") or "").strip()
            suffix = (r.get("ElementSuffix") or "").strip()
            code = (r.get("GlossaryCode") or "").strip()
            if not (model and suffix and code):
                continue
            if (r.get("Status") or "confirmed").strip().lower() != "confirmed":
                continue
            target = glossary_terms.status_of(code, terms, drafted)
            if target != "approved":
                held.append((model, suffix, code, target))
                continue
            rows.append((model, suffix, code))
    return rows, held


def index_models(models_dir):
    """name/url/id -> the parsed model, so a CSV row finds its model however it
    names it. Identity lives inside the file; a filename only agrees with it by
    convention."""
    import glob
    index = {}
    for path in sorted(glob.glob(os.path.join(models_dir, "**", "*.json"),
                                 recursive=True)):
        try:
            doc = json.load(io.open(path, encoding="utf-8"))
        except ValueError:
            continue
        if doc.get("resourceType") != "StructureDefinition":
            continue
        for key in (doc.get("name"), doc.get("id"), doc.get("url"),
                    os.path.splitext(os.path.basename(path))[0]):
            if key:
                index.setdefault(key, doc)
    return index


def element_paths(doc):
    """Every ElementDefinition path in a model, in document order."""
    seen, out = set(), []
    for section in ("differential", "snapshot"):
        for e in doc.get(section, {}).get("element", []):
            p = e.get("path") or e.get("id")
            if p and p not in seen:
                seen.add(p)
                out.append((p, e))
    return out


def resolve(doc, suffix):
    """The element a mapping row names, matched the way the rest of the
    pipeline matches: the row's key is the full path below the root, or a
    trailing part of it."""
    for path, e in element_paths(doc):
        below = path.split(".", 1)[1] if "." in path else ""
        if below == suffix or below.endswith("." + suffix):
            return path, e
    return None, None


def short_of(e):
    s = e.get("short") or e.get("definition") or ""
    return s if len(s) <= 80 else s[:77] + "..."


def build(rows, index, systems):
    groups, missing, unresolved = {}, [], []
    for model, suffix, code in rows:
        doc = index.get(model)
        if doc is None:
            missing.append((model, suffix))
            continue
        path, e = resolve(doc, suffix)
        if path is None:
            unresolved.append((model, suffix))
            continue
        system = systems.get(code)
        if not system:
            unresolved.append((model, "%s -> %s has no CodeSystem" % (suffix, code)))
            continue
        key = (doc.get("url") or model, system)
        groups.setdefault(key, {})[path] = {
            "code": path,
            "display": short_of(e) or path,
            "target": [{"code": code, "display": code,
                        "equivalence": EQUIVALENCE}],
        }

    out = []
    for (source, target), elements in sorted(groups.items()):
        out.append({"source": source, "target": target,
                    "element": [elements[p] for p in sorted(elements)]})
    return out, missing, unresolved


def previous(path):
    if not os.path.exists(path):
        return None
    try:
        return json.load(io.open(path, encoding="utf-8"))
    except ValueError:
        return None


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mappings", default=MAPPINGS)
    ap.add_argument("--models", default=MODELS,
                    help="folder of StructureDefinitions to resolve element paths "
                         "and canonicals against (default: input/models)")
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    sys.stdout.reconfigure(encoding="utf-8")
    mpath = args.mappings if os.path.isabs(args.mappings) else os.path.join(ROOT, args.mappings)
    mdir = args.models if os.path.isabs(args.models) else os.path.join(ROOT, args.models)
    out = args.out if os.path.isabs(args.out) else os.path.join(ROOT, args.out)

    rows, held = confirmed(mpath)
    index = index_models(mdir)
    systems = glossary_terms.systems()
    groups, missing, unresolved = build(rows, index, systems)

    n = sum(len(g["element"]) for g in groups)
    print("Confirmed  : %d mapping(s)" % len(rows))
    print("Mapped     : %d element(s) in %d group(s)" % (n, len(groups)))
    if held:
        print("Held back  : %d row(s) not pointing at an approved term" % len(held))
        for m, s, c, t in held[:5]:
            print("             %-26s %-20s %s (%s)" % (m, s, c, t))
    if missing:
        print("No model   : %d row(s)" % len(missing))
        for m, s in missing[:5]:
            print("             %-26s %s" % (m, s))
    if unresolved:
        print("No element : %d row(s)" % len(unresolved))
        for m, s in unresolved[:5]:
            print("             %-26s %s" % (m, s))

    doc = {
        "resourceType": "ConceptMap",
        "id": "model-to-glossary",
        "url": CANONICAL,
        "version": "1.0.0",
        "name": "ModelToGlossaryConceptMap",
        "title": "Logical model elements to Common Glossary concepts",
        "status": "active",
        "experimental": False,
        "date": time.strftime("%Y-%m-%d"),
        "description":
            "Maps elements of the Belgian CareSet logical models to the concepts "
            "of the Common Glossary. Kept as a ConceptMap rather than as "
            "element.code so that the StructureDefinitions remain exactly as "
            "published, and a change of mapping is not a change of model.",
        "purpose":
            "Lets a question about a concept be answered across every model at "
            "once - which elements mean Recorder, which models have none - and "
            "lets a rule about retention, consent or access be written against "
            "the concept rather than against each model's own field names.",
        "group": groups,
    }

    prior = previous(out)
    if prior:
        # The date says when the mapping last changed, so an unchanged rebuild
        # keeps the old one. Regenerating it on every build would otherwise put
        # a diff in the tree whenever anything else was rebuilt.
        comparable = dict(doc, date=prior.get("date"))
        if comparable == prior:
            doc["date"] = prior["date"]
            print("\nUnchanged since %s" % prior.get("date"))

    if args.dry_run:
        print("\n--dry-run: %s not written" % args.out)
        return 0

    os.makedirs(os.path.dirname(out), exist_ok=True)
    with io.open(out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print("\nWrote %s" % args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
