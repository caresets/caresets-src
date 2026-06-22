# BeSafeShare Documentation Site

Source for the BeSafeShare glossary and logical data model documentation, built with Jekyll and the [Just-the-docs](https://pmarsceill.github.io/just-the-docs) theme.

## Prerequisites

- **Ruby** (>= 2.7) and **Bundler** (`gem install bundler`)
- **Node.js** (>= 18) — only needed for encrypted deployments
- **Python 3** — only needed for glossary generation scripts

## Local Development

Install dependencies:

```sh
bundle install
```

Run the local dev server:

```sh
bundle exec jekyll serve --config _config.yml,_config_local.yml
```

The site will be available at `http://localhost:8002`.

## Building for Production

```sh
bundle exec jekyll build
```

The built site is output to `_site/`.

## Encrypted Preview Deployment

To build a password-protected version of the site and deploy it to the [caresets/caresets](https://github.com/caresets/caresets) repo (serves at `caresets.github.io/caresets`):

1. Install StatiCrypt: `npm install -g staticrypt`
2. Run the deploy script:

```sh
# Uses default password
deploy.bat

# Or specify a custom password
deploy.bat mypassword
```

This builds with the preview config, encrypts all HTML pages (except the root index), and outputs to `_site/`. You then push the contents of `_site/` to the `caresets/caresets` repo.

## Glossary Generation

Two glossaries are maintained in CSV and compiled to FHIR CodeSystem JSON:

| Glossary | Current CSV | Proposed-updates CSV | Generated JSON |
|---|---|---|---|
| clinical | `ClinicalGlossary.csv` | `ClinicalGlossary-proposed.csv` | `_resources/glossary/CodeSystem-glossary.json` |
| operational | `OperationalGlossary.csv` | `OperationalGlossary-proposed.csv` | `_resources/glossary/CodeSystem-operational-glossary.json` |

**Only the *current* CSV is the source of truth for the JSON.** The proposed CSV is a staging area for new or changed terms awaiting review. Terms are append-only — the only way to remove one is to mark it `rejected` first and physically remove it in a later cycle.

### Standard workflow (proposed → review → accept)

1. Add new terms (or proposed updates) to e.g. `OperationalGlossary-proposed.csv`. New terms get `Status: proposed`.
2. Preview what merging would change:

   ```sh
   python generate_glossary.py operational --preview
   ```

   Writes a `*-preview.md` file under `glossary-changes/` showing inline track-changes diff (word-level `<del>`/`<ins>`) of every added/modified term. No file is modified.

3. Review the markdown diff. If happy, accept:

   ```sh
   python generate_glossary.py operational --accept
   ```

   Merges proposed rows into the current CSV (skipping any code that already exists with different fields — those rows stay in proposed for you to resolve), clears proposed, regenerates the JSON, and writes a non-preview diff report to `glossary-changes/`. Backs up both CSVs and the previous JSON.

### Direct edits and other commands

```sh
python generate_glossary.py                       # current.csv -> JSON, all glossaries
python generate_glossary.py operational           # one glossary
python generate_glossary.py --to-csv              # JSON -> current.csv (re-extract; rarely needed)
python generate_glossary.py --list                # list configured glossaries
python generate_glossary.py --mode incremental    # only append new codes (rare)
```

Direct edits to the current CSV go straight to the JSON when you run without flags. Every run that changes the JSON writes a diff report to `glossary-changes/{glossary}-{timestamp}.md`.

### Diff report rendering

Reports use inline `<del>`/`<ins>` tags so altered words show as strikethrough/underline in any markdown viewer (GitHub, VS Code preview). Whole-paragraph rewrites still work — they just appear as a single deletion + insertion.

## Glossary Mappings & ConceptMap

The `glossary_mappings.csv` file defines how glossary codes map to elements in the FHIR StructureDefinitions (logical models). Each row maps a model element to a glossary term:

```
Model;ElementSuffix;GlossaryCode
StructureDefinition-be-model-vaccination.json;patient;Patient
StructureDefinition-be-model-vaccination.json;route;Route
```

**Add codes to model elements** — writes `element.code` entries directly into the StructureDefinition JSON files:

```sh
python add_glossary_mappings.py
```

**Generate a ConceptMap** — creates a FHIR ConceptMap resource instead of modifying the models:

```sh
python add_glossary_mappings.py --conceptmap
```

Output: `_resources/glossary/ConceptMap-model-to-glossary.json`

You can specify a different mappings CSV or output path:

```sh
python add_glossary_mappings.py --conceptmap --csv my_mappings.csv --output path/to/output.json
```

## Project Structure

```
en/, fr/, nl/        — Page content by language
_config.yml          — Main Jekyll config
_config_local.yml    — Local dev overrides (port 8002, no baseurl)
_config_preview.yml  — Preview/encrypted build config
_data/               — Language and model definitions
_includes/           — Reusable HTML components
_layouts/            — Page templates (glossary, logical-model)
_resources/          — Generated FHIR resources and data models
_sass/               — Custom stylesheets
assets/              — CSS, JS, images
deploy.bat           — Build + encrypt script (Windows)
encrypt-site.bat     — Encrypt-only script (Windows)
GlossaryTerms.csv    — Clinical glossary source data
OperationalGlossary.csv — Operational glossary source data
```

