# novels/

One directory per novel. `_template/` is the scaffold — copy it, never write into it.

`/novel-new` does the copying and fills it in from an interview. To do it by hand:

```bash
python3 scripts/sw.py newnovel my-slug         # any OS, any shell
```

It refuses to overwrite an existing novel and prints the tree it created. Without Python:

```bash
cp -r novels/_template novels/my-slug          # macOS / Linux / Git Bash
```

```powershell
Copy-Item -Recurse novels\_template novels\my-slug   # Windows PowerShell
```

Then edit `novels/my-slug/novel.md` and run `/novel-plan`.

## These directories are not committed

`.gitignore` excludes everything here except `_template/` and this file. Your manuscript is
yours, and keeping it out of the toolkit repo means you can pull toolkit updates without
merge conflicts in your prose.

If you do want a novel under version control, the clean option is its own repository. The
quick option is `git add -f novels/my-slug`.
