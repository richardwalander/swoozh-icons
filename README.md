# Swoozh Icons

Source for the SwoozhIcons Figma library: 24 px grid, 1.5 px centre stroke, butt caps, miter joins,
each icon a component set with `Style=Outline` and `Style=Filled`.

- `icons.py` holds every icon as a list of (kind, svg path) elements; see its docstring for kinds
  (`o`, `s`, `cut`, `k`, `d`, `f`, plus `e`/`g`/`gf` for corner badges).
- `python3 -I build.py [page-substring ...]` writes `build.js`; `python3 -I build_some.py name ...` builds named icons only.
- `python3 -I br.py build.js build_out.json --remove` runs it through the Figma MCP bridge (needs the bridge plugin open
  in SwoozhIcons and `FIGMA_BRIDGE_ENABLE_RUN_SCRIPT=1`; update `FILE_KEY` in `br.py` when the file key changes).
- `python3 -I export.py "Page title" ...` or `--sets name ...` writes preview PNGs to `previews/`.
- `tools/qa.js` checks the whole library (variants, sizes, duplicates, descriptions).
