"""
Generate diagrams and documents from the logical models (FHIR StructureDefinitions).

For each model, into exports/diagrams/ by default:

  <Name>.puml / .svg / .png        class notation as in modelgram: one box per model,
                                   elements as an indented tree, datatypes in <<guillemets>>
  <Name>-uml.puml / .svg / .png    classical UML as drawn in Enterprise Architect: one class
                                   per nested group, attributes as  +name : Type [0..1],
                                   composition links, generalisation to the parent
  <Name>-<lang>.xmi                UML 2.1 XMI for Enterprise Architect
                                   (Project > Import/Export > Import Model from XMI)
  <Name>-<lang>.docx               Word: metadata, description, the diagrams, element tables
  <Name>-<lang>.html               the same as a page you can copy-paste into Word / a wiki

Documents are written per language - en, fr and nl by default, --langs to change it.
The diagrams are not: they carry element names, datatypes and cardinalities, none of
which translate, so they are rendered once and shared by all three documents.

A language the models carry no translation extension for still produces a document; it
is simply the base text under that language's filename, and the run says so at the end
rather than leaving somebody to find out.

The parent model (baseDefinition) is drawn too, with a generalisation arrow, whenever it
is a real model rather than Base / Element - so a PatientSummary derived from Document
shows both classes.  The parent is resolved from the local model folders by canonical
URL, then by name, and otherwise fetched from the publisher
(<canonical base>/StructureDefinition-<Name>.json) and cached in imports/parents/.
Ancestors are followed recursively.

A model's elements are split into its own (drawn in the model's box) and the ones it
inherits (drawn in the parent's box).  An inherited element that the child constrains
again is repeated in the child in italics.

Text (short, definition, title, description) is taken in each language, falling back to
the base value when no translation extension exists for it.

Requires: python-docx (for .docx); java + plantuml.jar (for .svg/.png).  Without
PlantUML the .puml sources are still written and the docx just has no picture.

Usage:
  python generate_model_diagrams.py
  python generate_model_diagrams.py --model BeModelNursingPrescription BeModelPatient
  python generate_model_diagrams.py --lang fr --formats svg docx
  python generate_model_diagrams.py --langs en fr        # skip the Dutch documents
  python generate_model_diagrams.py --models-dir input/models --out exports/diagrams
  python generate_model_diagrams.py --plantuml c:/tools/plantuml.jar
"""

import argparse
import glob
import html
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
MODEL_DIRS = ["input/models", "_resources/models", "models"]
PARENT_CACHE = os.path.join(ROOT, "imports", "parents")
DEFAULT_OUT = os.path.join(ROOT, "exports", "diagrams")
PLANTUML_CANDIDATES = [
    os.environ.get("PLANTUML_JAR"),
    os.path.join(ROOT, "plantuml.jar"),
    r"c:\work\WHO\RAPublisher\plantuml.jar",
]
ALL_FORMATS = ["puml", "svg", "png", "xmi", "docx", "html"]

TRIVIAL_PARENTS = {"Base", "Element", "BackboneElement", "Resource", "DomainResource"}
NOISE = {"id", "extension", "modifierExtension"}
TRANSLATION = "http://hl7.org/fhir/StructureDefinition/translation"
FHIR_TYPE_EXT = "http://hl7.org/fhir/StructureDefinition/structuredefinition-fhir-type"
BG = "#B5E8F7"     # modelgram default: ArchiMate application-layer blue


# --------------------------------------------------------------------------- helpers

def warn(msg):
    print("  ! " + msg, file=sys.stderr)


def alias(name):
    return re.sub(r"\W", "_", name)


def last_segment(url):
    return url.split("|")[0].rstrip("/").split("/")[-1]


def text(obj, field, lang):
    """obj[field], or its translation extension for `lang` when there is one."""
    base = obj.get(field) or ""
    for ext in (obj.get("_" + field) or {}).get("extension", []):
        if ext.get("url") != TRANSLATION:
            continue
        code = content = None
        for sub in ext.get("extension", []):
            if sub.get("url") == "lang":
                code = sub.get("valueCode")
            elif sub.get("url") == "content":
                content = sub.get("valueString")
        if code == lang and content:
            return content
    return base


def type_name(t):
    code = t.get("code") or ""
    if code.startswith("http://hl7.org/fhirpath/System."):
        for ext in t.get("extension", []):
            if ext.get("url") == FHIR_TYPE_EXT and ext.get("valueUrl"):
                return ext["valueUrl"]
        return code.rsplit(".", 1)[-1].lower()
    if "/" in code:
        code = last_segment(code)
    if code == "Reference" and t.get("targetProfile"):
        return "Reference(" + " | ".join(last_segment(p) for p in t["targetProfile"]) + ")"
    return code


