// icons/ -> packages/*/dist (core, react, vue, svelte, element, elm, font) and site/data.
import { readFileSync, writeFileSync, mkdirSync, rmSync, copyFileSync, cpSync } from 'node:fs';
import { Readable } from 'node:stream';
import { SVGIcons2SVGFontStream } from 'svgicons2svgfont';
import svg2ttf from 'svg2ttf';
import ttf2woff2 from 'ttf2woff2';

const R = new URL('..', import.meta.url).pathname;
const pkg = JSON.parse(readFileSync(R + 'package.json', 'utf8'));
const VERSION = pkg.version;
const meta = JSON.parse(readFileSync(R + 'icons/icons.json', 'utf8'));
const cps = JSON.parse(readFileSync(R + 'icons/codepoints.json', 'utf8'));
const pathOf = (v, n) => readFileSync(R + `icons/${v}/${n}.svg`, 'utf8').match(/ d="([^"]*)"/)[1];
const pascal = n => n.split('-').map(s => s[0].toUpperCase() + s.slice(1)).join('');
const camel = n => { const p = pascal(n); return p[0].toLowerCase() + p.slice(1); };
const strokeOf = n => readFileSync(R + `icons/stroke/${n}.svg`, 'utf8').replace(/^<svg[^>]*>/, '').replace(/<\/svg>$/, '');
const icons = meta.map(m => ({...m, st: strokeOf(m.name), pascal: pascal(m.name), camel: camel(m.name), o: pathOf('outline', m.name), f: pathOf('filled', m.name), cp: cps[m.name]}));
if (new Set(icons.map(i => i.pascal)).size !== icons.length) throw new Error('PascalCase name collision');
const J = JSON.stringify;
const out = (p, s) => { mkdirSync(R + p.replace(/\/[^/]*$/, ''), {recursive: true}); writeFileSync(R + p, s); };
const fresh = d => { rmSync(R + d, {recursive: true, force: true}); mkdirSync(R + d, {recursive: true}); };
const XMLNS = 'http://www.w3.org/2000/svg';
const svgDoc = d => `<svg xmlns="${XMLNS}" width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="${d}"/></svg>`;

// core: @swoozh/icons ---------------------------------------------------------------------------
fresh('packages/icons/dist');
out('packages/icons/dist/index.js', `// Swoozh Icons ${VERSION}. Each export is {name, outline, filled}: SVG path data on a 24x24 viewBox.\n` +
  icons.map(i => `export const ${i.pascal} = {name: ${J(i.name)}, outline: ${J(i.o)}, filled: ${J(i.f)}};`).join('\n') + '\n' +
  `export function toSvg(icon, {variant = 'outline', size = 24, color = 'currentColor', title} = {}) {\n` +
  `  const t = title ? '<title>' + String(title).replace(/[<&]/g, c => c === '<' ? '&lt;' : '&amp;') + '</title>' : '';\n` +
  `  return '<svg xmlns="${XMLNS}" width="' + size + '" height="' + size + '" viewBox="0 0 24 24" fill="' + color + '"' + (title ? ' role="img"' : ' aria-hidden="true"') + '>' + t + '<path d="' + icon[variant === 'filled' ? 'filled' : 'outline'] + '"/></svg>';\n}\n`);
out('packages/icons/dist/index.d.ts', `export interface SwoozhIconData { name: string; outline: string; filled: string }\n` +
  `export interface ToSvgOptions { variant?: 'outline' | 'filled'; size?: number | string; color?: string; title?: string }\n` +
  `export declare function toSvg(icon: SwoozhIconData, options?: ToSvgOptions): string;\n` +
  icons.map(i => `export declare const ${i.pascal}: SwoozhIconData;`).join('\n') + '\n');
out('packages/icons/dist/icons.json', J(icons.map(({name, category, tags}) => ({name, category, tags}))));
for (const v of ['outline', 'filled']) {
  mkdirSync(R + `packages/icons/dist/svg/${v}`, {recursive: true});
  for (const i of icons) copyFileSync(R + `icons/${v}/${i.name}.svg`, R + `packages/icons/dist/svg/${v}/${i.name}.svg`);
  out(`packages/icons/dist/sprite-${v}.svg`, `<svg xmlns="${XMLNS}" style="display:none">` +
    icons.map(i => `<symbol id="${i.name}" viewBox="0 0 24 24" fill="currentColor"><path d="${v === 'filled' ? i.f : i.o}"/></symbol>`).join('') + '</svg>\n');
}

