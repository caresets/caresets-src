# Report format

Both files are rendered by `scripts/render_report.py` from one hand-authored
findings JSON (see **Input** at the bottom). Do not write them by hand.

Four files per review, same timestamp stem, in `glossary-changes/`:

- `definition-quality-<YYYYMMDD_HHMMSS>.md` — the long-form report the reviewer edits
- `definition-quality-<YYYYMMDD_HHMMSS>.findings.json` — the machine sidecar
- `definition-quality-<YYYYMMDD_HHMMSS>.decisions.csv` — the diff-able decisions ledger
- `definition-quality-<YYYYMMDD_HHMMSS>.approval.md` — the approval report

The last two are written by `scripts/export_decisions.py`; the ledger's editable
columns are `Decision`, `Final FR`, `Final NL`, `Final EN` and `Comment`, and
everything else in it is regenerated from the sidecar.

## The report

Header, then a summary table, then one section per term, then the findings.

````markdown
# Definition quality review — <scope>

- Generated: <YYYY-MM-DD HH:MM:SS>
- Source: `input/<workbook>.xlsx`, sheet `Glossaire v1`, status `Active`
- EN source: `input/ClinicalGlossary.csv`, `input/OperationalGlossary.csv`
- Checklist: `input/Definition quality checklist.md`
- Terms reviewed: **N** · Findings: **M** (FR n · NL n · EN n)

## How to review this file

For every finding, edit the `decision` block: set `status` to `accept`,
`reject` or `revise`. On `revise`, put your own wording on the `fr:`, `nl:`
and/or `en:` lines — it is used verbatim. Add anything you want on `comment:`.
Leave `pending` on anything you have not decided; nothing is applied until you
say so, and nothing outside these blocks is read back.

## Summary

| ID | Term | Row | Lang | Rules | Severity | Issue |
|----|------|-----|------|-------|----------|-------|
| F-001 | AdministrationDate | 2 | FR | 1, 7 | major | ... |

## Findings

### F-001 · `AdministrationDate` (row 2) · FR

**Rules:** 1 (substitution), 7 (no examples in definition) · **Severity:** major

**Current**
> Date d'administration du produit / vaccin par le Performer.

**Problem**
One or two sentences, naming what the rule requires and how this text misses it.

**Proposed**
> date à laquelle un produit ou un vaccin est administré à un patient par le Performer

**Also move to `Description FR`:** <text, when the fix is a rule-7 relocation>

```decision F-001
status: pending        # accept | reject | revise
fr:
nl:
en:
comment:
```
````

Rules:

- Finding ids are `F-001`, `F-002`, … zero-padded, unique across the report, and
  identical in the sidecar and the ledger. Findings are ordered by sheet row, so
  the report can be walked alongside the workbook; within a row the cross-cutting
  finding comes first, then FR, NL, EN. Re-rendering after adding or removing a
  finding renumbers everything — if ids are already in circulation, say so and
  carry any recorded decisions across by (term, row, lang).
- One finding per (term, language) pair. If the same defect hits FR and NL, that
  is two findings — the reviewer may accept one and reject the other.
- Severity: `major` (definition is wrong, circular, or unusable as written),
  `minor` (correct but off-style, e.g. leading capital, trailing period, sentence
  form), `missing` (no definition in that language).
- Quote the current text with `>` so the diff is visible; never paraphrase it.
- The `decision` fence must be exactly ```` ```decision <ID> ```` with the keys
  `status`, `fr`, `nl`, `en`, `comment` in that order, one per line, and must be
  the last thing in the finding.

## The sidecar

```json
[
  {
    "id": "F-001",
    "row": 2,
    "term": "AdministrationDate",
    "lang": "fr",
    "rules": [1, 7],
    "severity": "major",
    "current": "Date d'administration du produit / vaccin par le Performer.",
    "proposed": { "fr": "date à laquelle un produit ou un vaccin est administré …" },
    "description_move": "Une période de la vie peut aussi être mentionnée …"
  }
]
```

`proposed` is keyed by language so `apply_decisions.py` knows which column to
write. Include only the languages this finding changes.

## Input

What you actually author is the findings JSON handed to `render_report.py`:

```json
{
  "scope": "Glossaire v1 — status Active",
  "source": "input/Glossaire CareSets V1 28-08-2026.xlsx",
  "sheet": "Glossaire v1",
  "terms_reviewed": 23,
  "intro": "optional paragraph placed above the how-to-review section",
  "findings": [
    {
      "row": 5,
      "term": "BodyLaterality",
      "lang": "fr",
      "rules": [3, 4],
      "severity": "major",
      "current": "la latéralité du corps .",
      "problem": "First line becomes the Summary-table issue text; keep it short.",
      "proposed": "côté du corps auquel se rapporte l'information enregistrée",
      "description_move": "optional — text that belongs in the Description column",
      "note": "optional — anything the reviewer should know before deciding"
    }
  ]
}
```

- `proposed` may be a string (applies to this finding's `lang`) or an object
  keyed by language.
- `lang: "meta"` marks a cross-cutting finding — a term name, a Description
  column holding another entry's content, a synonym that contradicts another
  entry. Give it a `row` when it points at one; omit `proposed` when there is
  no cell to write. `apply_decisions.py` will not write these; act on an
  accepted `meta` finding by hand.
- Ids are assigned by the renderer in row order, so do not set `id` yourself
  unless you are regenerating a report whose ids are already in circulation.
