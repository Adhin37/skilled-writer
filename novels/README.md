# novels/

One directory per novel. `_template/` is the scaffold — copy it, never write into it.

`/novel-new` does the copying and fills it in from an interview. To do it by hand:

```
cp -r novels/_template novels/my-slug
```

Then edit `novels/my-slug/novel.md` and run `/novel-plan`.
