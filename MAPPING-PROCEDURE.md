# Mapping model elements to the Common Glossary

How a logical model element gets tied to a glossary concept, from the published
StructureDefinition to the workbook an analyst edits.

The short version: **the workbook is where a mapping lives; the CSV is where a
mapping is proposed and decided.** Nothing acts on a mapping until somebody has
marked it confirmed.

---

## The four steps

```
  1  fetch        published StructureDefinitions  ->  models/xls/*.xlsx
  2  propose      new mappings          ->  input/glossary_mappings.csv  (Status = proposed)
  3  review       a person sets Status  ->  confirmed  or  rejected
  4  merge        confirmed mappings    ->  the workbooks' Code column
  5  generate     the workbooks         ->  element.code in models/generated/
```

Step 2 can equally be done by hand: adding a row to the CSV with
`Status=proposed` is the same act as the script performing it.

---

## 1. Fetch the models and build the workbooks

```bash
python fetch_ehealth_models.py --apply      # download from ehealth.fgov.be
python export_logical_model_xlsx.py --overwrite --include-draft
```

`fetch_ehealth_models.py` walks the publisher's package registry, downloads each
guide's `package.tgz`, keeps the `kind: logical` StructureDefinitions, and
imports them into `input/models/`. It caches packages, so a re-run is cheap.
Run it every two to four weeks.

`export_logical_model_xlsx.py` turns each model into one workbook under
`models/xls/`, filling the `Code` column from the **confirmed** rows of the
mappings CSV.

Two flags matter:

- `--overwrite` — without it, existing workbooks are left alone. That default
  protects an analyst's unpublished work: English text or a glossary code typed
  into a workbook lives only there until it has been published, and
  re-exporting from the model would discard it silently. Use `--overwrite` only
  when the workbooks hold nothing that is not already in the models.
- `--include-draft` — models under `input/models/draft/` are excluded by
  default, because drafts are kept out of the published site. Pass this to map
  them too. Without it you get 38 workbooks; with it, 41.

## 2. Propose mappings

```bash
python propose_model_mappings.py --report
```

This reads every workbook, finds elements with an empty `Code`, and appends a
row to `input/glossary_mappings.csv` for each one it can propose a concept for:

| Column | Meaning |
|---|---|
| `Model` | the StructureDefinition's `name` |
| `ElementSuffix` | the element path below the root, e.g. `reactions.note` |
| `GlossaryCode` | the proposed Common Glossary concept |
| `GlossaryStatus` | whether that concept is an approved glossary term |
| `Status` | `proposed`, `confirmed` or `rejected` |
| `Confidence` | `certain`, `likely` or `check` — see below |
| `Rationale` | why this concept, in one line |
| `ElementDescription` | the model's own words for the element |

The last three exist so the CSV can be reviewed in Excel on its own, without
opening the model beside it.

**The script never touches a row that is already there.** A rejected mapping
does not come back as a proposal on the next run, and a confirmed one is not
second-guessed. Re-running after new models arrive proposes only for what is
genuinely new.

`--report` also writes a grouped read-through under `glossary-changes/`, which
lists proposals by concept rather than by model — useful for judging a decision
that spans twenty models at once. It is a reading aid; the CSV is the artifact.

### Only approved terms

A mapping is meaningful only if its target is a term the glossary actually
publishes and has approved. The clinical glossary holds 24 approved terms; the
workbook holds 96 in total, so pointing at one still being drafted is easy to
do by hand and would not otherwise surface until the term failed to resolve on
the site.

Every row carries a `GlossaryStatus` saying where its target stands:

| Value | Meaning |
|---|---|
| `approved` | the glossary publishes the term and it is approved |
| `in the workbook, not approved` | the term is being drafted - approve it, or point the mapping elsewhere |
| `not in glossary` | no such term; usually a typo |

The column is recomputed on every run of the proposer and again at merge time,
so it cannot go stale: a term withdrawn after a row was written starts showing
as unapproved straight away.

`merge_mappings_to_xlsx.py` **holds back** any confirmed row whose target is
not approved, and reports it. `--allow-unapproved` writes them anyway, which is
reasonable when a term is known to be about to be approved, and otherwise is
not.

Mapping to a term still being drafted is a legitimate thing to *propose* - the
requirement is that it is visible, not that it is forbidden.

### What confidence means

It is a judgement, not a measurement:

- **certain** — the element is that concept under another name, and every
  model's own description confirms it. `recorder`, `asserter`, `lotNumber`.
- **likely** — the mapping holds across the models seen, but the name is
  generic enough that some model could use it differently. `status`, `subject`,
  `bodySite`.