def types_of(el):
    if el.get("contentReference"):
        return "see " + el["contentReference"].split("#")[-1]
    return " | ".join(dict.fromkeys(type_name(t) for t in el.get("type", [])))


def card(el):
    return "%s..%s" % (el.get("min", 0), el.get("max", "1"))


def card_uml(el):
    mn, mx = str(el.get("min", 0)), str(el.get("max", "1"))
    return "[%s]" % mn if mn == mx else "[%s..%s]" % (mn, mx)


def binding_of(el):
    vs = (el.get("binding") or {}).get("valueSet") or ""
    return last_segment(vs) if vs else ""


# --------------------------------------------------------------------------- models

def load_models(dirs, include_draft):
    models = {}
    for d in dirs:
        patterns = [os.path.join(d, "*.json")]
        if include_draft:
            patterns.append(os.path.join(d, "draft", "*.json"))
        for pat in patterns:
            for fn in sorted(glob.glob(pat)):
                try:
                    with open(fn, encoding="utf-8") as fh:
                        sd = json.load(fh)
                except Exception as e:
                    warn("skipping %s: %s" % (fn, e))
                    continue
                if not isinstance(sd, dict) or sd.get("resourceType") != "StructureDefinition":
                    continue
                if sd.get("kind") != "logical":
                    continue
                name = sd.get("name") or sd.get("id")
                if name in models:
                    continue
                sd["_file"] = fn
                models[name] = sd
    return models


def elements(sd):
    src = (sd.get("snapshot") or sd.get("differential") or {}).get("element", [])
    return [e for e in src if "." in (e.get("path") or "")]


def rel(path):
    return path.split(".", 1)[1]


def is_noise(path):
    return path.split(".")[-1] in NOISE


class Elem:
    def __init__(self, el, lang, inherited):
        self.path = el["path"]
        self.rel = rel(self.path)
        parts = self.rel.split(".")
        self.depth = len(parts)
        self.name = parts[-1]
        if el.get("sliceName"):
            self.name += ":" + el["sliceName"]
        self.parent_rel = ".".join(parts[:-1])
        self.card = card(el)
        self.card_uml = card_uml(el)
        self.types = types_of(el)
        self.short = text(el, "short", lang)
        self.definition = text(el, "definition", lang)
        self.binding = binding_of(el)
        self.inherited = inherited
        self.has_children = False


def base_name(sd):
    return last_segment(sd.get("baseDefinition") or "")


def own_elements(sd, parent_sd, lang):
    """The elements to draw in this model's own box.

    With a resolved parent: everything not in the parent's element set, plus the
    inherited elements this model constrains again (marked inherited).  Without one,
    but with a non-trivial base: the differential.  Otherwise: everything."""
    els = [e for e in elements(sd) if not is_noise(e["path"])]
    if parent_sd is not None:
        parent_paths = {rel(e["path"]) for e in elements(parent_sd)}
        diff_paths = {rel(e["path"]) for e in (sd.get("differential") or {}).get("element", [])
                      if "." in (e.get("path") or "")}
        out = []
        for e in els:
            r = rel(e["path"])
            if r not in parent_paths:
                out.append(Elem(e, lang, False))
            elif r in diff_paths:
                out.append(Elem(e, lang, True))
    elif base_name(sd) not in TRIVIAL_PARENTS and sd.get("differential"):
        out = [Elem(e, lang, False) for e in (sd["differential"].get("element") or [])
               if "." in (e.get("path") or "") and not is_noise(e["path"])]
    else:
        out = [Elem(e, lang, False) for e in els]
    rels = {e.rel for e in out}
    out = [e for e in out if e.depth == 1 or e.parent_rel in rels]
    for e in out:
        e.has_children = any(o.parent_rel == e.rel for o in out)
    return out


# --------------------------------------------------------------------------- parents

