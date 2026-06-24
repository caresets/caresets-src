# backups/ — versioned snapshots of input/

Each `v<VERSION>/` folder is a complete copy of [`../input/`](../input/) as it was
for that release version (the version comes from the `VERSION` file).

- **Created automatically** on every publish (the GitHub Action runs
  `backup_content.py` and commits the snapshot here).
- **One snapshot per version.** Re-publishing the same version refreshes its
  folder; bumping `VERSION` creates a new one and keeps the old.

Do not edit these by hand — they are managed by `backup_content.py`.

## Restore an older version

```sh
python backup_content.py --list          # list versions
python backup_content.py --restore 0.1   # copy backups/v0.1/ back into input/
python build_content.py                  # regenerate the site content
```

Restoring first saves your current `input/` to `backups/_pre-restore/` (git-ignored)
so you can undo.
