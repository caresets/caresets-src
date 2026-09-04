"""
Fetch every logical model published by eHealth Belgium.

Discovery follows the standard FHIR publication chain, so nothing is hardcoded
except the publisher's hostname:

  FHIR IG registry            which implementation guides exist, and their canonicals
        |                     https://github.com/FHIR/ig-registry
        v
  <canonical>/package-list.json    the released versions of one guide
        |
        v
  <version path>/package.tgz       the published package
        |
        v
  StructureDefinitions with kind = logical  ->  imports/ehealth-models/

This is the heavier, occasional import - roughly every two to four weeks - as
against import_models_zip.py, which takes a zip somebody hands you. The output
is the same shape, so the two are interchangeable:

  python fetch_ehealth_models.py            # download, report what changed
  python fetch_ehealth_models.py --apply    # and import into input/models/

Downloaded packages are cached under imports/ehealth-cache/ and skipped on the
next run unless the published version changed, so a re-run is cheap and mostly
offline.

Usage:
  python fetch_ehealth_models.py --dry-run
  python fetch_ehealth_models.py
  python fetch_ehealth_models.py --apply
  python fetch_ehealth_models.py --ig core-clinical medication
"""

import argparse
import io
import json
import os
import shutil
import subprocess
import sys
import tarfile
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
REGISTRY = "https://raw.githubusercontent.com/FHIR/ig-registry/master/fhir-ig-list.json"
PUBLISHER_HOST = "www.ehealth.fgov.be"
# A publisher may serve its own index of everything it publishes. It is the
# better source when it exists - authoritative, and it names the latest version
# directly, so the per-guide package-list.json fetches are not needed. eHealth
# does not serve one today, so the FHIR IG registry remains the fallback.
PUBLISHER_REGISTRY = "https://www.ehealth.fgov.be/standards/fhir/package-registry.json"
CACHE = os.path.join("imports", "ehealth-cache")
OUT = os.path.join("imports", "ehealth-models")
TIMEOUT = 90
USER_AGENT = "caresets-glossary/1.0 (+https://github.com/caresets)"


def fetch(url, binary=False, retries=3):
    """GET with a couple of retries - a 20-package run over one host will
    occasionally see a transient failure, and losing the whole run to it is
    worse than waiting."""
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                if binary:
                    return r.read()
                # Some of these files are served with a UTF-8 BOM and some are
                # not - lab and patientwill have one, core-clinical does not.
                # Plain utf-8 leaves it in the string and json.loads rejects it.
                return r.read().decode("utf-8-sig")
        except (urllib.error.URLError, urllib.error.HTTPError, OSError) as e:
            last = e
            if isinstance(e, urllib.error.HTTPError) and e.code == 404:
                break               # a missing file is an answer, not a glitch
            time.sleep(1.5 * (attempt + 1))
    raise last


def discover_from_publisher(url, only=None):
    """Guides from a publisher's own package-registry.json, if it serves one.

    Each entry already carries the canonical and the latest released version,
    so nothing further has to be fetched to know what to download.
    """
    try:
        data = json.loads(fetch(url))
    except (urllib.error.URLError, urllib.error.HTTPError, OSError, ValueError):
        # No registry at that address is the normal case, not a failure: most
        # publishers do not serve one. Only these are treated as "absent" -
        # anything else is a real fault and should not be swallowed.
        return None
    if not isinstance(data, dict) or "packages" not in data:
        return None

    guides = []
    for p in data.get("packages", []):
        canonical = (p.get("canonical") or "").rstrip("/")
        if not canonical:
            continue
        slug = canonical.rsplit("/", 1)[-1]
        if only and slug not in only and p.get("package-id") not in only:
            continue
        latest = p.get("latest") or {}
        # A registry can list the same canonical more than once - IHE has two
        # BALP entries - so key on the canonical and keep the higher version.
        prior = next((x for x in guides if x["canonical"] == canonical), None)
        if prior:
            if not latest.get("version") or (
                prior.get("release") or {}).get("version", "") >= latest["version"]:
                continue
            guides.remove(prior)
        guides.append({
            "name": p.get("package-id") or slug,
            "slug": slug,
            "canonical": canonical,
            "release": ({"version": latest.get("version"), "status": "release",
                         "path": (latest.get("path") or "").rstrip("/")}
                        if latest.get("version") and latest.get("path") else None),
        })
    return sorted(guides, key=lambda g: g["slug"]) or None


