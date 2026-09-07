"""
Generate FSH ConceptMaps, one per implementation guide, for onboarding.

`make_conceptmap.py` builds a single ConceptMap for this site. That one cannot
be handed to eHealth, because the mapped models come from thirteen different
implementation guides and each guide publishes only its own. This splits the
same confirmed mappings by source guide and emits, for each:

  <ig>/ConceptMap-<Ig>ModelToGlossary.fsh   the ConceptMap, as FSH
  <ig>/map-<ig>-glossary.xml                the display page
  <ig>/sushi-config-pages.yaml              the `pages:` fragment to merge

FSH rather than a ConceptMap JSON dropped into input/resources/, because the
eHealth guides are sushi projects: a JSON resource is a foreign object in a
workflow where everything else is authored and reviewed as FSH.

The display page is generated from the same rows as the ConceptMap. In the
HL7 Europe proof of concept (hl7-eu/base, branch `mappings`) the FSH and the
XHTML table are separate hand-maintained artefacts - fourteen display pages
against one ConceptMap - and they have already drifted. Generating both from
one source is the point of doing this with a script at all.

Note on FSH RuleSets: the HL7 Europe PoC passes displays as unquoted RuleSet
arguments, which are comma-separated, so any description containing a comma
would be split into the wrong parameters. Glossary and element descriptions are
full of commas, so this writes plain FSH with quoted strings instead.

  python make_conceptmap_fsh.py --dry-run
  python make_conceptmap_fsh.py
  python make_conceptmap_fsh.py --ig drp medication
  python make_conceptmap_fsh.py --r5        # relationship, not equivalence
"""

import argparse
import csv
import glob
import io
import json
import os
import re
import sys
import time

import glossary_terms

ROOT = os.path.dirname(os.path.abspath(__file__))
MAPPINGS = os.path.join("input", "glossary_mappings.csv")
MODELS = os.path.join("input", "models")
INDEX = os.path.join("imports", "ehealth-models", "index.json")
OUT = os.path.join("exports", "conceptmaps")

UNKNOWN_IG = "unpublished"
# R4 spells this `equivalence` on the target, with a value from
# ConceptMapEquivalence. R5 renamed it `relationship`, with a different and
# smaller value set. The models are 4.0.1, so R4 is the default; --r5 switches
# both the property name and the value.
R4_REL = ("equivalence", "equivalent")
R5_REL = ("relationship", "equivalent")


def confirmed(path):
    """Confirmed rows whose target is an approved glossary term."""
    terms = glossary_terms.load()
    drafted = glossary_terms.workbook_terms()
    rows = []
    for r in csv.DictReader(io.open(path, encoding="utf-8-sig", newline=""),
                            delimiter=";"):
        model = (r.get("Model") or "").strip()
        suffix = (r.get("ElementSuffix") or "").strip()
        code = (r.get("GlossaryCode") or "").strip()
        if not (model and suffix and code):
            continue
        if (r.get("Status") or "confirmed").strip().lower() != "confirmed":
            continue
        if glossary_terms.status_of(code, terms, drafted) != "approved":
            continue
        rows.append((model, suffix, code))
    return rows


def load_models(models_dir):
    index = {}
    for path in sorted(glob.glob(os.path.join(models_dir, "**", "*.json"),
                                 recursive=True)):
        try:
            doc = json.load(io.open(path, encoding="utf-8"))
        except ValueError:
            continue
        if doc.get("resourceType") == "StructureDefinition":
            for key in (doc.get("name"), doc.get("id"), doc.get("url")):
                if key:
                    index.setdefault(key, doc)
    return index


def load_guides(path):
    """model name -> the guide that publishes it, from the fetch index.

    A model absent from the index was never fetched from a published guide -
    the drafts - and is grouped separately rather than guessed at.
    """
    if not os.path.exists(path):
        return {}
    try:
        doc = json.load(io.open(path, encoding="utf-8"))
    except ValueError:
        return {}
    return {m["name"]: m.get("guide") or UNKNOWN_IG
            for m in doc.get("models", []) if m.get("name")}


def resolve(doc, suffix):
    """The real ElementDefinition for a mapping row. Paths are read from the
    model, never assembled: an element's path is not always the model's name."""
    seen = set()
    for section in ("differential", "snapshot"):
        for e in doc.get(section, {}).get("element", []):
            p = e.get("path") or e.get("id")
            if not p or p in seen:
                continue
            seen.add(p)
            below = p.split(".", 1)[1] if "." in p else ""
            if below == suffix or below.endswith("." + suffix):
                return p, e
    return None, None


def fsh_string(s):
    """A double-quoted FSH string. FSH escapes with a backslash."""
    s = re.sub(r"\s+", " ", str(s or "")).strip()
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def pascal(s):
    return "".join(w[:1].upper() + w[1:] for w in re.split(r"[^A-Za-z0-9]+", s) if w)


