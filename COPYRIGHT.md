# Copyright and licensing

This repository holds two different kinds of thing, under two different terms.

## Code — AGPLv3

The software is licensed under the GNU Affero General Public License v3.0. The full text
is in [LICENSE](LICENSE).

Copyright © 2026 Simon Redfern.

This covers everything that makes the site work:

- `scripts/` — the image pipeline, the rehype plugin, the migration scripts
- `src/lib/components/` — the Svelte components
- `src/routes/`, `src/app.css`, `src/app.html`
- `svelte.config.js`, `vite.config.js`, `package.json`
- `.github/workflows/`

## Content — all rights reserved

Everything that *is* the site, rather than what renders it, is **not** open licensed:

- `src/content/` — the page text
- `src/lib/data/` — gigs, navigation, photo metadata and captions
- `media/` — all photographs
- `static/favicon.png`

Copyright © 3rd Party Influence and the individual photographers. All rights reserved.
Not covered by the AGPL. Please ask before reusing any of it.

### Photograph filenames carry the rights holder

Every image file is named `<rights-holder>_<description>.<ext>`, and that prefix survives
all the way to the files served from the site. Someone who saves a photo off a page gets
`falk-wieland_no-9995-group-from-back-wider-1280.avif`, not `img-9995.jpg` — the credit
travels with the file instead of being left behind in a caption.

| Photos | Prefix |
|---|---|
| 45 | `3pi_` |
| 7 | `falk-wieland_` |
| 6 | `paul-van-dorsten_` |
| 5 | `unknown_` |
| 3 | `lisa-knolle_` |
| 1 | `joranalogue_` |
| 1 | `leeds-media-services_` |
| 1 | `marlene-berhmann_` |
| 1 | `roberta-santanna_` |
| 1 | `soma-laboratory_` |
| 1 | `under-the-radar_` |

`3pi_` is the band's own work. `unknown_` means the photographer is genuinely not known —
mostly press photos supplied by guests of the *Artists, Activists and Audiences* series.
Everything else names the rights holder.

These are **not** ours to relicense and the AGPL does not apply to them:

| Photos | Rights holder |
|---|---|
| 7 | Falk Wieland |
| 6 | Paul van Dorsten ([@by_paulu](https://www.instagram.com/by_pauluz/)) |
| 3 | Lisa Knolle |
| 1 | Marlene Berhmann |
| 1 | [Under The Radar](https://www.undertheradarmag.com/) |
| 1 | Leeds Media Services |
| 1 | Roberta Santanna |
| 1 | [Joranalogue](https://joranalogue.com/) (product photo) |
| 1 | [SOMA Laboratory](https://somasynths.com/) (product photo) |

Per-image credit is also recorded in `src/lib/data/photos.json` as `credit` and
`creditUrl`, and rendered under the photo on the site. If you are one of these rights
holders and want a credit corrected or an image removed, please get in touch.

To regenerate the prefix table:

```sh
node -e "const p=require('./src/lib/data/photos.json');
const c={}; Object.keys(p).forEach(k=>{const o=k.split('_')[0]; c[o]=(c[o]||0)+1});
Object.entries(c).sort((a,b)=>b[1]-a[1]).forEach(([k,n])=>console.log(n,k))"
```

## Why the split

The AGPL grants anyone the right to redistribute and modify. That is the intent for the
code. It is not something we are in a position to grant for photographs taken by other
people, and it is not what we want for the band's own words and pictures.
