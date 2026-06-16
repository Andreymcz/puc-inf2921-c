# Research 000059 | project | 2026-06-16 14:04 UTC | best frontend for fala-gavea-seguranca
tags: frontend, architecture, alpine-js, leaflet, fala-gavea-seguranca

## User Brief

> best front end tool for this project. Atualmente estamos servindo paginas estáticas. porem com as mudanças previstas no roadmap 56 podemos precisar de uma UI mais dinamica.

## Agent Interpretation

The team is building `fala-gavea-seguranca`: a Leaflet.js-based civic security map served as static HTML/CSS/JS from a FastAPI backend. Roadmap 56 Wave 2 adds a significantly more complex UI (temporal filter, bbox filter, tag chips in popups, semantic search layer, and an AI category curation panel with multi-state popup interactions). The question is whether to stay with vanilla JS or adopt a lightweight UI framework — and if so, which one — subject to the no-bundler / no-npm-build constraint.

## Files Consulted

- `fala-gavea-seguranca/static/index.html` — current static page structure
- `fala-gavea-seguranca/static/app.js` — vanilla JS, 199 lines, mixes map control + DOM + API calls
- `_output/roadmaps/roadmap-000056-filtros-mapa-tags-ai-category.md` — Wave 2 feature spec
- `product-design/project/product-design-as-coded.md` — as-coded implementation state

---

## Q&A Log

### Q1: What is the best frontend approach for `fala-gavea-seguranca` as Wave 2 complexity arrives?

**Background (current state):**
- Static pages: `index.html`, `app.js`, `style.css` served by FastAPI
- Zero build tooling; Leaflet loaded from CDN
- `app.js` is 199 lines mixing map init, DOM manipulation, and API calls

**Wave 2 feature set (roadmap-000056 item 5):**
1. Temporal filter (two date inputs → `since`/`until` params)
2. Spatial bbox filter (checkbox → reads `map.getBounds()` on `moveend`)
3. Tag chips in every popup
4. Semantic search layer (separate Leaflet layer of purple pins)
5. AI category curation panel inside popups: three states — no suggestion / suggestion pending / delegado correcting; calls `POST /{id}/auto_categorize` and `PATCH /{id}/category`

**Options evaluated:**

| Option | Bundle step | Learning curve | Complexity ceiling | Leaflet popup support |
|--------|------------|---------------|-------------------|-----------------------|
| Vanilla JS (stay) | None | None | Low — popup string templates break on multi-state panels | `getPopup().setContent()` — works but fragile |
| **Alpine.js CDN** | None | Low (declarative HTML) | Medium — handles reactive state declaratively | `Alpine.initTree(el)` after `popupopen` |
| Vue 3 CDN | None | Medium (component model) | High | `createApp().mount()` inside popup — heavier, fragile |
| petite-vue CDN | None | Low-Medium | Medium | Limited docs for this case |
| HTMX | None | Medium | Medium | Requires backend HTML fragments — breaks JSON API |
| React/Svelte | Required | High | High | Overkill |

**Critical finding — the AI curation popup is the blocking constraint:**

The AI curation panel has three interactive states inside a Leaflet popup. The current pattern of building popup HTML as a template literal with `onclick` attribute handlers cannot represent state transitions without rebuilding the entire popup string on every action. The three states are:

1. No AI suggestion yet → show "🤖 Categorizar" button
2. Suggestion present, unconfirmed → badge + "✅ Confirmar" + "✏️ Corrigir" dropdown
3. PATCH in flight → loading indicator; on failure, error badge stays open

With vanilla JS, each state change requires `layer.getPopup().setContent(newHtml)` + re-binding all `onclick` handlers to global functions. This works but is fragile: name collisions, no encapsulation, silent failure if the PATCH errors after the popup closes.

With Alpine.js, the popup HTML declares `x-data="{ state: 'idle', error: null }"` and uses `x-show`/`x-on` for each state. After Leaflet renders the popup, one call to `Alpine.initTree(e.popup.getElement())` activates Alpine's reactivity inside it. This is documented Alpine behavior for dynamically injected content.

**Architecture finding — `app.js` is near its complexity ceiling:**

