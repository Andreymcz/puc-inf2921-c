# Plan 000063 | FEATURE-F | 2026-06-16 14:03 UTC | Frontend: painel de filtros completo | Review: light
plan_format_version: 1

## Brief

> roadmap-000056 Wave 2 Item 5 — Expor no frontend: filtro temporal (date_from/date_to), filtro espacial (bbox da área visível), tags chips + filtro por tag, busca semântica, painel de curadoria de categoria (ai_suggested_category). Depende de Wave 1 completa (plans 000060, 000061, 000062).

## Agent Interpretation

O frontend atual (`static/index.html` + `static/app.js`) expõe apenas `?category` e `?status`. Este plano completa o painel de filtros e expõe as capacidades do backend Wave 1.

**Stack decision (research-000059, 2026-06-16):** Steps 1-5 são vanilla JS puro. Step 6 (popup de curadoria) adopta **Alpine.js via CDN** para gerenciar os 3 estados do popup (sem sugestão / sugestão pendente / loading+erro) sem reescrever innerHTML a cada transição. Sem bundler, sem npm build. Leaflet continua como global (`window.L`); Alpine é ativado nos popups via `Alpine.initTree(e.popup.getElement())` no evento `popupopen`.

**Dependências**:
- plan-000057: enum com 9 categorias (CATEGORY_COLORS e CATEGORY_LABELS precisam das 9 entradas)
- plan-000060: `tags` nas properties do GeoJSON + `PATCH /{id}/tags` + `?tag=` filter
- plan-000061: `ai_suggested_category` nas properties + endpoints de auto-categorização e curadoria
- plan-000062: `?until=` no backend

---

## Scope

- **In scope**: `index.html` (campos de filtro + form); `app.js` (lógica de filtros, busca semântica, tags, curadoria); `style.css` (chips de tags, badge de IA, busca semântica).
- **Out of scope**: Autenticação de delegado (não há auth no sistema); paginação da lista de relatos; exportação CSV.

---

## Files

- `fala-gavea-seguranca/static/index.html` — novos controles de filtro + tag input + busca semântica + tag field no formulário
- `fala-gavea-seguranca/static/app.js` — lógica de todos os novos filtros + popup de curadoria + busca semântica
- `fala-gavea-seguranca/static/style.css` — estilos: chips de tag, badge de IA, busca semântica, data inputs

---

## Steps

### Step 1: Atualizar `CATEGORY_COLORS`, `CATEGORY_LABELS` e selects de categoria para 9 valores

Em `app.js`, substituir as constantes:
```js
const CATEGORY_COLORS = {
  furto_roubo:             '#e94560',
  iluminacao:              '#f0c040',
  transito:                '#4090f0',
  espaco_publico_inseguro: '#e07020',
  vandalismo:              '#f04040',
  moradores_situacao_rua:  '#a060d0',
  conflito_social:         '#d04040',
  barulho_perturbacao:     '#60a080',
  outro:                   '#90c090',
};

const CATEGORY_LABELS = {
  furto_roubo:             'Furto / Roubo',
  iluminacao:              'Iluminação',
  transito:                'Trânsito',
  espaco_publico_inseguro: 'Espaço público inseguro',
  vandalismo:              'Vandalismo',
  moradores_situacao_rua:  'Moradores em situação de rua',
  conflito_social:         'Conflito / Tensão comunitária',
  barulho_perturbacao:     'Barulho / Perturbação',
  outro:                   'Outro',
};
```

Em `index.html`, atualizar `<select id="filter-category">` e `<select id="f-category">` com as 9 opções correspondentes.

- **Files**: `static/app.js`, `static/index.html`
- **Verify**: visualmente no browser — marcadores existentes exibem cor correta; dropdown mostra 9 categorias
- [ ] Done

### Step 2: Adicionar filtros de data (date_from / date_to)

Em `index.html`, dentro de `<div id="filters">`, após o select de status, adicionar:
```html
<label>De
  <input type="date" id="filter-date-from" />
</label>
<label>Até
  <input type="date" id="filter-date-to" />
</label>
```

