"""
Resolve the ValueSets the served models bind to, so the site can show their
names and link to the right page.

Every element binding in _resources/models/ names a ValueSet by canonical
(https://www.ehealth.fgov.be/standards/fhir/allergy/ValueSet/be-vs-... or
http://hl7.org/fhir/ValueSet/...). The canonical carries neither the name nor
a version: an HL7 core canonical resolves to whatever FHIR release is current
(R5 today), while the models are R4. So this script records, per canonical:

  _resources/valuesets.json   { canonical: {name, title, version, page, ...} }

  page   the URL to link to. For HL7 core ValueSets that is the page in the
         FHIR release the models declare (fhirVersion 4.0.x -> /fhir/R4/),
         never the unversioned canonical. For a publisher's own ValueSets it is
         the page the canonical resolves to when asked for HTML, which is the
         versioned page of the published guide.

The viewers load this once, show title (or name) instead of the URL's last
segment, and link to `page`; anything not listed falls back to the last
segment and the canonical.

Incremental: a canonical already in the index is not fetched again unless
--refresh is given. A canonical that cannot be resolved is reported and left
out; the build goes on, since a missing entry only costs a nicer label.

  python make_valueset_index.py             resolve what is new
  python make_valueset_index.py --refresh   re-fetch everything
  python make_valueset_index.py --dry-run   list the canonicals and stop
"""

import argparse
import collections
import glob
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
MODELS = os.path.join(ROOT, "_resources", "models")
INDEX = os.path.join(ROOT, "_resources", "valuesets.json")
TIMEOUT = 30
USER_AGENT = "caresets-glossary/1.0 (+https://github.com/caresets)"

HL7_CORE = re.compile(r"^https?://hl7\.org/fhir/ValueSet/([^/|]+)$")


def fhir_release(version):
    """The hl7.org path segment for a fhirVersion: 4.0.x -> R4, 4.3.x -> R4B,
    5.0.x -> R5, 3.0.x -> STU3. Unknown -> None (link the canonical)."""
    v = (version or "").strip()
    if v.startswith("4.0"):
        return "R4"
    if v.startswith("4.3"):
        return "R4B"
    if v.startswith("5.0"):
        return "R5"
    if v.startswith("3.0"):
        return "STU3"
    return None


def canonicals_in_use():
    """{canonical: {models, fhirVersions}} for every ValueSet any served model
    binds to. The |version suffix is not part of the identity."""
    used = {}
    for fn in sorted(glob.glob(os.path.join(MODELS, "**", "*.json"), recursive=True)):
        try:
            with io.open(fn, encoding="utf-8-sig") as fh:
                sd = json.load(fh)
        except (OSError, ValueError):
            continue
        if not isinstance(sd, dict) or sd.get("resourceType") != "StructureDefinition":
            continue
        for e in (sd.get("snapshot") or {}).get("element", []):
            vs = ((e.get("binding") or {}).get("valueSet") or "").split("|")[0].strip()
            if vs.startswith("http"):
                u = used.setdefault(vs, {"models": set(), "fhirVersions": collections.Counter(), "guides": set()})
                u["models"].add(sd.get("name") or sd.get("id"))
                u["fhirVersions"][sd.get("fhirVersion") or ""] += 1
                # the guide the model is published in: everything before /StructureDefinition/
                base = (sd.get("url") or "").split("/StructureDefinition/")[0]
                if base.startswith("http"):
                    u["guides"].add(base)
    return used


def get(url, accept):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": accept})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read(), r.geturl()


def candidates(canonical, guides):
    """Where to ask for a ValueSet. The canonical first; then the same id under
    each guide that binds it. A guide can declare a ValueSet with a canonical
    in another guide's namespace (.../terminology/ValueSet/BeMedicationTypeVS
    is defined in the medication package): the package resolves it, the
    browser does not, but the binding guide's own URL for it does."""
    out = [canonical]
    vs_id = canonical.rstrip("/").rsplit("/", 1)[-1]
    for base in sorted(guides or []):
        alt = "%s/ValueSet/%s" % (base, vs_id)
        if alt != canonical:
            out.append(alt)
    return out


