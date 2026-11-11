# Swoozh Icons

1,778 fashion and e-commerce icons, each with an **outline** and a **filled** style, on a 24 px grid with a 1.5 px line.

| Package | Contents |
| --- | --- |
| `@swoozh/icons` | SVG files, sprites, path data, `icons.json` metadata |
| `@swoozh/icons-react` | React components (`<ShoppingBag variant="filled" />`) |
| `@swoozh/icons-vue` | Vue 3 components |
| `@swoozh/icons-svelte` | Svelte `<Icon icon={ShoppingBag} />` |
| `@swoozh/icons-element` | `<swoozh-icon name="shopping-bag">` web component |
| `@swoozh/icons-font` | Icon font (WOFF2/TTF) + CSS classes (`swz swz-shopping-bag`) |
| `packages/elm` | Elm module `SwoozhIcons` |

The icon browser and docs are published at https://richardwalander.github.io/swoozh-icons/ (built by `.github/workflows/pages.yml` on every push to `master`). Locally, after a build:

```bash
npm run build && python3 -m http.server 8642 --directory site
```

## Layout

- `icons/outline/*.svg`, `icons/filled/*.svg` — normalized single-path SVGs (`fill="currentColor"`), checked in.
- `icons/icons.json` — name, category, tags. `icons/codepoints.json` — stable font code points (only grows).
- `scripts/normalize.mjs` — Figma export → `icons/` (outlines strokes, fixes contour winding for nonzero/fonts).
- `scripts/build.mjs` — `icons/` → `packages/*/dist`, `packages/elm/src`, `site/data`, `site/fonts` (generated, not checked in).
- Packages are `private` and unlicensed until a license is chosen.

## Workflow

```bash
npm install
npm run export   # Figma bridge → tools/export/raw.json → icons/
npm run build    # icons/ → all packages + site data
```

## Figma source

Source for the SwoozhIcons Figma library: 24 px grid, 1.5 px centre stroke, butt caps, miter joins,
each icon a component set with `Style=Outline` and `Style=Filled`.

- `icons.py` holds every icon as a list of (kind, svg path) elements; see its docstring for kinds
  (`o`, `s`, `cut`, `k`, `d`, `f`, plus `e`/`g`/`gf` for corner badges).
- `python3 -I build.py [page-substring ...]` writes `build.js`; `python3 -I build_some.py name ...` builds named icons only.
- `python3 -I br.py build.js build_out.json --remove` runs it through the Figma MCP bridge (needs the bridge plugin open
  in SwoozhIcons and `FIGMA_BRIDGE_ENABLE_RUN_SCRIPT=1`; update `FILE_KEY` in `br.py` when the file key changes).
- `python3 -I export.py "Page title" ...` or `--sets name ...` writes preview PNGs to `previews/`.
- `tools/qa.js` checks the whole library (variants, sizes, duplicates, descriptions).
