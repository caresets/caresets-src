# Mapping model elements to the Common Glossary

How a logical model element gets tied to a glossary concept, from the published
StructureDefinition to the workbook an analyst edits.

The short version: **the workbook is where a mapping lives; the CSV is where a
mapping is proposed and decided.** Nothing acts on a mapping until somebody has
marked it confirmed.

## What to run

After editing `input/glossary_mappings.csv` — the ordinary case:

```bash
python merge_mappings_to_xlsx.py      # confirmed mappings -> the workbooks
python import_logical_model_xlsx.py   # workbooks -> models/generated/
python build_content.py               # -> the site's ConceptMap and glossary
```

After editing the **glossary workbook** or a **model workbook**, `build_content.py`
alone is enough — it re-imports the glossary and rebuilds everything served.

Before handing mappings to an eHealth IG:

```bash
python make_conceptmap_fsh.py --canonical-base <the real base>
```

Every one of these is safe to re-run. They act only on what has changed, and
each says what it did; a run that finds nothing to do prints so and writes
nothing. `--dry-run` on any of them shows the effect first.

---

## The six steps

```
  1  fetch        published StructureDefinitions  ->  models/xls/*.xlsx
  2  propose      new mappings          ->  input/glossary_mappings.csv  (Status = proposed)
  3  review       a person sets Status  ->  confirmed  or  rejected
  4  merge        confirmed mappings    ->  the workbooks' Code column
  5  publish      confirmed mappings    ->  ConceptMap-model-to-glossary.json
  6  onboard      the same mappings     ->  one .fsh per eHealth IG
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
mappings CSV. The `Code` column is where a mapping is authored; it is not
written back onto the model.

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

## 5. Into the ConceptMap

```bash
python import_logical_model_xlsx.py   # workbooks -> models/generated/
python build_content.py               # and the ConceptMap the site serves
```

The mapping is published as a **ConceptMap**, not written onto the model.
`_resources/glossary/ConceptMap-model-to-glossary.json` carries one group per
model, each group naming the model's canonical as its source and the glossary
CodeSystem as its target:

```
source   .../StructureDefinition/BeModelReferralPrescription
target   .../CodeSystem/BeSafeShareGlossary
  BeModelReferralPrescription.author        -> Recorder
  BeModelReferralPrescription.identifier    -> BusinessIdentifier
```

### Why not element.code

Putting the mapping in `element.code` writes it *inside* the
StructureDefinition. Three things follow, and all of them are unwanted:

- the models handed over for publication are no longer the models that were
  imported, so a reviewer cannot diff them against what eHealth published;
- a change of mapping becomes a change of model, with a model version bump for
  what is an editorial decision about the glossary;
- the mapping cannot be versioned or republished on its own.

A ConceptMap keeps the mapping as its own resource. The StructureDefinitions
stay exactly as published — verified: all 41 served models are identical to the
imported ones — and the mapping is reviewed and released separately.

Element codes in the ConceptMap are the real `ElementDefinition` paths, read
from the models rather than assembled from the CSV. An element's path is not
always the model's name — `BeModelVaccination`'s elements live under
`be-model-vaccination` — so a path built by hand would not resolve.

> **The CodeSystem and ConceptMap canonicals are still `http://example.org/...`.**
> They are placeholders and want replacing with the real eHealth or RIZIV
> canonicals before handover.

---

## 6. Onboarding into the eHealth IGs

```bash
python make_conceptmap_fsh.py --dry-run
python make_conceptmap_fsh.py --canonical-base https://www.ehealth.fgov.be/standards/fhir
```

The site's single ConceptMap cannot be handed to anyone: the mapped models come
from **14 different implementation guides**, and each guide publishes only its
own. This splits the same confirmed mappings by guide and writes
`exports/conceptmaps/<ig>/` holding three files:

| File | Goes into that guide's |
|---|---|
| `ConceptMap-<Ig>ModelToGlossary.fsh` | `input/fsh/maps/` |
| `map-<ig>-glossary.xml` | `input/pagecontent/` |
| `sushi-config-pages.yaml` | `sushi-config.yaml`, merged under `pages:` |

FSH rather than a ConceptMap JSON in `input/resources/`, because the eHealth
guides are sushi projects: a JSON resource is a foreign object in a workflow
where everything else is authored and reviewed as FSH.

The display page is generated from the same rows as the ConceptMap, so the two
cannot drift. In the HL7 Europe proof of concept this pattern follows
([hl7-eu/base](https://github.com/hl7-eu/base/tree/mappings), branch
`mappings`) they are separate hand-maintained artefacts — fourteen display
pages against one ConceptMap — and have already drifted.

Two things to know before sending:

- `--canonical-base` must be set. The default is `http://example.org` and the
  script warns when it has been left there.
- `--r5` emits `relationship` instead of R4's `equivalence`. The models are
  4.0.1, so R4 is the default; check the version of the guide receiving it.

The `unpublished` folder holds the draft models, which belong to no guide. It
is there so those mappings are visible rather than silently dropped; it is not
for onboarding.

## How the site displays it

The model table reads the glossary column from the ConceptMap, since the
mapping is no longer in the model. Where an element *does* carry its own
`element.code`, that wins: a model stating its own mapping makes a first-hand
claim about itself, where the ConceptMap is a statement made about it from
outside. A missing ConceptMap costs the glossary column, not the table.

## Why nothing leaks

A proposal sitting in the CSV cannot reach the ConceptMap or the workbooks:
`make_conceptmap.py` and `export_logical_model_xlsx.py` both skip any row
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
| `models/generated/*.json` | models rebuilt from the workbooks, for publishing — no mapping written into them |
| `_resources/glossary/ConceptMap-model-to-glossary.json` | **the mapping itself**, published as its own resource |
| `glossary-changes/` | read-throughs; working documents, not sources |

## Current state

As of 4 September 2026, across 41 workbooks and 602 elements:

- **196 confirmed** mappings, in 37 of 41 models
- every target an approved glossary term
- **5 still proposed**
- around 265 element names with no candidate concept

196 of 643 elements are mapped, in 37 groups of the ConceptMap. The
StructureDefinitions themselves are unchanged from what was imported.
