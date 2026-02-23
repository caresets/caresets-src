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

Generates FHIR CodeSystem JSON files from the CSV source data (`GlossaryTerms.csv`, `OperationalGlossary.csv`).

**Full mode** — replaces the entire CodeSystem from the CSV (use when the CSV is the complete source of truth):

```sh
python generate_glossary.py --mode full
python generate_glossary.py --mode full clinical    # clinical glossary only
python generate_glossary.py --mode full operational  # operational glossary only
```

**Incremental mode** — only adds new terms that don't already exist in the CodeSystem JSON (use when appending new rows to the CSV):

```sh
python generate_glossary.py --mode incremental
python generate_glossary.py --mode incremental clinical
```

List available glossaries:

```sh
python generate_glossary.py --list
```

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