mkdirSync(R + 'packages/icons/dist/svg/stroke', {recursive: true});
for (const i of icons) copyFileSync(R + `icons/stroke/${i.name}.svg`, R + `packages/icons/dist/svg/stroke/${i.name}.svg`);
// Stroke variant: line icons whose thickness can be set (0.75-2, default 1.5). Markup is inner SVG; element-level widths scale with it.
const STROKE_FN = `const sw = (m, w) => m.replace(/stroke-width="([\\d.]+)"/g, (_, x) => 'stroke-width="' + +(x * w / 1.5).toFixed(3) + '"');\n`;
out('packages/icons/dist/stroke.js', `// Swoozh Icons ${VERSION} (stroke). Each export is {name, stroke}: inner SVG markup on a 24x24 viewBox, drawn with strokes.\n` + STROKE_FN +
  icons.map(i => `export const ${i.pascal} = {name: ${J(i.name)}, stroke: ${J(i.st)}};`).join('\n') + '\n' +
  `export function toStrokeSvg(icon, {strokeWidth = 1.5, size = 24, color = 'currentColor', title} = {}) {\n` +
  `  const t = title ? '<title>' + String(title).replace(/[<&]/g, c => c === '<' ? '&lt;' : '&amp;') + '</title>' : '';\n` +
  `  return '<svg xmlns="${XMLNS}" width="' + size + '" height="' + size + '" viewBox="0 0 24 24" fill="none" stroke="' + color + '" stroke-width="' + strokeWidth + '" stroke-miterlimit="10"' + (title ? ' role="img"' : ' aria-hidden="true"') + '>' + t + sw(icon.stroke, strokeWidth) + '</svg>';\n}\n`);
out('packages/icons/dist/stroke.d.ts', `export interface SwoozhStrokeIconData { name: string; stroke: string }\n` +
  `export interface ToStrokeSvgOptions { strokeWidth?: number; size?: number | string; color?: string; title?: string }\n` +
  `export declare function toStrokeSvg(icon: SwoozhStrokeIconData, options?: ToStrokeSvgOptions): string;\n` +
  icons.map(i => `export declare const ${i.pascal}: SwoozhStrokeIconData;`).join('\n') + '\n');

// react ------------------------------------------------------------------------------------------
fresh('packages/react/dist');
out('packages/react/dist/index.js', `import { createElement, forwardRef } from 'react';\n` +
  `export function createIcon(displayName, outline, filled) {\n` +
  `  const Icon = forwardRef(function SwoozhIcon({variant = 'outline', size = 24, color = 'currentColor', title, children, ...rest}, ref) {\n` +
  `    return createElement('svg', {xmlns: '${XMLNS}', viewBox: '0 0 24 24', width: size, height: size, fill: color,\n` +
  `      'aria-hidden': title ? undefined : true, role: title ? 'img' : undefined, focusable: 'false', ref, ...rest},\n` +
  `      title ? createElement('title', null, title) : null, createElement('path', {d: variant === 'filled' ? filled : outline}), children);\n` +
  `  });\n  Icon.displayName = displayName;\n  return Icon;\n}\n` +
  icons.map(i => `export const ${i.pascal} = /*#__PURE__*/ createIcon(${J(i.pascal)}, ${J(i.o)}, ${J(i.f)});`).join('\n') + '\n');
out('packages/react/dist/index.d.ts', `import type { ForwardRefExoticComponent, RefAttributes, SVGProps } from 'react';\n` +
  `export interface SwoozhIconProps extends Omit<SVGProps<SVGSVGElement>, 'ref'> { variant?: 'outline' | 'filled'; size?: number | string; color?: string; title?: string }\n` +
  `export type SwoozhIcon = ForwardRefExoticComponent<SwoozhIconProps & RefAttributes<SVGSVGElement>>;\n` +
  `export declare function createIcon(displayName: string, outline: string, filled: string): SwoozhIcon;\n` +
  icons.map(i => `export declare const ${i.pascal}: SwoozhIcon;`).join('\n') + '\n');