def discover_guides(only=None):
    """The eHealth implementation guides, from the FHIR IG registry.

    Matching on the canonical's host rather than on the package name: a guide
    is eHealth's if eHealth publishes it. Filtering by an `hl7.fhir.be` prefix
    would also catch guides published elsewhere, and a substring search over
    the whole record catches guides that merely depend on one.
    """
    data = json.loads(fetch(REGISTRY))
    guides = []
    for g in data.get("guides", []):
        canonical = (g.get("canonical") or "").rstrip("/")
        if PUBLISHER_HOST not in canonical:
            continue
        slug = canonical.rsplit("/", 1)[-1]
        if only and slug not in only and g.get("npm-name") not in only:
            continue
        guides.append({"name": g.get("npm-name") or slug,
                       "slug": slug, "canonical": canonical})
    return sorted(guides, key=lambda g: g["slug"])


def latest_release(guide):
    """The newest released version of a guide, from its package-list.json.

    ci-build entries are skipped: they are a moving target, not a publication.
    """
    try:
        data = json.loads(fetch(guide["canonical"] + "/package-list.json"))
    except Exception as e:
        return None, "no package-list.json (%s)" % e.__class__.__name__

    releases = [e for e in data.get("list", [])
                if e.get("version") and e.get("version") != "current"
                and e.get("status") != "ci-build"]
    if not releases:
        return None, "no released version"

    # package-list.json is ordered newest first by convention; sorting on a
    # version string would misplace 1.10.0 behind 1.9.0.
    top = releases[0]
    path = (top.get("path") or "").rstrip("/")
    if not path.startswith("http"):
        path = "%s/%s" % (guide["canonical"], top.get("version"))
    return {"version": top.get("version"), "status": top.get("status"),
            "path": path}, None


def package_bytes(guide, release, cache_dir, refresh=False):
    """The package.tgz for one release, cached by guide and version."""
    name = "%s-%s.tgz" % (guide["slug"], release["version"])
    path = os.path.join(cache_dir, name)
    if os.path.exists(path) and not refresh:
        return io.open(path, "rb").read(), True
    blob = fetch(release["path"] + "/package.tgz", binary=True)
    os.makedirs(cache_dir, exist_ok=True)
    with io.open(path, "wb") as fh:
        fh.write(blob)
    return blob, False


