# input/ — sources, and things that arrive here

Not everything in this folder is a source. Two files are, one is a review
surface, and the rest is either produced by a script or arrives from upstream.
Editing a generated file loses the edit on the next build, so the distinction
matters.

## What you edit

| File | What it is |
|---|---|
| `Glossaire CareSets V1.xlsx` | **The clinical glossary.** The one source for it: terms, definitions and descriptions in FR, NL and EN. Only rows marked `active` are published. |
| `OperationalGlossary.csv` | **The operational glossary.** Hand-maintained, `;`-separated. It has no workbook — the workbook's operational sheet holds 2 rows against this file's 19 terms. |

Model workbooks are **not** here. They live in `../models/xls/`, one per model.

## What you review

| File | What it is |
|---|---|
| `glossary_mappings.csv` | Model element → glossary concept. Both a review surface and a generated file: `propose_model_mappings.py` adds proposals, you set `Status` to `confirmed` or `rejected`, and `import_logical_model_xlsx.py` rewrites it from the workbooks while carrying undecided rows across. Edit the `Status` and `GlossaryCode` columns; do not hand-add rows expecting them to survive unless you also put the mapping in a workbook. See [MAPPING-PROCEDURE.md](../MAPPING-PROCEDURE.md). |

## What is generated — do not edit

| File | Written by |
|---|---|
| `ClinicalGlossary.csv` | `import_glossary_xlsx.py`, from the workbook. **Editing it is lost** on the next `build_content.py` for any term the workbook also holds. |

## What arrives from upstream — do not edit

| Folder | Where it comes from |
|---|---|
| `models/` | The published StructureDefinitions, downloaded by `fetch_ehealth_models.py --apply` or imported by `import_models_zip.py`. This folder is *downstream* of publication, not a place to author a model. |
| `models/draft/` | Models not yet published. Excluded from the site and from the default workbook export; `--include-draft` picks them up. |

To change a model, edit its workbook in `../models/xls/`, run
`import_logical_model_xlsx.py`, and publish what lands in `../models/generated/`.
The change comes back here when it has been published upstream.

## After you edit anything here

```sh
python build_content.py
```

That converts the glossary workbook, syncs the models, rebuilds the glossary
CodeSystems, and rebuilds the model-to-glossary ConceptMap. Then preview
(`bundle exec jekyll serve --config _config.yml,_config_local.yml --watch`) or
commit and push.

If you changed mappings, that is a different sequence — see
[MAPPING-PROCEDURE.md](../MAPPING-PROCEDURE.md).

## Backups

Every published version is snapshotted to `../archive/v<VERSION>/`:

```sh
python backup_content.py --list          # available versions
python backup_content.py --restore 0.1   # bring v0.1 back into input/
python build_content.py                  # regenerate from it
```

See the main [README](../README.md) for the full procedure.