out('packages/react/dist/stroke.js', `import { createElement, forwardRef } from 'react';\n` + STROKE_FN +
  `export function createIcon(displayName, markup) {\n` +
  `  const Icon = forwardRef(function SwoozhStrokeIcon({strokeWidth = 1.5, size = 24, color = 'currentColor', title, ...rest}, ref) {\n` +
  `    return createElement('svg', {xmlns: '${XMLNS}', viewBox: '0 0 24 24', width: size, height: size, fill: 'none', stroke: color, strokeWidth, strokeMiterlimit: 10,\n` +
  `      'aria-hidden': title ? undefined : true, role: title ? 'img' : undefined, focusable: 'false', ref, ...rest,\n` +
  `      dangerouslySetInnerHTML: {__html: (title ? '<title>' + title.replace(/[<&]/g, c => c === '<' ? '&lt;' : '&amp;') + '</title>' : '') + sw(markup, strokeWidth)}});\n` +
  `  });\n  Icon.displayName = displayName;\n  return Icon;\n}\n` +
  icons.map(i => `export const ${i.pascal} = /*#__PURE__*/ createIcon(${J(i.pascal)}, ${J(i.st)});`).join('\n') + '\n');
out('packages/react/dist/stroke.d.ts', `import type { ForwardRefExoticComponent, RefAttributes, SVGProps } from 'react';\n` +
  `export interface SwoozhStrokeIconProps extends Omit<SVGProps<SVGSVGElement>, 'ref' | 'strokeWidth'> { strokeWidth?: number; size?: number | string; color?: string; title?: string }\n` +
  `export type SwoozhStrokeIcon = ForwardRefExoticComponent<SwoozhStrokeIconProps & RefAttributes<SVGSVGElement>>;\n` +
  `export declare function createIcon(displayName: string, markup: string): SwoozhStrokeIcon;\n` +
  icons.map(i => `export declare const ${i.pascal}: SwoozhStrokeIcon;`).join('\n') + '\n');

// vue --------------------------------------------------------------------------------------------
fresh('packages/vue/dist');
out('packages/vue/dist/index.js', `import { defineComponent, h } from 'vue';\n` +
  `export function createIcon(name, outline, filled) {\n  return defineComponent({\n    name,\n` +
  `    props: {variant: {type: String, default: 'outline'}, size: {type: [Number, String], default: 24}, color: {type: String, default: 'currentColor'}, title: String},\n` +
  `    setup(p) {\n      return () => h('svg', {xmlns: '${XMLNS}', viewBox: '0 0 24 24', width: p.size, height: p.size, fill: p.color,\n` +
  `        'aria-hidden': p.title ? undefined : 'true', role: p.title ? 'img' : undefined},\n` +
  `        [p.title ? h('title', p.title) : null, h('path', {d: p.variant === 'filled' ? filled : outline})]);\n    }\n  });\n}\n` +
  icons.map(i => `export const ${i.pascal} = /*#__PURE__*/ createIcon(${J(i.pascal)}, ${J(i.o)}, ${J(i.f)});`).join('\n') + '\n');
out('packages/vue/dist/index.d.ts', `import type { DefineComponent } from 'vue';\n` +
  `export interface SwoozhIconProps { variant?: 'outline' | 'filled'; size?: number | string; color?: string; title?: string }\n` +
  `export type SwoozhIcon = DefineComponent<SwoozhIconProps>;\n` +
  `export declare function createIcon(name: string, outline: string, filled: string): SwoozhIcon;\n` +
  icons.map(i => `export declare const ${i.pascal}: SwoozhIcon;`).join('\n') + '\n');

out('packages/vue/dist/stroke.js', `import { defineComponent, h } from 'vue';\n` + STROKE_FN +
  `export function createIcon(name, markup) {\n  return defineComponent({\n    name,\n` +
  `    props: {strokeWidth: {type: Number, default: 1.5}, size: {type: [Number, String], default: 24}, color: {type: String, default: 'currentColor'}, title: String},\n` +
  `    setup(p) {\n      return () => h('svg', {xmlns: '${XMLNS}', viewBox: '0 0 24 24', width: p.size, height: p.size, fill: 'none', stroke: p.color, 'stroke-width': p.strokeWidth, 'stroke-miterlimit': 10,\n` +
  `        'aria-hidden': p.title ? undefined : 'true', role: p.title ? 'img' : undefined,\n` +
  `        innerHTML: (p.title ? '<title>' + p.title.replace(/[<&]/g, c => c === '<' ? '&lt;' : '&amp;') + '</title>' : '') + sw(markup, p.strokeWidth)});\n    }\n  });\n}\n` +
  icons.map(i => `export const ${i.pascal} = /*#__PURE__*/ createIcon(${J(i.pascal)}, ${J(i.st)});`).join('\n') + '\n');