def build_fsh(ig, entries, systems, rel_field, rel_value, canonical_base):
    """One ConceptMap per guide, grouped by (model, glossary CodeSystem)."""
    name = "%sModelToGlossary" % pascal(ig)
    groups = {}
    for model_url, path, display, code in entries:
        groups.setdefault((model_url, systems[code]), []).append((path, display, code))

    out = []
    out.append("// Generated by make_conceptmap_fsh.py - do not edit by hand.")
    out.append("// Source: input/glossary_mappings.csv (confirmed rows only).")
    out.append("// Regenerate rather than patching: the display page beside this")
    out.append("// file is generated from the same rows and must agree with it.")
    out.append("")
    out.append("Instance: %s" % name)
    out.append("InstanceOf: ConceptMap")
    out.append("Usage: #definition")
    # The maturity level, machine-readable. Its context of use is any artifact,
    # so it is valid here, and a receiving guide can render it without reading
    # the copyright text.
    out.append('* extension[+].url = '
               '"http://hl7.org/fhir/StructureDefinition/structuredefinition-fmm"')
    out.append("* extension[=].valueInteger = 1")
    out.append('* url = "%s/ConceptMap/%s"' % (canonical_base.rstrip("/"), name))
    out.append("* name = %s" % fsh_string(name))
    out.append("* title = %s" % fsh_string(
        "%s logical model elements to Common Glossary concepts" % ig))
    # active is the resource's own lifecycle, not a governance sign-off, and
    # experimental would say this was authored for testing rather than for
    # genuine use. The maturity signal is the version, which the receiving
    # guide sets.
    out.append("* status = #active")
    out.append("* experimental = false")
    out.append("* date = \"%s\"" % time.strftime("%Y-%m-%d"))
    out.append("* copyright = %s" % fsh_string(
        "First public release - agreed by the editors and open for review. The "
        "mapping is informative: the logical models are published as released and "
        "are unchanged by it. Coverage will be extended and individual mappings "
        "may be revised as review progresses."))
    out.append("* description = %s" % fsh_string(
        "Maps elements of the %s logical models to the concepts of the Belgian "
        "Common Glossary. Published as a ConceptMap so the StructureDefinitions "
        "remain exactly as released and a change of mapping is not a change of "
        "model." % ig))
    out.append("")

    for (model_url, target_system), rows in sorted(groups.items()):
        out.append("* group[+]")
        out.append('  * source = "%s"' % model_url)
        out.append('  * target = "%s"' % target_system)
        for path, display, code in sorted(rows):
            out.append("  * element[+]")
            out.append("    * code = #%s" % path)
            out.append("    * display = %s" % fsh_string(display or path))
            out.append("    * target[+]")
            out.append("      * code = #%s" % code)
            out.append("      * display = %s" % fsh_string(code))
            out.append("      * %s = #%s" % (rel_field, rel_value))
        out.append("")
    return name, "\n".join(out).rstrip() + "\n"


def build_page(ig, entries, glossary_base):
    """The display page, in the shape the HL7 Europe PoC uses: an XHTML table
    the IG publisher includes verbatim."""
    by_model = {}
    for model_name, path, display, code in entries:
        by_model.setdefault(model_name, []).append((path, display, code))

    o = []
    o.append('<?xml version="1.0" encoding="UTF-8"?>')
    o.append('<html xmlns="http://www.w3.org/1999/xhtml" lang="en">')
    o.append("  <head>")
    o.append('    <meta http-equiv="Content-Type" '
             'content="application/xhtml+xml; charset=UTF-8" />')
    o.append("    <title>%s model elements &#8594; Common Glossary</title>" % ig)
    o.append("  </head>")
    o.append("  <body>")
    o.append("    <h3>%s model elements &#8594; Common Glossary</h3>" % ig)
    # The caution goes at the top of the page, not the bottom. This page ends
    # up in someone else's repository and is read by people who did not see
    # where it came from.
    o.append('    <blockquote class="dragon">')
    o.append("      <p><strong>First public release - agreed by the editors and "
             "open for review.</strong> The mapping is "
             "<strong>informative</strong>: the logical models are published as "
             "released and are unchanged by it. Coverage will be extended and "
             "individual mappings may be revised as review progresses.</p>")
    o.append("    </blockquote>")
    o.append("    <p>Each element below is mapped to a concept of the Belgian "
             "Common Glossary. The mapping is published as a ConceptMap, not "
             "written into the StructureDefinitions, so the models are "
             "unchanged from their release.</p>")
    o.append("    <p>This page is generated from the same source as the "
             "ConceptMap; do not edit it by hand.</p>")
    for model in sorted(by_model):
        rows = sorted(by_model[model])
        o.append('    <div class="table-wrap">')
        o.append("      <table>")
        o.append("        <caption>%s</caption>" % model)
        o.append("        <thead><tr>"
                 "<th>Element</th><th>Description</th>"
                 "<th>Relation</th><th>Glossary concept</th>"
                 "</tr></thead>")
        o.append("        <tbody>")
        for path, display, code in rows:
            url = "%s#%s" % (glossary_base.rstrip("/"), code)
            o.append("          <tr>"
                     "<td>%s</td><td>%s</td><td>equivalent</td>"
                     '<td><a href="%s">%s</a></td></tr>'
                     % (esc(path), esc(display), esc(url), esc(code)))
        o.append("        </tbody>")
        o.append("      </table>")
        o.append("    </div>")
    o.append("  </body>")
    o.append("</html>")
    return "\n".join(o) + "\n"


