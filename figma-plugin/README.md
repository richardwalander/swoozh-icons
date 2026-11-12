# Swoozh Icons for Figma

Search all Swoozh Icons and insert them as vectors in Figma, FigJam and Slides.

- Search by name or tag, filter by category.
- Outline, Filled, or Stroke (a live stroke you can edit, 0.75–2 px).
- Choose the size (16–48 px) and colour. Your choices are remembered.
- Click an icon to insert it. With a frame selected, the icon goes inside it. Or drag it onto the canvas.

## Build

```bash
npm run build    # writes site/data/*.js
npm run figma    # writes figma-plugin/dist/
```

## Try it in Figma

Figma desktop → Plugins → Development → Import plugin from manifest… → `figma-plugin/manifest.json`.

Before publishing to Community, Figma assigns a real plugin id; replace `"id"` in `manifest.json` with it.