def resolve(canonical, fhir_version, guides=None):
    """(ValueSet dict, json_url, page_url, resolved_via) for one canonical."""
    m = HL7_CORE.match(canonical)
    release = fhir_release(fhir_version)
    if m and release:
        # the release-specific copy, never the unversioned canonical
        vs_id = m.group(1)
        json_url = "http://hl7.org/fhir/%s/valueset-%s.json" % (release, vs_id)
        page = "http://hl7.org/fhir/%s/valueset-%s.html" % (release, vs_id)
        body, _ = get(json_url, "application/fhir+json, application/json;q=0.9")
        via = canonical
    else:
        last = None
        for url in candidates(canonical, guides):
            try:
                body, json_url = get(url, "application/fhir+json, application/json;q=0.9")
                via = url
                break
            except (urllib.error.URLError, urllib.error.HTTPError, OSError) as e:
                last = e
        else:
            raise last
        # the publisher's HTML rendering of the same resource, versioned
        try:
            _, page = get(via, "text/html")
        except (urllib.error.URLError, urllib.error.HTTPError, OSError):
            page = via
    data = json.loads(body.decode("utf-8-sig"))
    if not isinstance(data, dict) or data.get("resourceType") != "ValueSet":
        raise ValueError("not a ValueSet")
    return data, json_url, page, via


def load_index():
    if not os.path.exists(INDEX):
        return {}
    with io.open(INDEX, encoding="utf-8") as fh:
        return json.load(fh)


def save_index(index):
    os.makedirs(os.path.dirname(INDEX), exist_ok=True)
    with io.open(INDEX, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(dict(sorted(index.items())), fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--refresh", action="store_true", help="re-fetch canonicals already indexed")
    ap.add_argument("--dry-run", action="store_true", help="list the canonicals in use and stop")
    args = ap.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")

    used = canonicals_in_use()
    index = load_index()
    print("ValueSets bound by the served models: %d  (indexed so far: %d)" % (len(used), len(index)))
    if args.dry_run:
        for c, u in sorted(used.items()):
            print("  %-75s %s%s" % (c, ",".join(sorted(u["fhirVersions"])), "" if c in index else "   [not indexed]"))
        return 0

    fetched, failed = 0, []
    for canonical, u in sorted(used.items()):
        if canonical in index and not args.refresh:
            continue
        fhir_version = u["fhirVersions"].most_common(1)[0][0]
        try:
            vs, json_url, page, via = resolve(canonical, fhir_version, u["guides"])
        except (urllib.error.URLError, urllib.error.HTTPError, OSError, ValueError) as e:
            failed.append((canonical, "%s: %s" % (e.__class__.__name__, e)))
            print("  ! %-70s %s" % (canonical, e))
            continue
        index[canonical] = {
            "name": vs.get("name"),
            "title": vs.get("title"),
            "version": vs.get("version"),
            "status": vs.get("status"),
            "fhirVersion": fhir_version,
            "page": page,
            "source": json_url,
            "resolvedVia": via if via != canonical else None,
            "fetchedAt": time.strftime("%Y-%m-%dT%H:%M:%S"),
        }
        fetched += 1
        print("  %-70s %s%s" % (canonical, vs.get("title") or vs.get("name"),
                                 "" if via == canonical else "   [via %s]" % via.split("/fhir/")[-1].split("/ValueSet/")[0]))

    stale = [c for c in index if c not in used]
    for c in stale:
        del index[c]
    save_index(index)
    print("\n%d fetched, %d already indexed, %d stale dropped, %d failed -> %s"
          % (fetched, len(index) - fetched, len(stale), len(failed), os.path.relpath(INDEX, ROOT)))
    if failed:
        print("Unresolved (shown by their URL's last segment on the site):")
        for c, why in failed:
            print("  %s\n      %s" % (c, why))
    return 0


if __name__ == "__main__":
    sys.exit(main())