def esc(s):
    return (str(s or "").replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mappings", default=MAPPINGS)
    ap.add_argument("--models", default=MODELS)
    ap.add_argument("--index", default=INDEX,
                    help="the fetch index that says which guide publishes which "
                         "model (default: imports/ehealth-models/index.json)")
    ap.add_argument("--out-dir", dest="out_dir", default=OUT)
    ap.add_argument("--ig", nargs="+", metavar="SLUG", help="only these guides")
    ap.add_argument("--canonical-base", default="http://example.org",
                    help="canonical base for the generated ConceptMap urls; "
                         "replace with the real eHealth or RIZIV base")
    ap.add_argument("--glossary-base", default="https://caresets.github.io/en/glossary_clinical.html",
                    help="page the display table links a concept to")
    ap.add_argument("--r5", action="store_true",
                    help="emit `relationship` instead of R4's `equivalence`")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    sys.stdout.reconfigure(encoding="utf-8")
    p = lambda x: x if os.path.isabs(x) else os.path.join(ROOT, x)

    rows = confirmed(p(args.mappings))
    models = load_models(p(args.models))
    guides = load_guides(p(args.index))
    systems = glossary_terms.systems()
    rel_field, rel_value = R5_REL if args.r5 else R4_REL

    by_ig, unresolved = {}, []
    for model, suffix, code in rows:
        doc = models.get(model)
        if doc is None:
            unresolved.append((model, suffix, "no model"))
            continue
        path, e = resolve(doc, suffix)
        if path is None:
            unresolved.append((model, suffix, "no element"))
            continue
        if code not in systems:
            unresolved.append((model, suffix, "%s in no CodeSystem" % code))
            continue
        ig = guides.get(model, UNKNOWN_IG)
        display = e.get("short") or e.get("definition") or path
        by_ig.setdefault(ig, []).append(
            (doc.get("url") or model, model, path, display, code))

    if args.ig:
        want = set(args.ig)
        by_ig = {k: v for k, v in by_ig.items() if k in want}

    print("Confirmed  : %d mapping(s)" % len(rows))
    print("Guides     : %d" % len(by_ig))
    if unresolved:
        print("Unresolved : %d" % len(unresolved))
        for m, s, why in unresolved[:5]:
            print("             %-26s %-20s %s" % (m, s, why))

    out_root = p(args.out_dir)
    for ig in sorted(by_ig):
        entries = by_ig[ig]
        fsh_entries = [(url, path, display, code)
                       for url, _model, path, display, code in entries]
        page_entries = [(model, path, display, code)
                        for _url, model, path, display, code in entries]
        name, fsh = build_fsh(ig, fsh_entries, systems, rel_field, rel_value,
                              args.canonical_base)
        page = build_page(ig, page_entries, args.glossary_base)
        page_name = "map-%s-glossary" % ig
        pages_yaml = ("# Merge into sushi-config.yaml, under `pages:`\n"
                      "  %s.html:\n"
                      "    title: %s model elements to Common Glossary\n"
                      % (page_name, ig))

        n_models = len({m for _u, m, _p, _d, _c in entries})
        print("  %-22s %3d mapping(s)  %2d model(s)  ->  %s.fsh"
              % (ig, len(entries), n_models, "ConceptMap-" + name))
        if args.dry_run:
            continue
        d = os.path.join(out_root, ig)
        os.makedirs(d, exist_ok=True)
        io.open(os.path.join(d, "ConceptMap-%s.fsh" % name), "w",
                encoding="utf-8", newline="\n").write(fsh)
        io.open(os.path.join(d, "%s.xml" % page_name), "w",
                encoding="utf-8", newline="\n").write(page)
        io.open(os.path.join(d, "sushi-config-pages.yaml"), "w",
                encoding="utf-8", newline="\n").write(pages_yaml)

    if args.dry_run:
        print("\n--dry-run: nothing written")
        return 0
    print("\nWrote %d guide folder(s) into %s" % (len(by_ig), args.out_dir))
    print("Each holds: the .fsh for input/fsh/maps/, the .xml for "
          "input/pagecontent/,\nand the pages: fragment to merge into that "
          "guide's sushi-config.yaml.")
    if args.canonical_base == "http://example.org":
        print("\n! Canonicals are http://example.org - pass --canonical-base "
              "with the real one\n  before handing these to a guide.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
