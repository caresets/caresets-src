"""
Build the RIZIV-INAMI deliverable: content, site, zip, hash.

The three steps this replaces are shell-specific - `&&` and backslash
continuations are bash, and PowerShell rejects both - so they are here instead,
where the syntax is the same wherever you run it.

  1  build_content.py                 glossary and models -> _resources/
  2  jekyll build                     -> _site_riziv/
                                      with _config_riziv.yml layered on, which
                                      clears `url` so RIZIV pages do not declare
                                      the GitHub Pages copy as canonical
  3  zip                              -> riziv-inami-site.zip
  4  SHA-256                          the value HANDOVER-DISCLAIMER.md pins

The zip is written with Python rather than Compress-Archive or `zip`, so the
same bytes come out on any machine: entries sorted, forward-slash paths, a
fixed timestamp. Two builds of unchanged content then have the same hash, which
is what makes the hash in the handover statement worth anything.

  python build_package.py                     the RIZIV zip, and report its hash
  python build_package.py --update-disclaimer and write that hash into the handover
  python build_package.py --ghpages           the public site into _site_ghpages/
  python build_package.py --publish-to PATH   the public site straight into a clone
                                              of caresets/caresets, ready to commit
  python build_package.py --restricted        not-public mode (noindex, banner)
  python build_package.py --skip-content      skip the content step
"""

import argparse
import hashlib
import io
import os
import re
import shutil
import subprocess
import sys
import zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "_site_riziv"
ZIP = "riziv-inami-site.zip"
DISCLAIMER = "HANDOVER-DISCLAIMER.md"
CONFIGS = ["_config.yml", "_config_riziv.yml"]
RESTRICTED_OVERLAY = "_config_restricted.yml"

# A fixed timestamp for every entry. Zip stores mtimes, so without this the
# hash changes on every build even when nothing does.
FIXED_DATE = (2026, 1, 1, 0, 0, 0)


def run(cmd, **kw):
    print("  $ %s" % " ".join(cmd))
    return subprocess.run(cmd, cwd=ROOT, **kw).returncode


def jekyll(configs, dest, baseurl=""):
    """Jekyll is a Ruby command; shell=True keeps `bundle exec` working on
    Windows, where bundle is a batch shim rather than an executable."""
    cmd = ("bundle exec jekyll build --config %s --baseurl \"%s\" --destination %s"
           % (",".join(configs), baseurl, dest))
    print("  $ %s" % cmd)
    return subprocess.run(cmd, cwd=ROOT, shell=True).returncode


def make_zip(src, out):
    """A deterministic zip: sorted entries, forward slashes, fixed timestamps."""
    files = []
    for base, _dirs, names in os.walk(src):
        for n in names:
            full = os.path.join(base, n)
            files.append((os.path.relpath(full, src).replace(os.sep, "/"), full))
    files.sort()

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for arcname, full in files:
            info = zipfile.ZipInfo(arcname, date_time=FIXED_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, io.open(full, "rb").read())
    return len(files)