199 lines mixing three concerns. Wave 2 adds ~150 more lines (five new subsystems). Without module boundaries, the file becomes unmaintainable. ES module syntax (`<script type="module">`) works in modern browsers without a bundler and allows splitting into `map-init.js`, `filters.js`, `popup.js`. Leaflet stays as a global; only team-authored code uses `import/export`.

**Recommendation:** Adopt Alpine.js via CDN + ES module split. See recommendations below.

---

## Recommendations Summary

### [HIGH] 1. Adopt Alpine.js via CDN in `index.html`

Add to `index.html`:
```html
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
```

Use Alpine `x-data` for the filter panel state (show/hide form, loading flag, error display). Keep `app.js` for Leaflet initialization and API fetch logic. Alpine manages reactive UI state; vanilla JS manages the map object. Scope to `index.html` only — `chat.html` and `insights.html` don't need reactivity.

**Why Alpine over Vue 3 CDN:** Vue requires understanding a component model that the Python-primary team doesn't use today. Alpine's HTML-attribute approach (`x-show`, `x-on`, `x-bind`) is readable without JS framework knowledge. **Why not HTMX:** requires the FastAPI backend to return HTML fragments — a 5-day refactor that contradicts the existing JSON API pattern. **Why not Vue/React/Svelte:** build pipeline required.

### [HIGH] 2. Use `Alpine.initTree()` for AI curation popup

Replace the `bindPopup(\`template literal\`)` pattern for the AI curation popup with a `buildCurationPopup(p)` function that returns structured HTML with `x-data`, `x-show`, and `x-on` attributes. After `popupopen`, call:

```js
map.on('popupopen', (e) => {
  Alpine.initTree(e.popup.getElement());
});
```

This is the only clean way to support the three-state delegado flow (idle / suggestion / correction) without rebuilding popup content on every button click.

### [HIGH] 3. Split `app.js` into ES modules before implementing Wave 2

Refactor into at least three modules using `<script type="module">`:
- `map-init.js` — Leaflet setup, tile layer, layer group declarations
- `filters.js` — `buildQueryString()`, `loadReports()`, bbox/moveend logic
- `popup.js` — `buildPopupContent(p)`, PATCH handlers, Alpine popup builders

No bundler required; modern browsers support ES module imports natively. Leaflet stays as a global (`window.L`).

### [MEDIUM] 4. Debounce `moveend` and show a loading indicator for bbox filter

The bbox auto-update triggers `moveend` on every animation frame during pan. Without debounce, pins flicker continuously. Add 300-500ms debounce and a small `x-show="loading"` badge ("Atualizando...") that appears while the fetch is in flight. Without this, users lose confidence in map state.

### [MEDIUM] 5. Do not adopt Vue 3 CDN, petite-vue, HTMX, React, or Svelte

- **Vue 3 CDN:** component model overhead not justified for 2-3 week window
- **petite-vue:** sparse documentation for the Leaflet popup edge case; higher debugging risk
- **HTMX:** requires backend refactor to return HTML fragments; contradicts current JSON API
- **React/Svelte:** require build pipeline — ruled out by constraint

### [LOW] 6. Document the Alpine.js + Leaflet integration pattern

Add a comment block at the top of `popup.js` explaining the `Alpine.initTree(e.popup.getElement())` call convention, so team members adding Alpine directives to popup content don't hit a silent failure (directives declared but never initialized by Alpine because the popup HTML was injected after page load).

---

## Perspective Summary

| Perspective | Finding | Status |
|-------------|---------|--------|
| Architecture | `app.js` is at complexity ceiling; Wave 2 requires module split | Deferred → resolved by Rec 3 |
| DX | Alpine.js is the ergonomic fit for Python-primary team; zero new toolchain | Adopted |
| UX | AI curation panel's three states require reactive model in popup | Resolved by Rec 2 |
| Compatibility | All CDN options target modern browsers; Leaflet already sets the floor | Adopted |
| Performance | Alpine.js (~15KB) adds negligible weight vs. existing Leaflet CDN payload | Adopted |
| Micro-interaction | Leaflet popup requires `Alpine.initTree()` — non-obvious but documented | Resolved by Recs 2 + 6 |