def fetch_parent(url):
    """Try the publisher's <base>/StructureDefinition-<Name>.json; cache it."""
    canonical = url.split("|")[0]
    m = re.match(r"^(https?://.*)/StructureDefinition/([^/]+)$", canonical)
    if not m:
        return None
    base, name = m.group(1), m.group(2)
    os.makedirs(PARENT_CACHE, exist_ok=True)
    cache = os.path.join(PARENT_CACHE, "StructureDefinition-%s.json" % name)
    if os.path.exists(cache):
        with open(cache, encoding="utf-8") as fh:
            return json.load(fh)
    for candidate in ("%s/StructureDefinition-%s.json" % (base, name), canonical + ".json"):
        try:
            req = urllib.request.Request(candidate, headers={"Accept": "application/fhir+json, application/json"})
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            if data.get("resourceType") == "StructureDefinition":
                with open(cache, "w", encoding="utf-8") as fh:
                    json.dump(data, fh, indent=2, ensure_ascii=False)
                print("  fetched parent %s from %s" % (name, candidate))
                return data
        except Exception as e:
            warn("could not fetch %s: %s" % (candidate, e))
    return None


def resolve_parent(sd, models, by_url, allow_fetch):
    url = sd.get("baseDefinition") or ""
    name = last_segment(url)
    if not url or name in TRIVIAL_PARENTS:
        return None
    parent = by_url.get(url.split("|")[0]) or models.get(name)
    if parent is None and allow_fetch:
        parent = fetch_parent(url)
        if parent is not None:
            parent["_file"] = "(fetched)"
            models.setdefault(parent.get("name") or name, parent)
            by_url[parent.get("url", url)] = parent
    if parent is None:
        warn("%s: parent %s not found; drawing the differential only" % (sd["name"], name))
    return parent


def build_chain(sd, models, by_url, lang, allow_fetch):
    """[(sd, own elements), (parent, its own elements), ...] from the model up."""
    chain, seen = [], set()
    cur = sd
    while cur is not None and cur["name"] not in seen:
        seen.add(cur["name"])
        parent = resolve_parent(cur, models, by_url, allow_fetch)
        chain.append((cur, own_elements(cur, parent, lang)))
        cur = parent
    return chain


# --------------------------------------------------------------------------- PlantUML

def puml_tree(chain, datatypes=True):
    """modelgram class notation: one box per model, elements as a tree."""
    lines = ["@startuml",
             "skinparam ClassBackgroundColor " + BG,
             "skinparam linetype polyline",
             "hide circle",
             "hide stereotype",
             ""]
    for sd, elems in reversed(chain):
        lines.append('class "**%s**" as %s {' % (sd["name"], alias(sd["name"])))
        for e in elems:
            indent = "  " * (e.depth - 1)
            nm = "//%s//" % e.name if e.inherited else e.name
            ts = "   <<%s>>" % e.types if datatypes and e.types and not e.has_children else ""
            lines.append("%s|_ %s %s%s  " % (indent, nm, e.card, ts))
        lines += ["--", "}", ""]
    for (child, _), (parent, _) in zip(chain, chain[1:]):
        lines.append("%s <|-- %s" % (alias(parent["name"]), alias(child["name"])))
    lines.append("@enduml")
    return "\n".join(lines)


UML_HEAD = ["@startuml",
            "skinparam shadowing false",
            "skinparam classAttributeIconSize 0",
            "skinparam linetype ortho",
            "skinparam class {",
            "  BackgroundColor #FEFECE",
            "  BorderColor #000000",
            "  ArrowColor #000000",
            "  FontStyle bold",
            "  AttributeFontStyle normal",
            "}",
            "hide circle",
            "hide empty members",
            ""]


def elem_kind(e):
    """Which of the four box kinds an element is drawn as.

    rootconcept  a group that has children of its own - the model itself, and
                 any BackboneElement below it
    reference    a pointer at another resource, drawn apart from the data
    data         everything else: the fields that carry a value
    """
    if e.has_children:
        return "rootconcept"
    if (e.types or "").startswith("Reference"):
        return "reference"
    return "data"


