# BeSafeShare Documentation Site

Source for the BeSafeShare **glossary** and **logical data model** documentation, built with Jekyll and the [Just-the-docs](https://pmarsceill.github.io/just-the-docs) theme.

## TL;DR for maintainers

**To update the site you only edit files in [`input/`](input/) — nothing else, no tools to install.** You can do it entirely in the GitHub web interface:

1. Open the [`input/`](input/) folder on GitHub and **add, edit, or delete** a file (a glossary CSV, a model JSON, or the mappings CSV).
2. **Commit to the `main` branch.**

That's it. The **GitHub Action runs the Python and publishes the site automatically** — you never have to run anything yourself. Everything under `_resources/` is *generated* from `input/`; never edit it by hand.

| Content | What you edit in `input/` | Generated for you (don't touch) |
|---|---|---|
| Glossaries (clinical + operational) | `ClinicalGlossary.csv`, `OperationalGlossary.csv` | `_resources/glossary/CodeSystem-*.json` |
| Logical models | `models/StructureDefinition-*.json` | `_resources/models/` (served copy) |
| Concept mappings (model element → glossary concept) | `glossary_mappings.csv` | `element.code` in the served models |

---

## Update procedure

### 1. Edit the content in `input/`

In the GitHub web UI (or locally, if you prefer):

- **Glossaries** — edit `input/ClinicalGlossary.csv` and/or `input/OperationalGlossary.csv` (`;`-separated).
- **Logical models** — add/edit/remove `input/models/StructureDefinition-*.json` (FHIR `kind: logical`). Work-in-progress models go in `input/models/draft/` and are **not** published until moved up to `input/models/`.
- **Mappings** — edit `input/glossary_mappings.csv` (`Model;ElementSuffix;GlossaryCode`).

See [`input/README.md`](input/README.md) for a field-by-field guide.

### 2. Commit to `main` — the GitHub Action does the rest

Committing to `main` triggers [`.github/workflows/publish.yml`](.github/workflows/publish.yml). What it does depends on **what you changed**:

- **You edited something in `input/`** (or `VERSION`) → it runs the Python: regenerates `_resources/` (models, glossary, mappings), **snapshots `input/` to `backups/v<VERSION>/`**, commits both back, then builds and deploys.
- **You edited anything else** (a page, layout, CSS…) → it skips Python and backups entirely, and just builds and deploys what's committed.

Either way it ends by:
- deploying the site to the **`gh-pages`** branch → **<https://caresets.github.io/caresets-src/>**,
- publishing a deployable **`riziv-inami-site.zip`** at **<https://caresets.github.io/caresets-src/riziv-inami-site.zip>**.

You do **not** run any Python locally — that's the Action's job. (Pull requests are validated by [`ci.yml`](.github/workflows/ci.yml), which builds but does not deploy.)

> **One-time setup:** after the first run creates the `gh-pages` branch, set **Settings → Pages → Source → `gh-pages` branch**. The baseurl (`/caresets-src`) is set in `_config.yml` and the workflow; both are configurable (see the workflow header).

### When you cut a release

Bump `VERSION` (and `content_version` + `footer_content` in `_config.yml`) — also editable in the browser. The version names the backup snapshot (`backups/v<VERSION>/`).

### Optional: preview locally before committing

Only if you have Ruby + Python installed and want to see changes before pushing:

```sh
python build_content.py    # regenerate _resources/ from input/
bundle exec jekyll serve --config _config.yml,_config_local.yml --watch
```

Open <http://localhost:8002> and hard-refresh (**Ctrl+Shift+R**).

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
_config.yml            — main Jekyll config (production: baseurl /caresets-src)
_config_local.yml      — local dev overrides (port 8002, empty baseurl)
_config_preview.yml    — preview/encrypted build config
_data/, _includes/, _layouts/, _sass/, assets/ — theme, templates, CSS/JS, images
_resources/glossary/   — GENERATED CodeSystem + ConceptMap JSON
_resources/models/     — GENERATED served copy of input/models/ (git-ignored)
```

### Generated / disposable (not source — safe to delete, regenerated by the scripts/build)

`_site/`, `_site.zip`, `__pycache__/`, `.jekyll-cache/`, `glossary-changes/`, `_resources/models/`, `*.backup.json`, `*.backup.csv`, and `backups/_pre-restore/`.
