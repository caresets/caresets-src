#!/usr/bin/env python
"""Export the decisions taken on a review report into a diff-able ledger, and
render an approval report from that ledger.

The ledger is one `;`-separated row per finding, in stable id order, so a change
of mind shows up as a one-line diff. It is the artefact to commit and to hand
round for sign-off; the review report stays as the long-form justification.

    python export_decisions.py REPORT.md                  # write/refresh the ledger
    python export_decisions.py REPORT.md --approval       # + the approval report
    python export_decisions.py --ledger LEDGER.csv --approval   # from the ledger alone

Editable columns in the ledger: Decision, Final FR, Final NL, Final EN, Comment.
Everything else is context and is regenerated from the report's sidecar.

Refreshing an existing ledger keeps the decisions already recorded in it and
merges in anything newly decided in the report, so the two can be edited in
either place without losing work.
"""
import argparse
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from collect_decisions import BLOCK_RE, parse_block  # noqa: E402

FIELDS = [
    "ID", "Row", "Term", "Lang", "Rules", "Severity", "Decision",
    "Final FR", "Final NL", "Final EN", "Comment", "Current", "Proposed",
]
EDITABLE = ("Decision", "Final FR", "Final NL", "Final EN", "Comment")
LANG_KEY = {"fr": "Final FR", "nl": "Final NL", "en": "Final EN"}
VALID = {"accept", "reject", "revise", "pending"}


def read_report(path):
    """finding id -> decision fields, from the ```decision blocks in the report."""
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    out = {}
    for m in BLOCK_RE.finditer(text):
        f = parse_block(m.group("body"))
        out[m.group("id")] = {
            "status": (f.get("status") or "pending").strip().lower(),
            "fr": f.get("fr"), "nl": f.get("nl"), "en": f.get("en"),
            "comment": f.get("comment"),
        }
    return out


def read_ledger(path):
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8-sig", newline="") as fh:
        return {r["ID"]: r for r in csv.DictReader(fh, delimiter=";")}


def flatten(v):
    """Ledger cells are single-line; keep multi-line reviewer text readable."""
    if not v:
        return ""
    return " ".join(str(v).split())


def build_rows(sidecar, report_decisions, existing, prefer_report=None):
    """prefer_report: ids where the report deliberately supersedes the ledger
    (a later ruling that overturns an earlier decision), or True for all."""
    rows, conflicts = [], []
    for f in sidecar:
        fid = f["id"]
        prev = existing.get(fid, {})
        rep = report_decisions.get(fid)
        wins = prefer_report is True or (prefer_report and fid in prefer_report)

        row = {
            "ID": fid,
            "Row": f.get("row") or "",
            "Term": f.get("term") or "",
            "Lang": (f.get("lang") or "").upper(),
            "Rules": ", ".join(str(r) for r in f.get("rules") or []),
            "Severity": f.get("severity") or "",
            "Current": flatten(f.get("current")),
            "Proposed": flatten(
                " / ".join("%s: %s" % (k.upper(), v) for k, v in (f.get("proposed") or {}).items())
                if len(f.get("proposed") or {}) > 1
                else "".join((f.get("proposed") or {}).values())
            ),
        }

        # Decisions from the report win only where the ledger has not been
        # edited to something else; otherwise flag it rather than pick a side.
        for col, src in (("Decision", "status"), ("Comment", "comment")):
            rep_v = flatten(rep.get(src)) if rep else ""
            if col == "Decision" and rep_v == "pending":
                rep_v = ""  # not a decision, so never in conflict with the ledger
            led_v = flatten(prev.get(col))
            if col == "Decision" and led_v == "pending":
                led_v = ""
            row[col] = rep_v or led_v
            if rep_v and led_v and rep_v != led_v:
                if wins:
                    conflicts.append("%s %s: report supersedes ledger" % (fid, col))
                else:
                    conflicts.append("%s %s: report %r vs ledger %r" % (fid, col, rep_v, led_v))
                    row[col] = led_v
        for lang, col in LANG_KEY.items():
            rep_v = flatten(rep.get(lang)) if rep else ""
            led_v = flatten(prev.get(col))
            row[col] = rep_v or led_v
            if rep_v and led_v and rep_v != led_v:
                if wins:
                    conflicts.append("%s %s: report supersedes ledger" % (fid, col))
                else:
                    conflicts.append("%s %s: report %r vs ledger %r" % (fid, col, rep_v, led_v))
                    row[col] = led_v

        row["Decision"] = row["Decision"] or "pending"
        rows.append(row)
    return rows, conflicts


def final_text(row):
    """The text this row would write, and to which language."""
    if row["Decision"] not in ("accept", "revise"):
        return []
    out = []
    for lang, col in (("FR", "Final FR"), ("NL", "Final NL"), ("EN", "Final EN")):
        if row.get(col):
            out.append((lang, row[col]))
    if not out and row["Decision"] == "accept" and row["Proposed"]:
        out.append((row["Lang"], row["Proposed"]))
    return out


