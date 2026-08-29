---
name: definition-quality-review
description: Audit CareSets glossary definitions against the Definition quality checklist (ISO 704 / ISO-IEC Directives Part 2) and produce a reviewable report with per-finding accept/revise/reject decisions. Use when asked to check, review, QA or improve glossary definitions in input/Glossaire CareSets*.xlsx or the glossary CSVs, in FR, NL or EN, or to apply the reviewer's decisions back to the workbook.
---

# Definition quality review

Audit glossary definitions against `input/Definition quality checklist.md`, report
the defects with concrete replacement wording, and let the reviewer accept, revise
or reject each one — then apply what they agreed to.

The checklist in `input/Definition quality checklist.md` is the single source of
truth for the rules. **Read it at the start of every run** — do not work from the
summary below, which is only an index:

| # | Rule | # | Rule |
|---|---|---|---|
| 1 | Substitution test (phrase, not sentence) | 6 | One concept per definition |
| 2 | Same grammatical category as the term | 7 | No requirements, guidance or examples inside |
| 3 | Non-circularity | 8 | Necessary and sufficient |
| 4 | Genus + differentiating characteristics | 9 | Defined or commonly understood terms only |
| 5 | Positive formulation | 10 | Consistency with the concept system |

## Data layout

- **`input/Glossaire CareSets V<n> <date>.xlsx`**, sheet `Glossaire v1` — the working
  source. Columns: `statut de la def`, `Item`, `Synonym`, `Suggested Min/Max`,
  `Definition FR`, `Description FR`, `Définition NL`, `Description NL`, `DataType`.
  **There is no EN column here.**
- **`input/ClinicalGlossary.csv` / `OperationalGlossary.csv`** (`;`-separated,
  `Term;Status;Synonym;FR;EN;NL`) — the published glossary, and the only place EN
  lives. The extractor joins EN in by `Term`.
- `Definition` is the definition proper; `Description` is the note-to-entry slot.
  Rule 7 material (examples, "shall", implementation detail) belongs in
  `Description`, not `Definition` — moving text between the two columns is a normal
  and preferred fix, not a rewrite.

## Workflow

### 1. Extract

```sh
python .claude/skills/definition-quality-review/scripts/extract_definitions.py \
  --status Active --out <scratchpad>/defs.json
```

Defaults to the newest `input/Glossaire CareSets*.xlsx`, sheet `Glossaire v1`,
status `Active`. Pass `--workbook` / `--sheet` / `--status` to widen the scope
(e.g. `--status Draft`). Each entry carries its 1-based `row`, so findings can be
written straight back later.

### 2. Review

Judge **every language independently** — FR, NL and EN each get their own verdict
against all ten rules. A term can pass in FR and fail in NL.

Also check, across languages:

- **Missing translation** — a language whose definition is empty or absent (EN is
  missing for any active term not yet in the CSVs). Report it as a finding.
- **Divergence** — NL/EN saying something the FR does not, or vice versa. The
  translation must express the same concept, not a different one, and must satisfy
  the checklist in its own right; a faithful translation of a defective FR
  definition is still a finding in both languages.
- **Term-name consistency (rule 10)** — sibling items should share genus and
  register, and item names themselves should be consistent across the sheet.

Only report defects you can name a rule for, and prefer the smallest fix that
clears it. Do not invent domain content: if fixing a definition needs a fact you
cannot get from the workbook, the CSVs or the models, say so in the finding and
propose the wording as provisional.

### 3. Write the report

Author the findings as one JSON file (schema in `references/report-format.md`
and in the script's docstring), then render both output files from it:

```sh
python .claude/skills/definition-quality-review/scripts/render_report.py   <scratchpad>/findings.json   --out glossary-changes/definition-quality-<YYYYMMDD_HHMMSS>.md
```

That writes the reviewable `.md` and the `.findings.json` sidecar from the same
data, assigns the `F-nnn` ids, and appends the ```decision fence to every
finding. Never hand-write the two files separately — they must not drift.

Set `lang` to `fr`, `nl`, `en`, or `meta` for a cross-cutting finding (term
naming, a column holding the wrong content, a synonym that contradicts another
entry). `meta` findings are decided like any other but are applied by hand.

Tell the reviewer where the report is and how to fill it in. Stop there — do not
edit the workbook in the same run as the review.

### 4. Export the decisions ledger (after every review pass)

```sh
python .claude/skills/definition-quality-review/scripts/export_decisions.py \
  glossary-changes/<report>.md --approval
```

Writes two more files next to the report:

- `<report>.decisions.csv` — the **ledger**: one `;`-separated row per finding,
  in id order, holding `Decision`, `Final FR/NL/EN` and `Comment` alongside the
  current and proposed text. This is the artefact to commit — one changed mind is
  one changed line, so a `git diff` shows exactly what was decided and when.
- `<report>.approval.md` — the approval report: only the accepted and revised
  items, current → proposed, grouped by term, with a sign-off table.

Re-running merges rather than overwrites: decisions taken in the report are
folded in, decisions already in the ledger are kept, and any genuine
disagreement between the two is printed as a conflict with the ledger value
kept. So the reviewer can work in the long-form report or directly in the ledger.

### 5. Collect decisions

```sh
python .claude/skills/definition-quality-review/scripts/collect_decisions.py \
  glossary-changes/<report>.decisions.csv --json <scratchpad>/decisions.json
```

Takes the ledger `.csv` or the report `.md` — prefer the ledger once it exists,
since it is the merged state. Reports the tally and flags malformed entries
(`revise` with no text, unknown status). Resolve every problem it lists — and
confirm what to do with anything still `pending` — before applying anything.

### 6. Apply

```sh
python .claude/skills/definition-quality-review/scripts/apply_decisions.py \
  --findings glossary-changes/<report>.findings.json \
  --decisions <scratchpad>/decisions.json \
  --out input/<new workbook name>.xlsx
```

Writes a **new** workbook (it refuses to overwrite the source) plus a
`.changelog.json` of every before/after. `accept` takes the proposed text,
`revise` takes the reviewer's text, `reject` and `pending` are skipped.

EN has no workbook column, so EN changes come out as a printed patch list for
`input/ClinicalGlossary.csv` — apply those by editing the CSV, then run
`python build_content.py` from the repo root to regenerate `_resources/`.

## Rules of engagement

- Never edit `input/Glossaire CareSets*.xlsx` in place; always produce a new file.
- Never apply a finding the reviewer has not marked `accept` or `revise`.
- Never touch `_resources/` — it is generated.
- Preserve the reviewer's own wording verbatim on `revise`; do not "improve" it.