def sha256(path):
    h = hashlib.sha256()
    with io.open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--skip-content", action="store_true",
                    help="do not re-run build_content.py")
    ap.add_argument("--restricted", action="store_true",
                    help="build in not-public mode: noindex, robots.txt Disallow "
                         "and the restricted-distribution banner. Keeps the site "
                         "out of search results; does not restrict access")
    ap.add_argument("--update-disclaimer", action="store_true",
                    help="write the resulting hash into HANDOVER-DISCLAIMER.md")
    ap.add_argument("--ghpages", metavar="BASEURL", nargs="?", const="/caresets",
                    help="build the GitHub Pages copy into _site_ghpages/ instead "
                         "of the RIZIV package: the main config only, and the "
                         "baseurl the Pages site is served under (default "
                         "/caresets, the repo that serves the site - not this one). No zip "
                         "is produced: the folder is what "
                         "you publish")
    ap.add_argument("--publish-to", dest="publish_to", metavar="PATH",
                    help="build the GitHub Pages copy straight into a local "
                         "clone of the public repository, e.g. "
                         "E:/work/BE/caresets-site. Implies --ghpages. The "
                         "path must be a git work tree - Jekyll empties its "
                         "destination, and this is the check that stops it "
                         "emptying an ordinary folder")
    ap.add_argument("--out", default=ZIP)
    args = ap.parse_args()

    sys.stdout.reconfigure(encoding="utf-8")

    if args.publish_to and not args.ghpages:
        args.ghpages = "/caresets"

    if not args.skip_content:
        print("[1/4] Content")
        if run([sys.executable, os.path.join(ROOT, "build_content.py")]):
            return 1
    else:
        print("[1/4] Content  (skipped)")

    configs = ["_config.yml"] if args.ghpages else list(CONFIGS)

    keep_overlay = os.path.join(ROOT, "_config_keep.yml")
    if args.publish_to:
        # Jekyll's own default keeps .git; CNAME is not generated by the build
        # and would otherwise be deleted, taking the custom domain with it.
        io.open(keep_overlay, "w", encoding="utf-8", newline="\n").write(
            "# Written by build_package.py --publish-to; removed after the build.\n"
            "keep_files: [\".git\", \"CNAME\"]\n")
        configs.append("_config_keep.yml")

    overlay = os.path.join(ROOT, RESTRICTED_OVERLAY)
    if args.restricted:
        # Written beside the other configs because Jekyll resolves --config
        # relative to the source directory, then removed again so the flag
        # cannot leak into a later build.
        io.open(overlay, "w", encoding="utf-8", newline="\n").write(
            "# Written by build_package.py --restricted; removed after the build.\n"
            "restricted: true\n")
        configs.append(RESTRICTED_OVERLAY)

    print("\n[2/4] Site%s" % ("  (not-public mode)" if args.restricted else ""))
    if args.publish_to:
        dest = os.path.abspath(args.publish_to)
        site = dest
        # Jekyll empties its destination before writing. Into a clone that is
        # exactly what we want - stale pages should go - but into a mistyped
        # path it would delete somebody's folder, so refuse anything that is
        # not a git work tree.
        if not os.path.isdir(os.path.join(dest, ".git")):
            print("  ! %s is not a git clone - refusing to build into it, "
                  "because Jekyll would empty it first." % dest)
            return 1
        remote = subprocess.run(["git", "-C", dest, "remote", "get-url", "origin"],
                                capture_output=True, text=True)
        print("  target: %s" % dest)
        print("  origin: %s" % (remote.stdout.strip() or "(none)"))
    else:
        site = "_site_ghpages" if args.ghpages else SITE
        dest = os.path.join(ROOT, site)
        if os.path.isdir(dest):
            shutil.rmtree(dest)
    try:
        rc = jekyll(configs, site, args.ghpages or "")
    finally:
        if args.restricted and os.path.exists(overlay):
            os.remove(overlay)
        if os.path.exists(keep_overlay):
            os.remove(keep_overlay)
    if rc:
        return rc

    if args.ghpages:
        # GitHub Pages runs Jekyll over whatever it is given unless told not to,
        # and Jekyll drops every path beginning with an underscore. That removes
        # _resources/, so the glossary and every model 404 on the live site
        # while the build itself looks perfect. .nojekyll turns that processing
        # off. The deploy action writes one; a hand-copied deploy has nothing
        # that would.
        io.open(os.path.join(dest, ".nojekyll"), "w").close()
        print("  .nojekyll written - Pages would otherwise drop _resources/")

        # The Pages copy is published as a folder, not a zip, so there is
        # nothing to hash and nothing for the handover statement to pin.
        print("\n[3/4] Package  (skipped - GitHub Pages copy)")
        if args.publish_to:
            print("\nBuilt into %s for baseurl %r." % (dest, args.ghpages))
            st = subprocess.run(["git", "-C", dest, "status", "--short"],
                                capture_output=True, text=True)
            lines = [l for l in st.stdout.splitlines() if l.strip()]
            print("  %d path(s) changed in the clone." % len(lines))
            for l in lines[:12]:
                print("    %s" % l)
            if len(lines) > 12:
                print("    ... and %d more" % (len(lines) - 12))
            print("\nReview with `git -C %s status`, then commit and push there."
                  % dest)
        else:
            print("\nBuilt %s/ for baseurl %r." % (site, args.ghpages))
            print("Copy its contents into the public repo, replacing what is there.")
        return 0

    print("\n[3/4] Package")
    out = args.out if os.path.isabs(args.out) else os.path.join(ROOT, args.out)
    n = make_zip(dest, out)
    size = os.path.getsize(out)
    print("  %s  %d file(s), %.1f MB" % (args.out, n, size / 1048576.0))

    print("\n[4/4] SHA-256")
    digest = sha256(out)
    print("  %s" % digest)

    if args.update_disclaimer:
        p = os.path.join(ROOT, DISCLAIMER)
        s = io.open(p, encoding="utf-8").read()
        s2 = re.sub(r"(\*\*SHA-256:\*\*\s*`)[0-9a-f]{64}(`)",
                    lambda m: m.group(1) + digest + m.group(2), s, count=1)
        if s2 == s:
            print("  ! no SHA-256 line found in %s - not updated" % DISCLAIMER)
        else:
            io.open(p, "w", encoding="utf-8", newline="\n").write(s2)
            print("  %s updated" % DISCLAIMER)
    else:
        print("\n  HANDOVER-DISCLAIMER.md pins this value. Re-run with")
        print("  --update-disclaimer to write it in.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
