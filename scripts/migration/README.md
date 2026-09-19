# Migration scripts

One-shot tooling that lifted the content out of Super.so in September 2026. Kept for
provenance and in case anything needs re-extracting. **Not part of the build.**

They expect the 12 fetched Super HTML pages in the same directory, as `page.html`
(the homepage) and `p_<slug>.html`:

```sh
curl -sSL https://3pi.tv/ -o page.html
curl -sSL https://3pi.tv/module-co2e -o p_module-co2e.html   # ...etc
```

Then, in order:

| Script | Does |
|---|---|
| `extract.py` | Walks the `notion-root` article in each page, emits markdown + `out/images.json` |
| `download.py` | Pulls every image at 1920px from `images.spr.so` into `media/web/`, slugifying filenames |
| `finalize.py` | Rewrites photo ids, injects component imports, writes `src/content/` and the data files |

`extract.py` maps Notion block types to markdown and components: `notion-text` to
paragraphs, `notion-image` to `<Photo>`, `notion-embed` to `<Embed>`, `notion-column-list`
to `<Columns>`/`<Column>`, headings to `##`/`###`.

Two bits of content were deliberately turned into data rather than prose: the homepage's
"Next Gig" heading and the hand-written list on `/gig-archive` both became
`src/lib/data/gigs.json`.

## Careful

Re-running `finalize.py` would regenerate `src/content/` and `photos.json` from the
original Super HTML, which predates the `<rights-holder>_` filename prefixes. It would
undo them. If you ever need to re-extract, re-apply the prefixes afterwards — see
[COPYRIGHT.md](../../COPYRIGHT.md).
