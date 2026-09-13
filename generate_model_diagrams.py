"""
Generate diagrams and documents from the logical models (FHIR StructureDefinitions).

For each model, into exports/diagrams/ by default:

  <Name>.puml / .svg / .png        class notation as in modelgram: one box per model,
                                   elements as an indented tree, datatypes in <<guillemets>>
  <Name>-uml.puml / .svg / .png    classical UML as drawn in Enterprise Architect: one class
                                   per nested group, attributes as  +name : Type [0..1],
                                   composition links, generalisation to the parent
  <Name>.xmi                       UML 2.1 XMI for Enterprise Architect
                                   (Project > Import/Export > Import Model from XMI)
  <Name>.docx                      Word: metadata, description, the diagram, element tables
  <Name>.html                      the same as a page you can copy-paste into Word / a wiki

The parent model (baseDefinition) is drawn too, with a generalisation arrow, whenever it
is a real model rather than Base / Element - so a PatientSummary derived from Document
shows both classes.  The parent is resolved from the local model folders by canonical
URL, then by name, and otherwise fetched from the publisher
(<canonical base>/StructureDefinition-<Name>.json) and cached in imports/parents/.
Ancestors are followed recursively.

A model's elements are split into its own (drawn in the model's box) and the ones it
inherits (drawn in the parent's box).  An inherited element that the child constrains
again is repeated in the child in italics.

Text (short, definition, title, description) is taken in --lang, falling back to the
base value when no translation extension exists for that language.

Requires: python-docx (for .docx); java + plantuml.jar (for .svg/.png).  Without
PlantUML the .puml sources are still written and the docx just has no picture.

Usage:
  python generate_model_diagrams.py
  python generate_model_diagrams.py --model BeModelNursingPrescription BeModelPatient
  python generate_model_diagrams.py --lang fr --formats svg docx
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


def puml_uml(chain):
    """Classical UML class diagram, Enterprise Architect look."""
    lines = ["@startuml",
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
        doc.add_picture(uml_png, width=Inches(6.3))
    if png and os.path.exists(png):
        doc.add_heading("Structure", 1)
        doc.add_picture(png, width=Inches(6.3))
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
    ap.add_argument("--lang", default="en")
    ap.add_argument("--formats", nargs="*", default=ALL_FORMATS, choices=ALL_FORMATS)
    ap.add_argument("--include-draft", action="store_true", help="also the draft/ subfolders")
    ap.add_argument("--no-fetch", action="store_true", help="never download a missing parent")
    ap.add_argument("--no-datatypes", action="store_true",
                    help="leave the <<datatypes>> out of the class-notation diagram")
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

    print("models: %s\nout:    %s" % (", ".join(dirs), args.out))
    for name in wanted:
        sd = models[name]
        chain = build_chain(sd, models, by_url, args.lang, not args.no_fetch)
        chains[name] = chain
        parents = " <- ".join(c[0]["name"] for c in chain[1:])
        print("- %s%s" % (name, ("  (parent: %s)" % parents) if parents else ""))
        base = os.path.join(args.out, name)
        p1, p2 = base + ".puml", base + "-uml.puml"
        with open(p1, "w", encoding="utf-8") as fh:
            fh.write(puml_tree(chain, datatypes=not args.no_datatypes))
        with open(p2, "w", encoding="utf-8") as fh:
            fh.write(puml_uml(chain))
        puml_paths += [p1, p2]
        if "xmi" in fmts:
            with open(base + ".xmi", "w", encoding="utf-8") as fh:
                fh.write(xmi_ea(chain, args.lang))

    if fmts & {"svg", "html"}:
        render(puml_paths, "svg", jar)
    if fmts & {"png", "docx"}:
        render(puml_paths, "png", jar)

    for name in wanted:
        base = os.path.join(args.out, name)
        if "docx" in fmts:
            write_docx(models[name], chains[name], base + ".png", base + ".docx",
                       args.lang, base + "-uml.png")
        if "html" in fmts:
            write_html(models[name], chains[name], base + ".svg", base + ".html", args.lang)
    if "puml" not in fmts:
        for p in puml_paths:
            os.remove(p)
    print("done: %d model(s)" % len(wanted))


if __name__ == "__main__":
    main()