def logical_models(blob):
    """Every kind=logical StructureDefinition in a package."""
    out = []
    with tarfile.open(fileobj=io.BytesIO(blob)) as t:
        for m in t.getmembers():
            if not m.isfile() or not m.name.endswith(".json"):
                continue
            f = t.extractfile(m)
            if f is None:
                continue
            try:
                doc = json.load(io.TextIOWrapper(f, encoding="utf-8"))
            except (ValueError, UnicodeDecodeError):
                continue
            if isinstance(doc, dict) and doc.get("resourceType") == "StructureDefinition" \
                    and doc.get("kind") == "logical":
                out.append(doc)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ig", nargs="+", metavar="SLUG",
                    help="only these guides, by slug (core-clinical) or package name")
    ap.add_argument("--out-dir", dest="out_dir", default=OUT)
    ap.add_argument("--cache-dir", dest="cache_dir", default=CACHE)
    ap.add_argument("--publisher-registry", dest="publisher_registry",
                    default=PUBLISHER_REGISTRY,
                    help="a publisher's own package-registry.json, preferred when it "
                         "exists; falls back to the FHIR IG registry")
    ap.add_argument("--no-publisher-registry", action="store_true",
                    help="skip the publisher registry and use the FHIR IG registry")
    ap.add_argument("--refresh", action="store_true",
                    help="re-download packages already cached")
    ap.add_argument("--apply", action="store_true",
                    help="after fetching, run import_models_zip.py to bring the models "
                         "into input/models/")
    ap.add_argument("--dry-run", action="store_true",
                    help="discover and report, without downloading packages")
    args = ap.parse_args()

    sys.stdout.reconfigure(encoding="utf-8")
    out_dir = os.path.join(ROOT, args.out_dir)
    cache_dir = os.path.join(ROOT, args.cache_dir)

    only = set(args.ig) if args.ig else None
    guides = None
    if not args.no_publisher_registry:
        guides = discover_from_publisher(args.publisher_registry, only)
    if guides:
        source = "%s  (the publisher's own)" % args.publisher_registry
    else:
        source = REGISTRY
        guides = discover_guides(only)
    print("Registry: %s" % source)
    print("Guides  : %d\n" % len(guides))
    if not guides:
        sys.exit("No guides matched.")

    models, problems, cached_n = {}, [], 0
    for g in guides:
        # The publisher registry already named the release; only the IG-registry
        # route has to go and look it up.
        release, err = (g["release"], None) if g.get("release") else latest_release(g)
        if err:
            problems.append((g["slug"], err))
            print("  %-24s %s" % (g["slug"], err))
            continue
        if args.dry_run:
            print("  %-24s %-8s %s" % (g["slug"], release["version"], release["path"]))
            continue
        try:
            blob, from_cache = package_bytes(g, release, cache_dir, args.refresh)
        except Exception as e:
            problems.append((g["slug"], "package.tgz: %s" % e))
            print("  %-24s package.tgz failed: %s" % (g["slug"], e))
            continue
        cached_n += from_cache
        found = logical_models(blob)
        for doc in found:
            name = doc.get("name")
            if name in models:
                # The same model can ship in more than one guide; keep the
                # higher version rather than whichever was walked last.
                if str(doc.get("version", "")) <= str(models[name][0].get("version", "")):
                    continue
            models[name] = (doc, g["slug"], release["version"])
        print("  %-24s %-8s %2d logical model(s)%s"
              % (g["slug"], release["version"], len(found), "  [cached]" if from_cache else ""))

    if args.dry_run:
        print("\n--dry-run: nothing downloaded")
        return 0

    if os.path.isdir(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir, exist_ok=True)
    for name, (doc, slug, version) in sorted(models.items()):
        with io.open(os.path.join(out_dir, "StructureDefinition-%s.json" % name),
                     "w", encoding="utf-8", newline="\n") as fh:
            json.dump(doc, fh, ensure_ascii=False, indent=2)

    index = {
        "fetchedAt": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "registry": REGISTRY,
        "publisher": PUBLISHER_HOST,
        "models": [{"name": n, "version": doc.get("version"),
                    "url": doc.get("url"), "guide": slug, "guideVersion": gv,
                    "stage": "published"}
                   for n, (doc, slug, gv) in sorted(models.items())],
    }
    with io.open(os.path.join(out_dir, "index.json"), "w",
                 encoding="utf-8", newline="\n") as fh:
        json.dump(index, fh, ensure_ascii=False, indent=2)

    print("\n%d logical model(s) from %d guide(s) -> %s"
          % (len(models), len(guides) - len(problems), args.out_dir))
    print("%d package(s) served from the cache" % cached_n)
    if problems:
        print("\n%d guide(s) had a problem:" % len(problems))
        for slug, err in problems:
            print("  %-24s %s" % (slug, err))

    if args.apply:
        print("\nImporting into input/models/ ...")
        rc = subprocess.run([sys.executable, os.path.join(ROOT, "import_models_zip.py"),
                             out_dir], cwd=ROOT).returncode
        return rc
    print("\nNext: python import_models_zip.py %s" % args.out_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