Em `app.js`, em `buildQueryString()`, adicionar:
```js
const dateFrom = document.getElementById('filter-date-from').value;
const dateTo   = document.getElementById('filter-date-to').value;
if (dateFrom) params.set('since', new Date(dateFrom).toISOString());
if (dateTo)   params.set('until', new Date(dateTo + 'T23:59:59').toISOString());
```

- **Files**: `static/index.html`, `static/app.js`
- **Verify**: selecionar período no filtro → apenas relatos dentro do intervalo aparecem no mapa
- [ ] Done

### Step 3: Adicionar filtro espacial por bbox (área visível do mapa)

Em `index.html`, após os filtros de data:
```html
<label class="checkbox-label">
  <input type="checkbox" id="filter-bbox" />
  Somente área visível
</label>
```

Em `app.js`, em `buildQueryString()`:
```js
if (document.getElementById('filter-bbox').checked) {
  const b = map.getBounds();
  params.set('lat_min', b.getSouth().toFixed(6));
  params.set('lat_max', b.getNorth().toFixed(6));
  params.set('lon_min', b.getWest().toFixed(6));
  params.set('lon_max', b.getEast().toFixed(6));
}
```

Em `app.js`, após inicialização do mapa, registrar listener com debounce:
```js
let bboxDebounce = null;
map.on('moveend', () => {
  if (!document.getElementById('filter-bbox').checked) return;
  clearTimeout(bboxDebounce);
  bboxDebounce = setTimeout(loadReports, 300);
});
```

- **Files**: `static/index.html`, `static/app.js`
- **Verify**: marcar checkbox + mover mapa → lista atualiza automaticamente com relatos visíveis (sem flickering)
- [ ] Done

### Step 4: Filtro por tag + campo de tag no formulário de novo relato

**Filtro de tag (sidebar)**

Em `index.html`, dentro de `<div id="filters">`:
```html
<label>Tag
  <input type="text" id="filter-tag" placeholder="ex: perigoso" />
</label>
```

Em `app.js`, em `buildQueryString()`:
```js
const tag = document.getElementById('filter-tag').value.trim();
if (tag) params.set('tag', tag);
```

**Tags no popup de marcador** (dentro de `geojson.features.forEach`):

Após a linha de status no popup, adicionar chips de tags:
```js
const tagsHtml = (p.tags || []).length > 0
  ? '<br>' + p.tags.map(t => `<span class="tag-chip">${t}</span>`).join(' ')
  : '';
```

Incluir `tagsHtml` no template de popup.

**Campo de tags no formulário de novo relato**

Em `index.html`, no `<form id="report-form">`, após o campo território:
```html
<label>Tags (separe por vírgulas)
  <input id="f-tags" type="text" placeholder="ex: perigoso, noite, esquina" />
</label>
```

Em `app.js`, no `onsubmit` do formulário, ler e transformar:
```js
const tagsRaw = document.getElementById('f-tags').value;
body.tags = tagsRaw ? tagsRaw.split(',').map(t => t.trim()).filter(Boolean) : [];
```

Em `style.css`, adicionar estilos para chips:
```css
.tag-chip {
  display: inline-block;
  background: #e0e7ff;
  color: #3730a3;
  border-radius: 4px;
  padding: 1px 6px;
  font-size: 0.75rem;
  margin: 1px 2px;
}
```

- **Files**: `static/index.html`, `static/app.js`, `static/style.css`
- **Verify**: criar relato com tags "perigoso,noite"; ver chips no popup; filtrar por "perigoso" → relato aparece; filtrar por "manhã" → não aparece
- [ ] Done

### Step 5: Busca semântica (campo + layer de pins roxos)

Em `index.html`, após `<div id="filters">`, adicionar painel de busca separado:
```html
<div id="search-panel">
  <h2>Busca Semântica</h2>
  <div class="search-row">
    <input type="text" id="search-q" placeholder="Descreva o que procura..." />
    <button id="btn-search">🔍</button>
  </div>
  <button id="btn-clear-search" class="secondary hidden">✕ Limpar busca</button>
</div>
```

