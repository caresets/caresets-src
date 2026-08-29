#!/usr/bin/env python
"""Read the reviewer's decisions back out of a definition-quality review report.

Each finding in the report carries one fenced block:

    ```decision F-003
    status: pending          # accept | reject | revise
    fr:
    nl:
    en:
    comment:
    ```

Usage:
    python collect_decisions.py REPORT.md            # human summary
    python collect_decisions.py REPORT.md --json OUT # machine-readable
"""
import argparse
import json
import re
import sys

BLOCK_RE = re.compile(
    r"^```decision[ \t]+(?P<id>[A-Za-z0-9_.-]+)[ \t]*\n(?P<body>.*?)^```[ \t]*$",
    re.MULTILINE | re.DOTALL,
)
KEY_RE = re.compile(r"^(status|fr|nl|en|comment)[ \t]*:(?P<rest>.*)$", re.IGNORECASE)
VALID = {"accept", "reject", "revise", "pending"}


def strip_comment(line):
    """Drop a trailing ' # ...' hint, but keep '#' that is part of real text."""
    m = re.search(r"(?:^|\s)#\s(?:accept|reject|revise)\b.*$", line)
    return line[: m.start()] if m else line


def read_ledger(path):
    """The `;`-separated decisions ledger, in the same shape as a parsed block."""
    import csv

    out = []
    with open(path, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh, delimiter=";"):
            out.append((
                r["ID"],
                {
                    "status": r.get("Decision"),
                    "fr": r.get("Final FR") or None,
                    "nl": r.get("Final NL") or None,
                    "en": r.get("Final EN") or None,
                    "comment": r.get("Comment") or None,
                },
            ))
    return out


def parse_block(body):
    """Tolerant key: value parser; values may span lines until the next key."""
    fields, key, buf = {}, None, []

    def flush():
        if key is not None:
            fields[key] = "\n".join(buf).strip() or None

    for line in body.splitlines():
        m = KEY_RE.match(line)
        if m:
            flush()
            key = m.group(1).lower()
            buf = [strip_comment(m.group("rest")).strip()]
        elif key is not None:
            # continuation of the current value; drop the wrap indent
            buf.append(line.strip())
    flush()
    return fields


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("report", help="the review report .md, or a .decisions.csv ledger")
    ap.add_argument("--json", dest="json_out")
    ap.add_argument("--sidecar", help="the .findings.json, so cross-cutting findings "
                                      "are not flagged for carrying no replacement text")
    args = ap.parse_args()

    problems = []
    meta_ids = set()
    if args.sidecar:
        with open(args.sidecar, encoding="utf-8") as fh:
            meta_ids = {f["id"] for f in json.load(fh) if f.get("lang") == "meta"}
    if args.report.lower().endswith(".csv"):
        raw = read_ledger(args.report)
    else:
        with open(args.report, encoding="utf-8") as fh:
            text = fh.read()
        raw = [
            (m.group("id"), parse_block(m.group("body"))) for m in BLOCK_RE.finditer(text)
        ]

    decisions = []
    for fid, f in raw:
        status = (f.get("status") or "pending").strip().lower()
        if status not in VALID:
            problems.append("%s: unknown status %r" % (fid, status))
            status = "invalid"
        d = {
            "id": fid,
            "status": status,
            "fr": f.get("fr"),
            "nl": f.get("nl"),
            "en": f.get("en"),
            "comment": f.get("comment"),
        }
        if (status == "revise" and fid not in meta_ids
                and not any(d[k] for k in ("fr", "nl", "en"))):
            problems.append("%s: status 'revise' but no fr/nl/en text supplied" % fid)
        decisions.append(d)

    if not decisions:
        sys.exit("No decisions found in %s" % args.report)

    tally = {}
    for d in decisions:
        tally[d["status"]] = tally.get(d["status"], 0) + 1

    payload = {
        "report": args.report,
        "count": len(decisions),
        "tally": tally,
        "problems": problems,
        "decisions": decisions,
    }

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)

    sys.stdout.reconfigure(encoding="utf-8")
    print("%d findings in %s" % (len(decisions), args.report))
    for k in ("accept", "revise", "reject", "pending", "invalid"):
        if k in tally:
            print("  %-8s %d" % (k, tally[k]))
    for p in problems:
        print("  ! %s" % p)
    if not args.json_out:
        for d in decisions:
            if d["status"] in ("accept", "revise"):
                print("\n[%s] %s" % (d["status"], d["id"]))
                for lang in ("fr", "nl", "en"):
                    if d[lang]:
                        print("  %s: %s" % (lang.upper(), d[lang]))
                if d["comment"]:
                    print("  comment: %s" % d["comment"])


if __name__ == "__main__":
    main()