def write_approval(rows, path, report_name):
    decided = [r for r in rows if r["Decision"] in ("accept", "revise")]
    rejected = [r for r in rows if r["Decision"] == "reject"]
    pending = [r for r in rows if r["Decision"] == "pending"]

    o = []
    o.append("# Glossary definition changes - for approval\n")
    o.append("- Source review: `%s`" % report_name)
    o.append("- Changes proposed: **%d** / Rejected: **%d** / Still open: **%d**\n"
             % (len(decided), len(rejected), len(pending)))
    o.append("Each change below has been reviewed and is put forward for approval. "
             "The full justification for every item - the rule it breaches and why - "
             "is in the source review report.\n")

    if decided:
        o.append("## Changes proposed\n")
        last = object()
        for r in decided:
            if r["Term"] != last:
                last = r["Term"]
                o.append("### `%s`%s\n" % (r["Term"], " (row %s)" % r["Row"] if r["Row"] else ""))
            for lang, text in final_text(r):
                o.append("**%s - %s** (%s, rules %s)\n"
                         % (r["ID"], lang, r["Severity"], r["Rules"] or "-"))
                o.append("| | |")
                o.append("|--|--|")
                o.append("| Current | %s |" % (r["Current"].replace("|", "\\|") or "*(none)*"))
                o.append("| **Proposed** | **%s** |" % text.replace("|", "\\|"))
                o.append("")
                if r["Comment"]:
                    o.append("> %s\n" % r["Comment"])

    if rejected:
        o.append("## Reviewed and left unchanged\n")
        o.append("| ID | Term | Row | Lang | Reason given |")
        o.append("|----|------|-----|------|--------------|")
        for r in rejected:
            o.append("| %s | %s | %s | %s | %s |"
                     % (r["ID"], r["Term"], r["Row"], r["Lang"],
                        r["Comment"].replace("|", "\\|") or "-"))
        o.append("")

    if pending:
        o.append("## Still open (%d)\n" % len(pending))
        o.append("Not put forward for approval yet.\n")
        o.append("| ID | Term | Row | Lang | Severity |")
        o.append("|----|------|-----|------|----------|")
        for r in pending:
            o.append("| %s | %s | %s | %s | %s |"
                     % (r["ID"], r["Term"], r["Row"], r["Lang"], r["Severity"]))
        o.append("")

    o.append("## Approval\n")
    o.append("| | Name | Date | Outcome |")
    o.append("|--|------|------|---------|")
    o.append("| Reviewer | | | |")
    o.append("| Approver | | | |")
    o.append("")

    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(o))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("report", nargs="?", help="the review report .md")
    ap.add_argument("--ledger", help="ledger path (default: <report stem>.decisions.csv)")
    ap.add_argument("--sidecar", help="findings sidecar (default: <report stem>.findings.json)")
    ap.add_argument("--approval", nargs="?", const=True,
                    help="also write the approval report (default: <report stem>.approval.md)")
    ap.add_argument("--prefer-report", nargs="?", const=True, dest="prefer_report",
                    help="comma-separated finding ids where the report deliberately supersedes "
                         "the ledger (a later ruling overturning an earlier decision); bare flag "
                         "means all. Without it the ledger value is kept on any disagreement.")
    args = ap.parse_args()
    prefer = args.prefer_report
    if isinstance(prefer, str):
        prefer = {i.strip() for i in prefer.split(",") if i.strip()}

    if not args.report and not args.ledger:
        sys.exit("Give a report .md, or --ledger to work from an existing ledger")

    stem = os.path.splitext(args.report)[0] if args.report else os.path.splitext(args.ledger)[0]
    if stem.endswith(".decisions"):
        stem = stem[: -len(".decisions")]
    ledger_path = args.ledger or stem + ".decisions.csv"
    sidecar_path = args.sidecar or stem + ".findings.json"

    with open(sidecar_path, encoding="utf-8") as fh:
        sidecar = json.load(fh)
    report_decisions = read_report(args.report) if args.report else {}
    rows, conflicts = build_rows(sidecar, report_decisions, read_ledger(ledger_path), prefer)

    bad = [r["ID"] for r in rows if r["Decision"] not in VALID]
    with open(ledger_path, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS, delimiter=";", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

    sys.stdout.reconfigure(encoding="utf-8")
    tally = {}
    for r in rows:
        tally[r["Decision"]] = tally.get(r["Decision"], 0) + 1
    print("Ledger : %s (%d findings)" % (ledger_path, len(rows)))
    for k in ("accept", "revise", "reject", "pending"):
        if k in tally:
            print("  %-8s %d" % (k, tally[k]))
    for c in conflicts:
        print("  ! %s%s" % ("" if "supersedes" in c else "conflict, kept the ledger value - ", c))
    for b in bad:
        print("  ! %s has an unknown Decision value" % b)

    if args.approval:
        path = args.approval if isinstance(args.approval, str) else stem + ".approval.md"
        write_approval(rows, path, os.path.basename(args.report or ledger_path))
        print("Approval: %s" % path)


if __name__ == "__main__":
    main()