Em `app.js`:
```js
const searchLayerGroup = L.layerGroup().addTo(map);

document.getElementById('btn-search').onclick = async () => {
  const q = document.getElementById('search-q').value.trim();
  if (!q) return;
  searchLayerGroup.clearLayers();

  const res = await fetch(`${API}/search?q=${encodeURIComponent(q)}&n=20`);
  const results = await res.json();

  results.forEach(r => {
    if (r.lat != null && r.lon != null) {
      L.circleMarker([r.lat, r.lon], {
        radius: 10,
        color: '#7c3aed',
        fillColor: '#7c3aed',
        fillOpacity: 0.7,
        weight: 2,
      })
        .addTo(searchLayerGroup)
        .bindPopup(`
          <strong>🔍 ${CATEGORY_LABELS[r.category] || r.category}</strong><br>
          ${r.text}<br>
          <small>Distância: ${r.distance.toFixed(3)}</small>
        `);
    }
  });

  document.getElementById('btn-clear-search').classList.remove('hidden');
};

document.getElementById('btn-clear-search').onclick = () => {
  searchLayerGroup.clearLayers();
  document.getElementById('search-q').value = '';
  document.getElementById('btn-clear-search').classList.add('hidden');
};
```

Em `style.css`:
```css
#search-panel { margin-top: 12px; }
.search-row { display: flex; gap: 4px; }
.search-row input { flex: 1; }
button.secondary { background: #6b7280; }
button.secondary:hover { background: #4b5563; }
```

- **Files**: `static/index.html`, `static/app.js`, `static/style.css`
- **Verify**: digitar "assalto perto do parque" → pins roxos aparecem nos relatos semanticamente relacionados; "Limpar busca" remove os pins
- [ ] Done

### Step 6: Painel de curadoria de categoria no popup com Alpine.js

> **Abordagem:** Alpine.js via CDN para gerenciar os 3 estados do popup sem reescrever innerHTML a cada clique. Ativado com `Alpine.initTree()` no evento `popupopen` do Leaflet.

**6a — Adicionar Alpine.js ao `index.html`:**
```html
<!-- no <head>, após os outros scripts -->
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
```

**6b — Registrar `Alpine.initTree` no `popupopen` do Leaflet (em `app.js`, após `map` ser criado):**
```js
map.on('popupopen', (e) => {
  if (window.Alpine) Alpine.initTree(e.popup.getElement());
});
```