out('packages/vue/dist/stroke.d.ts', `import type { DefineComponent } from 'vue';\n` +
  `export interface SwoozhStrokeIconProps { strokeWidth?: number; size?: number | string; color?: string; title?: string }\n` +
  `export type SwoozhStrokeIcon = DefineComponent<SwoozhStrokeIconProps>;\n` +
  `export declare function createIcon(name: string, markup: string): SwoozhStrokeIcon;\n` +
  icons.map(i => `export declare const ${i.pascal}: SwoozhStrokeIcon;`).join('\n') + '\n');

// svelte -----------------------------------------------------------------------------------------
fresh('packages/svelte/dist');
out('packages/svelte/dist/Icon.svelte', `<script>\n  /** @type {{outline: string, filled: string}} */\n  export let icon;\n` +
  `  /** @type {'outline' | 'filled'} */\n  export let variant = 'outline';\n  export let size = 24;\n  export let color = 'currentColor';\n  export let title = undefined;\n</script>\n\n` +
  `<svg xmlns="${XMLNS}" viewBox="0 0 24 24" width={size} height={size} fill={color} aria-hidden={title ? undefined : 'true'} role={title ? 'img' : undefined} {...$$restProps}>{#if title}<title>{title}</title>{/if}<path d={variant === 'filled' ? icon.filled : icon.outline} /></svg>\n`);
cpSync(R + 'packages/icons/dist/index.js', R + 'packages/svelte/dist/icons.js');
cpSync(R + 'packages/icons/dist/index.d.ts', R + 'packages/svelte/dist/icons.d.ts');
out('packages/svelte/dist/index.js', `export { default as Icon } from './Icon.svelte';\nexport * from './icons.js';\n`);
out('packages/svelte/dist/index.d.ts', `import type { SvelteComponent } from 'svelte';\nimport type { SwoozhIconData } from './icons.js';\n` +
  `export * from './icons.js';\nexport declare class Icon extends SvelteComponent<{icon: SwoozhIconData; variant?: 'outline' | 'filled'; size?: number | string; color?: string; title?: string; [attr: string]: unknown}> {}\n`);

out('packages/svelte/dist/StrokeIcon.svelte', `<script>\n  /** @type {{stroke: string}} */\n  export let icon;\n  export let strokeWidth = 1.5;\n  export let size = 24;\n  export let color = 'currentColor';\n  export let title = undefined;\n` +
  `  $: markup = (title ? '<title>' + title.replace(/[<&]/g, c => c === '<' ? '&lt;' : '&amp;') + '</title>' : '') + icon.stroke.replace(/stroke-width="([\\d.]+)"/g, (_, x) => 'stroke-width="' + +(x * strokeWidth / 1.5).toFixed(3) + '"');\n</script>\n\n` +
  `<svg xmlns="${XMLNS}" viewBox="0 0 24 24" width={size} height={size} fill="none" stroke={color} stroke-width={strokeWidth} stroke-miterlimit="10" aria-hidden={title ? undefined : 'true'} role={title ? 'img' : undefined} {...$$restProps}>{@html markup}</svg>\n`);
cpSync(R + 'packages/icons/dist/stroke.js', R + 'packages/svelte/dist/stroke-icons.js');
cpSync(R + 'packages/icons/dist/stroke.d.ts', R + 'packages/svelte/dist/stroke-icons.d.ts');
out('packages/svelte/dist/stroke.js', `export { default as StrokeIcon } from './StrokeIcon.svelte';\nexport * from './stroke-icons.js';\n`);
out('packages/svelte/dist/stroke.d.ts', `import type { SvelteComponent } from 'svelte';\nimport type { SwoozhStrokeIconData } from './stroke-icons.js';\n` +
  `export * from './stroke-icons.js';\nexport declare class StrokeIcon extends SvelteComponent<{icon: SwoozhStrokeIconData; strokeWidth?: number; size?: number | string; color?: string; title?: string; [attr: string]: unknown}> {}\n`);