- **check** — plausible, but read the descriptions before deciding. `device`
  is the instrument an act was carried out with, and a model where the device
  is the *subject* of the act means something else by it.

### What the proposer will not do

Two limits are deliberate:

- **It does not map below the top level for the CareSet's own fields.**
  `Code` and `Status` name the concept and lifecycle of the record itself, so
  `section.code` and `adherence.status` are not those things. This was settled
  on 29 August — "leave all six unmapped". Concepts that are genuinely about an
  inner structure — `LotNumber`, `BodyLocation`, `Note` — do map when nested.
- **It proposes nothing for an element name the glossary does not cover.**
  Around 265 element names have no candidate: `date`, `type`, `role`, `period`,
  `value`, `statusReason`. Most are model-specific and correctly unmapped, but
  the tail of the read-through lists them, and a name recurring across many
  models is a hint that the glossary is missing a term.

## 3. Review

Open `input/glossary_mappings.csv` in Excel, sort or filter on `Status`, and
change each `proposed` to either `confirmed` or `rejected`. Leaving it as
`proposed` is a valid state — it means undecided, and nothing acts on it.

To accept a proposal but with a different concept, edit `GlossaryCode` and set
`Status` to `confirmed`.

Deciding by `GlossaryCode` rather than row is usually faster: `Status` is
proposed for 22 models at once and `BusinessIdentifier` for 20, and those are
one judgement each, not twenty-two.

> Save as CSV, keeping the `;` delimiter and UTF-8. Excel will offer to change
> the format; decline.

## 4. Merge into the workbooks

```bash
python merge_mappings_to_xlsx.py --dry-run   # what would change
python merge_mappings_to_xlsx.py            # write it
```

Only `confirmed` rows are merged, and only those pointing at an approved
glossary term. Each one is written into the `Code` column of
the matching element, and `Relationship` is set to `equivalent` if it is empty.

If an element already carries a *different* code, the merge reports it and
changes nothing. That is not a stale value to be overwritten — the workbook is
the source, so a difference is a real disagreement between two decisions, and
it wants a person. `--force` resolves it in the CSV's favour; use it only after
looking.

## 5. Into the StructureDefinitions

```bash
python import_logical_model_xlsx.py   # workbooks -> models/generated/
python build_content.py               # and into the site's own copies
```

`import_logical_model_xlsx.py` writes `element.code` from the workbook's `Code`
column, so the models under `models/generated/` — the ones handed over for
publication — carry the mapping:

```json
"code": [{
  "system": "http://example.org/CodeSystem/BeSafeShareGlossary",
  "code": "BusinessIdentifier"
}]
```

The `system` is looked up per term: a term belongs to either the clinical or the
operational CodeSystem, and naming the wrong one does not resolve. A term in
neither is reported and its code left off, rather than written with a guessed
system.

`build_content.py` separately applies the mappings to `_resources/models/`,
which is what the site renders. Both need running: one is what gets published,
the other is what gets displayed.

> **The CodeSystem canonicals are still `http://example.org/...`.** They are
> placeholders, and they will be published inside every StructureDefinition
> that carries a mapping. They want replacing with the real eHealth or RIZIV
> canonicals before handover. Changing them in the generated CodeSystems is
> enough — the lookup reads them from there.

---

## Why nothing leaks

A proposal sitting in the CSV cannot reach the site or the StructureDefinitions:
`add_glossary_mappings.py` and `export_logical_model_xlsx.py` both skip any row
whose `Status` is not `confirmed`. A blank `Status` counts as confirmed, which
is what the rows written before that column existed are.

`import_logical_model_xlsx.py` regenerates the CSV from the workbooks, and
carries `proposed` and `rejected` rows across unchanged while doing so. Without
that, one regeneration would erase every pending decision — and a rejected row
returning as a fresh proposal would put a settled question back to the reviewer.

## Where the state lives

| File | Role |
|---|---|
| `input/models/` | published StructureDefinitions, downstream of eHealth |
| `models/xls/*.xlsx` | the workbooks — **where a mapping is authored** |
| `input/glossary_mappings.csv` | proposals and decisions, one row per element |
| `models/generated/*.json` | models rebuilt from the workbooks, for publishing |
| `glossary-changes/` | read-throughs; working documents, not sources |

## Current state

As of 4 September 2026, across 41 workbooks and 602 elements:

- **193 confirmed** mappings, in 37 of 41 models
- every target an approved glossary term
- **5 still proposed**
- around 265 element names with no candidate concept

193 of 643 elements carry an `element.code` in the generated
StructureDefinitions.