def puml_boxes(chain):
    """The concept diagram: one box per element, arranged around the concept.

    Colour and stereotype carry the kind, as in the models drawn by hand for
    review - the concept in amber at the centre, its data elements in blue,
    references in grey, and each bound value set in green beside the element
    that binds it. Arrows run from an element into the concept it belongs to,
    labelled with the element's cardinality.

    A nested group is a concept in its own right, so a BackboneElement gets the
    amber treatment and its own children point at it rather than at the model.
    """
    lines = ["@startuml",
             # Ranks run left to right, so the elements stack beside the
             # concept instead of spreading along one row. With everything
             # pointing at a single node the default top-to-bottom layout puts
             # every element in one rank: 2385x260 for MedicationLine, against
             # 749x902 this way, which fits a page and can be read.
             "left to right direction",
             "skinparam shadowing false",
             "skinparam nodesep 10",
             "skinparam ranksep 40",
             "skinparam classAttributeIconSize 0",
             "skinparam class {",
             "  FontStyle italic",
             "  BackgroundColor<<rootconcept>> #FAC08F",
             "  BorderColor<<rootconcept>> #E36C0A",
             "  BackgroundColor<<data>> #B8CCE4",
             "  BorderColor<<data>> #4F81BD",
             "  BackgroundColor<<reference>> #D9D9D9",
             "  BorderColor<<reference>> #808080",
             "  BackgroundColor<<value set>> #C3D69B",
             "  BorderColor<<value set>> #77933C",
             "  ArrowColor #4F81BD",
             "}",
             "hide circle",
             "hide empty members",
             ""]
    links = []
    for sd, elems in reversed(chain):
        root = alias(sd["name"])
        lines.append('class "%s" as %s <<rootconcept>> {' % (sd["name"], root))
        lines += ["}", ""]

        known = {""}
        for e in elems:
            a = "%s_%s" % (root, alias(e.rel))
            known.add(e.rel)
            lines.append('class "%s" as %s <<%s>> {' % (e.name, a, elem_kind(e)))
            lines += ["}", ""]

            # The bound value set as a box of its own, beside the element that
            # binds it. Drawn per binding rather than once per value set: the
            # same list bound in two places is two statements about two
            # elements, and the hand-drawn models show it that way.
            if e.binding:
                vs = "%s_vs" % a
                lines.append('class "%s" as %s <<value set>> {' % (e.binding, vs))
                lines += ["}", ""]
                links.append("%s <-- %s" % (a, vs))

        for e in elems:
            a = "%s_%s" % (root, alias(e.rel))
            parent = root if not e.parent_rel or e.parent_rel not in known \
                else "%s_%s" % (root, alias(e.parent_rel))
            # Pointing inward, at the concept the element belongs to, with the
            # cardinality read off the element end.
            links.append('%s "%s" --> %s' % (a, e.card, parent))

    for (child, _), (parent, _) in zip(chain, chain[1:]):
        links.append("%s <|-- %s" % (alias(parent["name"]), alias(child["name"])))
    return "\n".join(lines + links + ["@enduml"])


def puml_uml(chain):
    """Classical UML class diagram, attributes folded into their group."""
    lines = list(UML_HEAD)
    links = []
    for sd, elems in reversed(chain):
        root = alias(sd["name"])
        groups = {"": (sd["name"], root)}
        for e in elems:
            if e.has_children:
                groups[e.rel] = (e.name, root + "_" + alias(e.rel))
        for grel, (gname, galias) in groups.items():
            title = sd["name"] if grel == "" else "%s.%s" % (sd["name"], grel)
            lines.append('class "%s" as %s {' % (title, galias))
            for e in elems:
                if e.parent_rel != grel:
                    continue
                nm = "//%s//" % e.name if e.inherited else e.name
                if e.has_children:
                    links.append('%s *-- "%s" %s : %s' % (galias, e.card, groups[e.rel][1], e.name))
                    continue
                lines.append("  +%s : %s %s" % (nm, e.types or "-", e.card_uml))
            lines += ["}", ""]
    for (child, _), (parent, _) in zip(chain, chain[1:]):
        links.append("%s <|-- %s" % (alias(parent["name"]), alias(child["name"])))
    lines += links + ["@enduml"]
    return "\n".join(lines)


def translation_counts(models, wanted):
    """How many translated short/definition texts each language actually has.

    Reported because a French document built from a model with no French in it
    is not wrong, just identical to the English one, and somebody handed it
    should know which they are looking at.
    """
    out, models_with = {}, {}
    for name in wanted:
        sd = models.get(name) or {}
        seen = set()
        for section in ("differential", "snapshot"):
            for e in (sd.get(section) or {}).get("element", []):
                for key in ("_short", "_definition"):
                    for ext in (e.get(key) or {}).get("extension", []):
                        code = None
                        for sub in ext.get("extension", []):
                            if sub.get("url") == "lang":
                                code = sub.get("valueCode")
                        if code:
                            out[code] = out.get(code, 0) + 1
                            seen.add(code)
        for code in seen:
            models_with[code] = models_with.get(code, 0) + 1
    return out, models_with


def find_plantuml(explicit):
    for c in [explicit] + PLANTUML_CANDIDATES:
        if c and os.path.exists(c):
            return c
    return None


def render(puml_files, fmt, jar):
    if not puml_files:
        return
    if jar is None or shutil.which("java") is None:
        warn("java or plantuml.jar not found; skipping ." + fmt)
        return
    cmd = ["java", "-Djava.awt.headless=true", "-jar", jar, "-charset", "UTF-8", "-t" + fmt] + puml_files
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        warn("plantuml -t%s failed: %s" % (fmt, (r.stderr or r.stdout).strip()[:500]))