// web component ----------------------------------------------------------------------------------
fresh('packages/element/dist');
const wc = `(() => {\n  const I = {\n` + icons.map(i => `    ${J(i.name)}: [${J(i.o)}, ${J(i.f)}]`).join(',\n') + `\n  };\n` +
  `  const esc = s => String(s).replace(/[<&"]/g, c => ({'<': '&lt;', '&': '&amp;', '"': '&quot;'}[c]));\n` +
  `  class SwoozhIcon extends HTMLElement {\n    static observedAttributes = ['name', 'variant', 'size', 'label'];\n` +
  `    static icons = I;\n    connectedCallback() { this.render(); }\n    attributeChangedCallback() { if (this.isConnected) this.render(); }\n` +
  `    render() {\n      const i = I[this.getAttribute('name')];\n      if (!i) { this.innerHTML = ''; return; }\n` +
  `      const s = esc(this.getAttribute('size') || '24'), l = this.getAttribute('label');\n` +
  `      this.style.display = this.style.display || 'inline-flex';\n` +
  `      this.innerHTML = '<svg xmlns="${XMLNS}" viewBox="0 0 24 24" width="' + s + '" height="' + s + '" fill="currentColor"' + (l ? ' role="img" aria-label="' + esc(l) + '"' : ' aria-hidden="true"') + '><path d="' + i[this.getAttribute('variant') === 'filled' ? 1 : 0] + '"/></svg>';\n    }\n  }\n` +
  `  if (!customElements.get('swoozh-icon')) customElements.define('swoozh-icon', SwoozhIcon);\n})();\n`;
out('packages/element/dist/swoozh-icon.js', wc);
const wcs = `(() => {\n  const I = {\n` + icons.map(i => `    ${J(i.name)}: ${J(i.st)}`).join(',\n') + `\n  };\n` + STROKE_FN +
  `  const esc = s => String(s).replace(/[<&"]/g, c => ({'<': '&lt;', '&': '&amp;', '"': '&quot;'}[c]));\n` +
  `  class SwoozhStrokeIcon extends HTMLElement {\n    static observedAttributes = ['name', 'size', 'stroke-width', 'label'];\n` +
  `    static icons = I;\n    connectedCallback() { this.render(); }\n    attributeChangedCallback() { if (this.isConnected) this.render(); }\n` +
  `    render() {\n      const m = I[this.getAttribute('name')];\n      if (!m) { this.innerHTML = ''; return; }\n` +
  `      const s = esc(this.getAttribute('size') || '24'), l = this.getAttribute('label'), w = Math.min(4, Math.max(0.25, parseFloat(this.getAttribute('stroke-width')) || 1.5));\n` +
  `      this.style.display = this.style.display || 'inline-flex';\n` +
  `      this.innerHTML = '<svg xmlns="${XMLNS}" viewBox="0 0 24 24" width="' + s + '" height="' + s + '" fill="none" stroke="currentColor" stroke-width="' + w + '" stroke-miterlimit="10"' + (l ? ' role="img" aria-label="' + esc(l) + '"' : ' aria-hidden="true"') + '>' + sw(m, w) + '</svg>';\n    }\n  }\n` +
  `  if (!customElements.get('swoozh-stroke-icon')) customElements.define('swoozh-stroke-icon', SwoozhStrokeIcon);\n})();\n`;
out('packages/element/dist/swoozh-stroke-icon.js', wcs);
out('packages/element/dist/swoozh-icon.d.ts', `export {};\ndeclare global { interface HTMLElementTagNameMap { 'swoozh-icon': HTMLElement } }\n`);

// elm --------------------------------------------------------------------------------------------
fresh('packages/elm/src');
const ELM_RESERVED = new Set(['if', 'then', 'else', 'case', 'of', 'let', 'in', 'type', 'module', 'where', 'import', 'exposing', 'as', 'port', 'alias', 'infix', 'effect', 'command', 'subscription']);
const elmName = i => ELM_RESERVED.has(i.camel) ? i.camel + 'Icon' : i.camel;
out('packages/elm/src/SwoozhIcons.elm', `module SwoozhIcons exposing\n    ( Variant(..), icon\n    , ` + icons.map(elmName).join('\n    , ') + `\n    )\n\n` +
  `{-| Swoozh Icons ${VERSION}: ${icons.length} icons in two variants on a 24x24 grid.\n\n    SwoozhIcons.shoppingBag SwoozhIcons.Outline [ Svg.Attributes.width "32", Svg.Attributes.height "32" ]\n\n` +
  `@docs Variant, icon\n\n@docs ` + icons.map(elmName).join(', ') + `\n\n-}\n\nimport Svg exposing (Svg)\nimport Svg.Attributes as A\n\n\n` +
  `{-| Outline (line) or Filled (solid). -}\ntype Variant\n    = Outline\n    | Filled\n\n\n` +
  `{-| Build an icon from outline and filled path data. Attributes come last so they override width, height and fill. -}\n` +
  `icon : String -> String -> Variant -> List (Svg.Attribute msg) -> Svg msg\nicon outline filled variant attrs =\n` +
  `    Svg.svg\n        ([ A.viewBox "0 0 24 24", A.width "24", A.height "24", A.fill "currentColor" ] ++ attrs)\n` +
  `        [ Svg.path\n            [ A.d\n                (case variant of\n                    Outline ->\n                        outline\n\n                    Filled ->\n                        filled\n                )\n            ]\n            []\n        ]\n` +
  icons.map(i => `\n\n{-| ${i.name}${i.tags.length ? ': ' + i.tags.join(', ') : ''} -}\n${elmName(i)} : Variant -> List (Svg.Attribute msg) -> Svg msg\n${elmName(i)} =\n    icon ${J(i.o)} ${J(i.f)}\n`).join(''));

