# BeSafeShare Documentation Site

Source for the BeSafeShare **glossary** and **logical data model** documentation, built with Jekyll and the [Just-the-docs](https://pmarsceill.github.io/just-the-docs) theme.

## TL;DR for maintainers

**Everything you edit lives in [`input/`](input/).** Then run one command and push:

```sh
python build_content.py     # regenerate the site content from input/
git commit -am "update content" && git push   # the GitHub Action publishes it
```

Everything under `_resources/` is **generated** from `input/` — never edit it by hand.

| Content | Source of truth (edit here) | Generated artifact (don't edit) |
|---|---|---|
| Glossaries (clinical + operational) | `input/ClinicalGlossary.csv`, `input/OperationalGlossary.csv` | `_resources/glossary/CodeSystem-*.json` |
| Logical models | `input/models/StructureDefinition-*.json` | `_resources/models/` (served copy) |
| Concept mappings (model element → glossary concept) | `input/glossary_mappings.csv` | `element.code` in the served models |

---

## Update procedure (end to end)

### 1. Edit the content in `input/`

- **Glossaries** — edit `input/ClinicalGlossary.csv` and/or `input/OperationalGlossary.csv` (`;`-separated).
- **Logical models** — add/edit/remove `input/models/StructureDefinition-*.json` (FHIR `kind: logical`). Work-in-progress models go in `input/models/draft/` and are **not** published until moved up to `input/models/`.
- **Mappings** — edit `input/glossary_mappings.csv` (`Model;ElementSuffix;GlossaryCode`).

See [`input/README.md`](input/README.md) for a field-by-field guide.

### 2. Regenerate the served content

```sh
python build_content.py
```

This one command (1) syncs `input/models/` → `_resources/models/`, (2) compiles the glossary CodeSystems, and (3) applies the mappings into the served models. Run it after **any** change in `input/`.

### 3. Bump the version

Update `VERSION`, and `content_version` + `footer_content` in `_config.yml`. (The version drives the per-version backup folder.)

### 4. Preview locally

```sh
bundle exec jekyll serve --config _config.yml,_config_local.yml --watch
```

Open <http://localhost:8002>, hard-refresh (**Ctrl+Shift+R**), and confirm the glossary, model list, and mappings look right.

> The models list is baked into the page at **build time**, so it only reflects what's in `_resources/models/` after `build_content.py` has run and the site is rebuilt.

### 5. Publish — just push to `main`

[`.github/workflows/publish.yml`](.github/workflows/publish.yml) then automatically:
1. runs `build_content.py`,
2. **snapshots `input/` to `backups/v<VERSION>/`** and commits it,
3. builds the site and deploys it to the **`gh-pages`** branch,
4. packages a deployable **`riziv-inami-site.zip`**, published alongside the site at:

**<https://caresets.github.io/glossary/riziv-inami-site.zip>**

(URL follows the gh-pages baseurl. Both baseurls are configurable via the workflow's `workflow_dispatch` inputs or repo variables — see the workflow header. The zip is also kept as a workflow artifact.)

**One-time setup:** after the first run creates the `gh-pages` branch, set **Settings → Pages → source → `gh-pages` branch**.

#### Manual encrypted preview (optional)

To build a password-protected copy for the [`caresets/caresets`](https://github.com/caresets/caresets) preview repo (`caresets.github.io/caresets`):

```sh
deploy.bat            # builds + encrypts (default password: 25caresets)
deploy.bat mypass     # or a custom password
```

Then push the contents of `_site/` to that repo.

---

## Backups & versioning

Every published version is snapshotted to `backups/v<VERSION>/` (one folder per version, refreshed if the same version is re-published). This happens automatically on publish; you can also do it by hand:

```sh
python backup_content.py            # snapshot input/ -> backups/v<VERSION>/
python backup_content.py --list     # list available version backups
python backup_content.py --restore 0.1   # restore backups/v0.1/ into input/
```

Restoring first saves the current `input/` to `backups/_pre-restore/` (git-ignored) so you can undo, then run `python build_content.py` to regenerate. See [`backups/README.md`](backups/README.md).

---

## Prerequisites

- **Ruby** (>= 2.7) and **Bundler** (`gem install bundler`) — `bundle install`
- **Python 3** — `build_content.py`, `backup_content.py`, and the glossary scripts (stdlib only, no pip install)
- **Node.js** (>= 18) + **StatiCrypt** (`npm install -g staticrypt`) — only for the encrypted preview

---

## Glossary generation (details)

Two glossaries are maintained in CSV and compiled to FHIR CodeSystem JSON:

| Glossary | Source CSV | Generated JSON |
|---|---|---|
| clinical | `input/ClinicalGlossary.csv` | `_resources/glossary/CodeSystem-glossary.json` |
| operational | `input/OperationalGlossary.csv` | `_resources/glossary/CodeSystem-operational-glossary.json` |

Terms are append-only — to remove one, mark it `rejected`, then physically delete it in a later cycle.

### Commands

```sh
python generate_glossary.py            # all glossaries: input CSV -> JSON
python generate_glossary.py --list     # list configured glossaries
python generate_glossary.py --to-csv   # JSON -> input CSV (re-extract; rarely needed)
```

Every run that changes a JSON writes a diff report to `glossary-changes/{glossary}-{timestamp}.md` and backs up the previous CSV/JSON.

---

## Glossary mappings (details)

`input/glossary_mappings.csv` maps model elements to glossary terms:

```
Model;ElementSuffix;GlossaryCode
StructureDefinition-be-model-vaccination.json;patient;Patient
StructureDefinition-be-model-vaccination.json;route;Route
```

`ElementSuffix` matches any element whose `id`/`path` ends with `.<suffix>`; `GlossaryCode` is a concept `code` from the glossary CodeSystem. `build_content.py` applies these automatically. To run the mapping step alone:

```sh
python add_glossary_mappings.py                                   # write element.code into the served models
python add_glossary_mappings.py --conceptmap                      # build a ConceptMap instead
python add_glossary_mappings.py --csv my.csv --output out.json    # custom paths
```

The script is idempotent (skips codes already present) and emits the glossary system `http://example.org/CodeSystem/BeSafeShareGlossary`. Keep the `Model` column in sync with the filenames in `input/models/` — rows pointing at missing files are silently skipped.

---

## Project structure

```
input/                 — ★ SOURCE OF TRUTH — everything maintainers edit
  ClinicalGlossary.csv, OperationalGlossary.csv (+ -proposed.csv)
  glossary_mappings.csv
  models/              — logical model StructureDefinition JSON (draft/ = unpublished)
backups/               — versioned snapshots of input/ (backups/v<VERSION>/)
build_content.py       — regenerate _resources/ from input/ (run after editing)
backup_content.py      — snapshot / list / restore input/ versions
generate_glossary.py   — glossary CSV <-> CodeSystem JSON
add_glossary_mappings.py — apply mappings to models / build ConceptMap
deploy.bat             — build + encrypt for the manual preview (Windows)
en/, fr/, nl/          — page content by language (new models appear automatically)
_config.yml            — main Jekyll config (production: baseurl /caresets)
_config_local.yml      — local dev overrides (port 8002, empty baseurl)
_config_preview.yml    — preview/encrypted build config
_data/, _includes/, _layouts/, _sass/, assets/ — theme, templates, CSS/JS, images
_resources/glossary/   — GENERATED CodeSystem + ConceptMap JSON
_resources/models/     — GENERATED served copy of input/models/ (git-ignored)
```

### Generated / disposable (not source — safe to delete, regenerated by the scripts/build)

`_site/`, `_site.zip`, `__pycache__/`, `.jekyll-cache/`, `glossary-changes/`, `_resources/models/`, `*.backup.json`, `*.backup.csv`, and `backups/_pre-restore/`.