**6c — `buildCurationPanel(p)` em `app.js` — retorna HTML com `x-data`:**
```js
function buildCurationPanel(p) {
  const catOptions = Object.entries(CATEGORY_LABELS)
    .map(([v, l]) => `<option value="${v}">${l}</option>`).join('');

  return `
    <div x-data="{
      state: '${p.ai_suggested_category && p.ai_suggested_category !== p.category ? 'pending' : 'idle'}',
      correcting: false,
      loading: false,
      error: null,
      suggested: '${p.ai_suggested_category || ''}',
      async confirm(id, cat) {
        this.loading = true; this.error = null;
        const r = await fetch(\`${API}/\${id}/category\`, {method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({category:cat})});
        this.loading = false;
        if (r.ok) { map.closePopup(); loadReports(); }
        else { this.error = 'Erro ao confirmar'; }
      },
      async autocat(id) {
        this.loading = true; this.error = null;
        const r = await fetch(\`${API}/\${id}/auto_categorize\`, {method:'POST'});
        this.loading = false;
        if (r.ok) { const d = await r.json(); this.suggested = d.category; this.state = 'pending'; }
        else { this.error = 'Ollama indisponível'; }
      }
    }">
      <!-- Estado: sem sugestão -->
      <div x-show="state === 'idle'">
        <button @click="autocat('${p.id}')">🤖 Categorizar por IA</button>
      </div>
      <!-- Estado: sugestão pendente -->
      <div x-show="state === 'pending'" class="ai-badge">
        🤖 Sugestão: <strong x-text="suggested"></strong>
        <div class="curation-actions" x-show="!correcting">
          <button @click="confirm('${p.id}', suggested)">✅ Confirmar</button>
          <button @click="correcting = true">✏️ Corrigir</button>
        </div>
        <div class="curation-actions" x-show="correcting">
          <select id="cat-fix-${p.id}">${catOptions}</select>
          <button @click="confirm('${p.id}', document.getElementById('cat-fix-${p.id}').value)">Salvar</button>
          <button @click="correcting = false">Cancelar</button>
        </div>
      </div>
      <!-- Loading / Erro -->
      <div x-show="loading" class="hint">⏳ Aguardando IA...</div>
      <div x-show="error" class="hint error" x-text="error"></div>
    </div>
  `;
}
```

Chamar `buildCurationPanel(p)` dentro do template de popup de cada marcador e concatenar no final do popup HTML.

**6d — Estilos em `style.css`:**
```css
.ai-badge {
  background: #fef3c7;
  border: 1px solid #f59e0b;
  border-radius: 4px;
  padding: 4px 8px;
  margin: 4px 0;
  font-size: 0.85rem;
}
.curation-actions {
  display: flex;
  gap: 4px;
  align-items: center;
  flex-wrap: wrap;
  margin-top: 4px;
}
.hint.error { color: #dc2626; font-size: 0.8rem; }
```

- **Files**: `static/index.html` (Alpine CDN), `static/app.js` (initTree + buildCurationPanel), `static/style.css`
- **Verify**:
  - Relato sem sugestão → botão "🤖 Categorizar por IA" aparece; ao clicar, spinner aparece e após resposta o badge de sugestão emerge
  - Relato com `ai_suggested_category` → badge amarelo + "✅ Confirmar" + "✏️ Corrigir"
  - "✅ Confirmar" → popup fecha, relato recarregado com nova categoria
  - "✏️ Corrigir" → dropdown aparece; "Salvar" → confirma com valor selecionado
  - Ollama offline → mensagem de erro aparece no popup sem fechar
- [ ] Done

---

## Review

### Perspectives evaluated

| Tag | Perspective | Status | Notes |
|-----|-------------|--------|-------|
| ARCH | Architecture | Adopted | Vanilla JS + fetch — sem build pipeline novo; conteúdo estático servido pelo FastAPI |
| UX | User Experience | Adopted | Filtros são opcionais e independentes — usuário básico não precisa usá-los |
| SEC | Security | Adopted | Inputs de filtro passados como query params via `URLSearchParams` (sem interpolação de HTML não-sanitizada fora do `bindPopup` que já usa template literal); `p.text` exibido diretamente no popup — considerar escaping se dados externos (aceitável para MVP local) |
| DEP | Dependencies | Adopted | Zero novas dependências de runtime; Leaflet já presente |

**Nota de segurança**: `p.text` e outros dados do servidor são inseridos diretamente via template literal no popup do Leaflet. Para MVP local com dados controlados, é aceitável. Para produção com dados públicos, usar `L.popup().setContent(el)` com `textContent` em vez de innerHTML para campos de usuário.

---

## Commit message

```
feat(frontend): full filter panel — date range, bbox, tags, semantic search, AI curation

- Date range filters (?since=/?until=) with date inputs
- Bbox filter: "Somente área visível" checkbox + moveend auto-reload
- Tag chips in popup + ?tag= filter + tags field in new-report form
- Semantic search: purple pins layer via GET /security_reports/search
- AI curation panel: ai_suggested_category badge + confirm/correct buttons
- Update CATEGORY_COLORS and CATEGORY_LABELS for all 9 categories

Depends on: plan-000057 (9 categories), plan-000060 (tags backend),
plan-000061 (AI categorization), plan-000062 (until filter).
Part of roadmap-000056 Wave 2.
```