# --------------------------------------------------------------------------- XMI (Enterprise Architect)

def xml_escape(s):
    return html.escape(str(s), quote=True)


def xmi_id(*parts):
    return "id_" + re.sub(r"[^A-Za-z0-9]", "_", "_".join(parts))


def xmi_ea(chain, lang):
    model = chain[0][0]
    pkg = xmi_id(model["name"], "pkg")
    datatypes = {}
    classes = []     # (id, name, doc, attrs, general_id)
    assocs = []
    generals = {c["name"]: xmi_id(p["name"]) for (c, _), (p, _) in zip(chain, chain[1:])}
    for sd, elems in reversed(chain):
        root_id = xmi_id(sd["name"])
        groups = {"": root_id}
        for e in elems:
            if e.has_children:
                groups[e.rel] = xmi_id(sd["name"], e.rel)
        for grel, gid in groups.items():
            gname = sd["name"] if grel == "" else grel.split(".")[-1]
            gdoc = text(sd, "description", lang) if grel == "" else ""
            attrs = []
            for e in elems:
                if e.parent_rel != grel:
                    continue
                aid = xmi_id(sd["name"], e.rel, "attr")
                if e.has_children:
                    attrs.append((aid, e, groups[e.rel], None))
                    assocs.append((aid, gid, groups[e.rel], e))
                else:
                    tid = datatypes.setdefault(e.types, xmi_id("type", e.types)) if e.types else None
                    attrs.append((aid, e, None, tid))
            classes.append((gid, gname, gdoc, attrs, generals.get(sd["name"]) if grel == "" else None))

    L = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<xmi:XMI xmi:version="2.1" xmlns:xmi="http://schema.omg.org/spec/XMI/2.1" '
         'xmlns:uml="http://schema.omg.org/spec/UML/2.1">',
         '  <xmi:Documentation exporter="generate_model_diagrams" exporterVersion="1.0"/>',
         '  <uml:Model xmi:type="uml:Model" xmi:id="%s" name="EA_Model" visibility="public">'
         % xmi_id(model["name"], "model"),
         '    <packagedElement xmi:type="uml:Package" xmi:id="%s" name="%s" visibility="public">'
         % (pkg, xml_escape(model["name"]))]
    ind = "      "
    for cid, cname, cdoc, attrs, general in classes:
        L.append('%s<packagedElement xmi:type="uml:Class" xmi:id="%s" name="%s" visibility="public">'
                 % (ind, cid, xml_escape(cname)))
        if cdoc:
            L.append('%s  <ownedComment xmi:type="uml:Comment" xmi:id="%s_doc" body="%s"/>' % (ind, cid, xml_escape(cdoc)))
        if general:
            L.append('%s  <generalization xmi:type="uml:Generalization" xmi:id="%s_gen" general="%s"/>' % (ind, cid, general))
        for aid, e, comp_id, tid in attrs:
            lo, hi = e.card.split("..")
            if comp_id:
                extra = ' type="%s" aggregation="composite"' % comp_id
            elif tid:
                extra = ' type="%s"' % tid
            else:
                extra = ""
            L.append('%s  <ownedAttribute xmi:type="uml:Property" xmi:id="%s" name="%s" visibility="public"%s>'
                     % (ind, aid, xml_escape(e.name), extra))
            L.append('%s    <lowerValue xmi:type="uml:LiteralInteger" xmi:id="%s_lo" value="%s"/>' % (ind, aid, lo))
            L.append('%s    <upperValue xmi:type="uml:LiteralUnlimitedNatural" xmi:id="%s_up" value="%s"/>' % (ind, aid, hi))
            doc = e.definition or e.short
            if e.binding:
                doc = (doc + " " if doc else "") + "[ValueSet: %s]" % e.binding
            if doc:
                L.append('%s    <ownedComment xmi:type="uml:Comment" xmi:id="%s_doc" body="%s"/>' % (ind, aid, xml_escape(doc)))
            L.append('%s  </ownedAttribute>' % ind)
        L.append('%s</packagedElement>' % ind)
    for aid, owner, target, e in assocs:
        end = aid + "_end"
        L.append('%s<packagedElement xmi:type="uml:Association" xmi:id="%s_assoc" memberEnd="%s %s">' % (ind, aid, aid, end))
        L.append('%s  <ownedEnd xmi:type="uml:Property" xmi:id="%s" type="%s" association="%s_assoc">' % (ind, end, owner, aid))
        L.append('%s    <lowerValue xmi:type="uml:LiteralInteger" xmi:id="%s_lo" value="1"/>' % (ind, end))
        L.append('%s    <upperValue xmi:type="uml:LiteralUnlimitedNatural" xmi:id="%s_up" value="1"/>' % (ind, end))
        L.append('%s  </ownedEnd>' % ind)
        L.append('%s</packagedElement>' % ind)
    L.append('    </packagedElement>')
    if datatypes:
        L.append('    <packagedElement xmi:type="uml:Package" xmi:id="%s" name="Data Types" visibility="public">'
                 % xmi_id(model["name"], "types"))
        for tname, tid in datatypes.items():
            L.append('      <packagedElement xmi:type="uml:DataType" xmi:id="%s" name="%s" visibility="public"/>'
                     % (tid, xml_escape(tname)))
        L.append('    </packagedElement>')
    L.append('  </uml:Model>')
    # a ready-made class diagram: classes on a grid, EA adds the connectors itself
    L.append('  <xmi:Extension extender="Enterprise Architect" extenderID="6.5">')
    L.append('    <diagrams><diagram xmi:id="%s">' % xmi_id(model["name"], "diagram"))
    L.append('      <model package="%s" owner="%s"/>' % (pkg, pkg))
    L.append('      <properties name="%s" type="Logical"/>' % xml_escape(model["name"] + " Class Diagram"))
    L.append('      <elements>')
    w, h, gx, gy, cols = 260, 200, 40, 80, 3
    for i, (cid, _, _, _, _) in enumerate(classes):
        left, top = 40 + (i % cols) * (w + gx), 40 + (i // cols) * (h + gy)
        L.append('        <element subject="%s" geometry="Left=%d;Top=%d;Right=%d;Bottom=%d;"/>'
                 % (cid, left, top, left + w, top + h))
    L.append('      </elements>')
    L.append('    </diagram></diagrams>')
    L.append('  </xmi:Extension>')
    L.append('</xmi:XMI>')
    return "\n".join(L)


# --------------------------------------------------------------------------- Word / HTML

def model_meta(sd, chain, lang):
    parent = chain[1][0]["name"] if len(chain) > 1 else (base_name(sd) or "-")
    return [("Name", sd.get("name", "")),
            ("Title", text(sd, "title", lang) or sd.get("name", "")),
            ("Canonical URL", sd.get("url", "")),
            ("Version", sd.get("version", "")),
            ("Status", sd.get("status", "")),
            ("Parent model", parent),
            ("Publisher", sd.get("publisher", ""))]


HEADERS = ("Element", "Card.", "Type", "Value set", "Description")


# A page with the default Word margins, less a little for the heading above
# the picture.
PAGE_W_IN = 6.3
PAGE_H_IN = 8.2


def png_size(path):
    """(width, height) in pixels, from the PNG header."""
    with open(path, "rb") as fh:
        head = fh.read(33)
    if len(head) < 24 or head[1:4] != b"PNG":
        return None
    import struct
    return struct.unpack(">II", head[16:24])


def fit_width(path, max_w=PAGE_W_IN, max_h=PAGE_H_IN):
    """The width to place a picture at so the whole of it lands on one page.

    Setting only a width scales the height with it, which is fine for a
    landscape picture and ruinous for a tall one: these diagrams rank top to
    bottom, so BeModelClinicalReport at 6.3in wide came out 13.8in tall and ran
    off the end of the page. Constraining both keeps the aspect ratio and puts
    the whole diagram where it can be seen.
    """
    size = png_size(path)
    if not size or not size[1]:
        return max_w
    w, h = size
    return min(max_w, max_h * w / float(h))


def write_docx(sd, chain, png, out, lang, uml_png=None):
    try:
        from docx import Document
        from docx.shared import Inches, Pt
    except ImportError:
        warn("python-docx not installed (pip install python-docx); skipping .docx")
        return False
    doc = Document()
    doc.add_heading(text(sd, "title", lang) or sd["name"], 0)
    t = doc.add_table(rows=0, cols=2)
    t.style = "Table Grid"
    for k, v in model_meta(sd, chain, lang):
        row = t.add_row().cells
        row[0].paragraphs[0].add_run(k).bold = True
        row[1].text = v
    desc = text(sd, "description", lang)
    if desc:
        doc.add_paragraph()
        doc.add_paragraph(desc)
    # The class diagram first: it is the one a reader coming from Enterprise
    # Architect recognises, and the one being asked for when someone asks to
    # see the model. The element tables follow it, never precede it.
    if uml_png and os.path.exists(uml_png):
        doc.add_heading("Class diagram", 1)
        doc.add_picture(uml_png, width=Inches(fit_width(uml_png)))
    if png and os.path.exists(png):
        doc.add_heading("Structure", 1)
        doc.add_picture(png, width=Inches(fit_width(png)))
    for i, (csd, elems) in enumerate(chain):
        doc.add_heading("Elements" if i == 0 else "Inherited from %s" % csd["name"], 1)
        table = doc.add_table(rows=1, cols=len(HEADERS))
        table.style = "Table Grid"
        for cell, head in zip(table.rows[0].cells, HEADERS):
            cell.paragraphs[0].add_run(head).bold = True
        for e in elems:
            cells = table.add_row().cells
            p = cells[0].paragraphs[0]
            run = p.add_run(e.name)
            run.bold = e.has_children
            run.italic = e.inherited
            p.paragraph_format.left_indent = Inches(0.15 * (e.depth - 1))
            cells[1].text = e.card
            cells[2].text = "" if e.has_children else e.types
            cells[3].text = e.binding
            cells[4].text = e.short or e.definition
            if e.definition and e.definition != e.short:
                para = cells[4].add_paragraph(e.definition)
                for r in para.runs:
                    r.font.size = Pt(8)
    doc.save(out)
    return True


def write_html(sd, chain, svg, out, lang):
    esc = html.escape
    H = ["<!doctype html><html><head><meta charset='utf-8'><title>%s</title>" % esc(sd["name"]),
         "<style>body{font-family:Calibri,Arial,sans-serif;max-width:1000px;margin:2em auto}"
         "table{border-collapse:collapse;width:100%}td,th{border:1px solid #999;padding:4px 6px;vertical-align:top}"
         "th{background:#eee;text-align:left}td.n{white-space:nowrap}.d{color:#555;font-size:90%}</style></head><body>",
         "<h1>%s</h1>" % esc(text(sd, "title", lang) or sd["name"]),
         "<table>"]
    for k, v in model_meta(sd, chain, lang):
        H.append("<tr><th>%s</th><td>%s</td></tr>" % (esc(k), esc(v)))
    H.append("</table>")
    desc = text(sd, "description", lang)
    if desc:
        H.append("<p>%s</p>" % esc(desc))
    if svg and os.path.exists(svg):
        with open(svg, encoding="utf-8") as fh:
            H.append("<h2>Diagram</h2>" + fh.read())
    for i, (csd, elems) in enumerate(chain):
        H.append("<h2>%s</h2>" % ("Elements" if i == 0 else "Inherited from %s" % esc(csd["name"])))
        H.append("<table><tr>" + "".join("<th>%s</th>" % h for h in HEADERS) + "</tr>")
        for e in elems:
            nm = esc(e.name)
            if e.has_children:
                nm = "<b>%s</b>" % nm
            if e.inherited:
                nm = "<i>%s</i>" % nm
            d = esc(e.short or e.definition)
            if e.definition and e.definition != e.short:
                d += "<div class='d'>%s</div>" % esc(e.definition)
            H.append("<tr><td class='n' style='padding-left:%dpx'>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
                     % (6 + 18 * (e.depth - 1), nm, e.card, "" if e.has_children else esc(e.types), esc(e.binding), d))
        H.append("</table>")
    H.append("</body></html>")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(H))