// font -------------------------------------------------------------------------------------------
fresh('packages/font/dist');
async function font(variant, family, file) {
  const stream = new SVGIcons2SVGFontStream({fontName: family, fontHeight: 1200, descent: 150, normalize: false, fixedWidth: true, log: () => {}});
  const chunks = [];
  const done = new Promise((ok, ko) => { stream.on('data', c => chunks.push(c)); stream.on('end', ok); stream.on('error', ko); });
  for (const i of icons) {
    const g = Readable.from([svgDoc(variant === 'filled' ? i.f : i.o)]);
    g.metadata = {name: i.name, unicode: [String.fromCodePoint(i.cp)]};
    stream.write(g);
  }
  stream.end(); await done;
  const svgFont = chunks.map(String).join('');
  const ttf = Buffer.from(svg2ttf(svgFont, {version: 'Version ' + VERSION.replace(/^(\d+\.\d+).*/, '$1'), description: 'Swoozh Icons', url: ''}).buffer);
  writeFileSync(R + `packages/font/dist/${file}.ttf`, ttf);
  writeFileSync(R + `packages/font/dist/${file}.woff2`, ttf2woff2(ttf));
}
await font('outline', 'Swoozh Icons', 'swoozh-icons-outline');
await font('filled', 'Swoozh Icons Filled', 'swoozh-icons-filled');
const hex = cp => cp.toString(16);
out('packages/font/dist/swoozh-icons.css', `/* Swoozh Icons ${VERSION} */\n` +
  `@font-face{font-family:"Swoozh Icons";src:url("swoozh-icons-outline.woff2") format("woff2"),url("swoozh-icons-outline.ttf") format("truetype");font-weight:normal;font-style:normal;font-display:block}\n` +
  `@font-face{font-family:"Swoozh Icons Filled";src:url("swoozh-icons-filled.woff2") format("woff2"),url("swoozh-icons-filled.ttf") format("truetype");font-weight:normal;font-style:normal;font-display:block}\n` +
  `.swz{font-family:"Swoozh Icons"!important;font-style:normal;font-weight:normal;font-variant:normal;text-transform:none;line-height:1;display:inline-block;speak:never;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale}\n` +
  `.swz.swz-filled{font-family:"Swoozh Icons Filled"!important}\n` +
  icons.map(i => `.swz-${i.name}::before{content:"\\${hex(i.cp)}"}`).join('\n') + '\n');
out('packages/font/dist/codepoints.json', J(Object.fromEntries(icons.map(i => [i.name, i.cp])), null, 1));

// site data --------------------------------------------------------------------------------------
fresh('site/data'); fresh('site/fonts');
out('site/data/icons.js', `window.SWOOZH = ${J({version: VERSION, categories: [...new Set(icons.map(i => i.category))],
  icons: icons.map(i => [i.name, i.category, i.tags.join(','), i.o, i.f, i.cp])})};\n`);
out('site/data/stroke.js', `window.SWOOZH_STROKE = ${J(Object.fromEntries(icons.map(i => [i.name, i.st])))};\n`);
cpSync(R + 'packages/element/dist/swoozh-icon.js', R + 'site/data/swoozh-icon.js');
for (const f of ['swoozh-icons-outline.woff2', 'swoozh-icons-filled.woff2', 'swoozh-icons.css']) copyFileSync(R + 'packages/font/dist/' + f, R + 'site/fonts/' + f);
console.log(`built ${icons.length} icons, version ${VERSION}`);
