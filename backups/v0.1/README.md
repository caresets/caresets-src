# input/ — the content you edit

**This folder is the single source of truth for the site's content.** If you are
maintaining the glossary or the logical models, everything you need to edit is
here. You should not need to touch any other folder.

Everything under `_resources/` is **generated** from this folder — do not edit it
by hand; your changes there will be overwritten.

## What's in here

| File / folder | What it is | How to edit |
|---|---|---|
| `ClinicalGlossary.csv` | The clinical glossary (terms + definitions) | Edit rows directly, `;`-separated |
| `OperationalGlossary.csv` | The operational glossary | Edit rows directly, `;`-separated |
| `glossary_mappings.csv` | Links model elements to glossary concepts | `Model;ElementSuffix;GlossaryCode` |
| `models/` | The logical models (FHIR StructureDefinition JSON) | Add/edit/remove `StructureDefinition-*.json` |
| `models/draft/` | Work-in-progress models, **not** published yet | Move a file up to `models/` to publish it |

## After you edit anything here

Run one command from the project root to regenerate the site content:

```sh
python build_content.py
```

That syncs the models, rebuilds the glossary CodeSystems, and applies the
mappings. Then preview locally (`bundle exec jekyll serve --config _config.yml,_config_local.yml --watch`)
or just commit and push — the GitHub Action does the rest.

## Backups

Every published version is snapshotted to `../backups/v<VERSION>/`. To restore an
older version's content:

```sh
python backup_content.py --list          # see available versions
python backup_content.py --restore 0.1   # bring v0.1 back into input/
python build_content.py                  # regenerate from the restored content
```

See the main [README](../README.md) for the full procedure.