# --------------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--model", nargs="*", help="model names (default: all)")
    ap.add_argument("--models-dir", nargs="*",
                    help="folders with StructureDefinition JSON (default: %s)" % ", ".join(MODEL_DIRS))
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--base-lang", dest="base_lang", default="en",
                    help="the language the models are written in, which needs "
                         "no translation extension (default: en)")
    ap.add_argument("--langs", nargs="+", default=["en", "fr", "nl"],
                    metavar="LANG",
                    help="languages to write the documents in (default: en fr "
                         "nl). One .docx, .html and .xmi per language, suffixed "
                         "-<lang>. The diagrams carry element names and types "
                         "only, so they are rendered once and shared")
    # No default: --langs supplies the list, and a default here would silently
    # override it and always produce English only.
    ap.add_argument("--lang", default=None,
                    help="shorthand for a single language, e.g. --lang fr. "
                         "Overrides --langs")
    ap.add_argument("--formats", nargs="*", default=ALL_FORMATS, choices=ALL_FORMATS)
    ap.add_argument("--include-draft", action="store_true", help="also the draft/ subfolders")
    ap.add_argument("--no-fetch", action="store_true", help="never download a missing parent")
    ap.add_argument("--no-datatypes", action="store_true",
                    help="leave the <<datatypes>> out of the class-notation diagram")
    ap.add_argument("--uml-style", dest="uml_style",
                    choices=["boxes", "attributes"], default="boxes",
                    help="boxes: one box per element, related to the box it "
                         "hangs from - the shape a data model is reviewed in. "
                         "attributes: leaf elements folded into their parent "
                         "box as +name : Type [0..1], so only groups get a box "
                         "(default: boxes)")
    ap.add_argument("--plantuml", help="path to plantuml.jar (or set PLANTUML_JAR)")
    args = ap.parse_args()

    dirs = args.models_dir or [os.path.join(ROOT, d) for d in MODEL_DIRS if os.path.isdir(os.path.join(ROOT, d))]
    if not dirs:
        sys.exit("no model folder found; pass --models-dir")
    models = load_models(dirs, args.include_draft)
    if not models:
        sys.exit("no logical models found in " + ", ".join(dirs))
    by_url = {sd.get("url", "").split("|")[0]: sd for sd in models.values()}
    wanted = args.model or sorted(models)
    missing = [m for m in wanted if m not in models]
    if missing:
        sys.exit("unknown model(s): %s\nknown: %s" % (", ".join(missing), ", ".join(sorted(models))))

    os.makedirs(args.out, exist_ok=True)
    fmts = set(args.formats)
    jar = find_plantuml(args.plantuml)
    puml_paths = []
    chains = {}

    # --lang stays as the single-language shorthand it was.
    langs = [args.lang] if args.lang else list(args.langs)

    print("models: %s\nout:    %s\nlangs:  %s"
          % (", ".join(dirs), args.out, " ".join(langs)))
    for name in wanted:
        sd = models[name]
        # One chain per language: an Elem carries the short and definition text
        # resolved for that language, falling back to the base value where no
        # translation extension exists.
        chain = {l: build_chain(sd, models, by_url, l, not args.no_fetch)
                 for l in langs}
        chains[name] = chain
        first = chain[langs[0]]
        parents = " <- ".join(c[0]["name"] for c in first[1:])
        print("- %s%s" % (name, ("  (parent: %s)" % parents) if parents else ""))
        base = os.path.join(args.out, name)
        # The diagrams hold element names, datatypes and cardinalities, none of
        # which translate, so they are built once rather than once per language.
        p1, p2 = base + ".puml", base + "-uml.puml"
        with open(p1, "w", encoding="utf-8") as fh:
            fh.write(puml_tree(first, datatypes=not args.no_datatypes))
        with open(p2, "w", encoding="utf-8") as fh:
            fh.write((puml_boxes if args.uml_style == "boxes" else puml_uml)(first))
        puml_paths += [p1, p2]
        if "xmi" in fmts:
            for l in langs:
                with open("%s-%s.xmi" % (base, l), "w", encoding="utf-8") as fh:
                    fh.write(xmi_ea(chain[l], l))

    if fmts & {"svg", "html"}:
        render(puml_paths, "svg", jar)
    if fmts & {"png", "docx"}:
        render(puml_paths, "png", jar)

    for name in wanted:
        base = os.path.join(args.out, name)
        for l in langs:
            chain = chains[name][l]
            if "docx" in fmts:
                write_docx(models[name], chain, base + ".png",
                           "%s-%s.docx" % (base, l), l, base + "-uml.png")
            if "html" in fmts:
                write_html(models[name], chain, base + ".svg",
                           "%s-%s.html" % (base, l), l)
    if "puml" not in fmts:
        for p in puml_paths:
            os.remove(p)
    print("done: %d model(s) x %d language(s)" % (len(wanted), len(langs)))
    if len(langs) > 1:
        # A document in a language the models do not carry is not wrong, it is
        # just the base text under another filename - and somebody handed it
        # would have no way to tell. Say which languages are real.
        have, models_with = translation_counts(models, wanted)
        for l in langs:
            if l == args.base_lang:
                print("  %-3s the base language of these models" % l)
                continue
            n, m = have.get(l, 0), models_with.get(l, 0)
            if n:
                print("  %-3s %d translated text(s), in %d of %d model(s); the "
                      "rest falls back to %s"
                      % (l, n, m, len(wanted), args.base_lang))
            else:
                print("  %-3s NO translations in these models - the document is "
                      "the %s text under an %s filename"
                      % (l, args.base_lang, l))


if __name__ == "__main__":
    main()
