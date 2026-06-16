const API = '/security_reports';
const GAVEA_CENTER = [-22.9756, -43.2296];
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
const STATUS_LABELS = { pendente: '🔴 Pendente', em_analise: '🟡 Em análise', resolvido: '🟢 Resolvido' };

// Illumination layer (lazy-loaded)
const iluminacaoLayerGroup = L.layerGroup();
let iluminacaoLoaded = false;

async function loadIluminacao() {
  if (iluminacaoLoaded) return;
  try {
    const res = await fetch('/iluminacao/geojson');
    if (!res.ok) return;
    const geojson = await res.json();
    L.geoJSON(geojson, {
      pointToLayer: (_feat, latlng) =>
        L.circleMarker(latlng, {
          radius: 3,
          color: '#f0c040',
          fillColor: '#f0c040',
          fillOpacity: 0.6,
          weight: 0,
        }),
    }).addTo(iluminacaoLayerGroup);
    iluminacaoLoaded = true;
  } catch (e) {
    console.warn('Camada de iluminação não disponível:', e);
  }
}

const map = L.map('map').setView(GAVEA_CENTER, 15);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  maxZoom: 19
}).addTo(map);

// Layer control for illumination overlay
iluminacaoLayerGroup.addTo(map);
loadIluminacao();
L.control.layers({}, { '💡 Luminárias': iluminacaoLayerGroup }, { collapsed: false }).addTo(map);

// Semantic search layer
const searchLayerGroup = L.layerGroup().addTo(map);

// Alpine.js integration: init tree on popup open
map.on('popupopen', (e) => {
  if (window.Alpine) Alpine.initTree(e.popup.getElement());
});

// Bbox auto-reload on moveend (debounced)
let bboxDebounce = null;
map.on('moveend', () => {
  if (!document.getElementById('filter-bbox').checked) return;
  clearTimeout(bboxDebounce);
  bboxDebounce = setTimeout(loadReports, 300);
});

let markers = [];
let pendingLatLng = null;
let pendingMarker = null;

function makeIcon(category) {
  const color = CATEGORY_COLORS[category] || '#888';
  return L.divIcon({
    className: '',
    html: `<div style="background:${color};width:14px;height:14px;border-radius:50%;border:2px solid white;box-shadow:0 1px 4px rgba(0,0,0,.5)"></div>`,
    iconSize: [14, 14],
    iconAnchor: [7, 7],
  });
}

function buildQueryString() {
  const params = new URLSearchParams();
  const cat = document.getElementById('filter-category').value;
  const st  = document.getElementById('filter-status').value;
  if (cat) params.set('category', cat);
  if (st)  params.set('status', st);

  const dateFrom = document.getElementById('filter-date-from').value;
  const dateTo   = document.getElementById('filter-date-to').value;
  if (dateFrom) params.set('since', new Date(dateFrom).toISOString());
  if (dateTo)   params.set('until', new Date(dateTo + 'T23:59:59').toISOString());

  if (document.getElementById('filter-bbox').checked) {
    const b = map.getBounds();
    params.set('lat_min', b.getSouth().toFixed(6));
    params.set('lat_max', b.getNorth().toFixed(6));
    params.set('lon_min', b.getWest().toFixed(6));
    params.set('lon_max', b.getEast().toFixed(6));
  }

  const tag = document.getElementById('filter-tag').value.trim();
  if (tag) params.set('tag', tag);

  return params.toString() ? '?' + params.toString() : '';
}

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
      <div x-show="state === 'idle'">
        <button @click="autocat('${p.id}')">🤖 Categorizar por IA</button>
      </div>
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
      <div x-show="loading" class="hint">⏳ Aguardando IA...</div>
      <div x-show="error" class="hint error" x-text="error"></div>
    </div>
  `;
}

async function loadReports() {
  const qs = buildQueryString();
  const res = await fetch(API + '/geojson' + qs);
  const geojson = await res.json();

  markers.forEach(m => map.removeLayer(m));
  markers = [];

  const list = document.getElementById('reports-ul');
  list.innerHTML = '';
  document.getElementById('report-count').textContent = geojson.features.length;

  geojson.features.forEach(f => {
    const p = f.properties;
    const [lon, lat] = f.geometry.coordinates;

    const tagsHtml = (p.tags || []).length > 0
      ? '<br>' + p.tags.map(t => `<span class="tag-chip">${t}</span>`).join(' ')
      : '';

    if (lat != null && lon != null) {
      const marker = L.marker([lat, lon], { icon: makeIcon(p.category) })
        .addTo(map)
        .bindPopup(`
          <strong>${CATEGORY_LABELS[p.category] || p.category}</strong><br>
          ${p.text}<br>
          <em>${STATUS_LABELS[p.status] || p.status}</em>
          ${p.territory_name ? '<br>📍 ' + p.territory_name : ''}
          ${tagsHtml}
          <br><small>${new Date(p.created_at).toLocaleDateString('pt-BR')}</small>
          <br><button onclick="updateStatus('${p.id}')">Atualizar status</button>
          ${buildCurationPanel(p)}
        `);
      markers.push(marker);
    }

    const li = document.createElement('li');
    li.innerHTML = `
      <div class="r-category">${CATEGORY_LABELS[p.category] || p.category}</div>
      <div class="r-text">${p.text}</div>
      <div class="r-status">${STATUS_LABELS[p.status] || p.status}${p.territory_name ? ' · ' + p.territory_name : ''}</div>
    `;
    if (lat != null && lon != null) {
      li.onclick = () => { map.setView([lat, lon], 17); };
    }
    list.appendChild(li);
  });
}

async function updateStatus(id) {
  const s = prompt('Novo status: pendente | em_analise | resolvido');
  if (!s) return;
  const res = await fetch(`${API}/${id}/status`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ status: s }),
  });
  if (res.ok) { map.closePopup(); loadReports(); }
  else { alert('Erro ao atualizar: ' + (await res.json()).detail); }
}

// New report form
document.getElementById('btn-new-report').onclick = () => {
  document.getElementById('form-panel').classList.remove('hidden');
  document.getElementById('f-coords-hint').textContent = 'Clique no mapa para definir a localização.';
  document.getElementById('f-lat').value = '';
  document.getElementById('f-lon').value = '';
};

document.getElementById('btn-cancel').onclick = () => {
  document.getElementById('form-panel').classList.add('hidden');
  if (pendingMarker) { map.removeLayer(pendingMarker); pendingMarker = null; }
  pendingLatLng = null;
};

map.on('click', (e) => {
  if (!document.getElementById('form-panel').classList.contains('hidden')) {
    pendingLatLng = e.latlng;
    document.getElementById('f-lat').value = e.latlng.lat.toFixed(6);
    document.getElementById('f-lon').value = e.latlng.lng.toFixed(6);
    document.getElementById('f-coords-hint').textContent =
      `📍 ${e.latlng.lat.toFixed(5)}, ${e.latlng.lng.toFixed(5)}`;
    if (pendingMarker) map.removeLayer(pendingMarker);
    pendingMarker = L.circleMarker(e.latlng, { radius: 8, color: '#e94560', fillOpacity: 0.8 }).addTo(map);
  }
});

document.getElementById('report-form').onsubmit = async (ev) => {
  ev.preventDefault();
  const errEl = document.getElementById('f-error');
  errEl.classList.add('hidden');

  const tagsRaw = document.getElementById('f-tags').value;
  const body = {
    text: document.getElementById('f-text').value,
    category: document.getElementById('f-category').value,
    author_id: 'cidadao-' + Math.random().toString(36).slice(2, 8),
    territory_name: document.getElementById('f-territory').value || null,
    lat: document.getElementById('f-lat').value ? parseFloat(document.getElementById('f-lat').value) : null,
    lon: document.getElementById('f-lon').value ? parseFloat(document.getElementById('f-lon').value) : null,
    tags: tagsRaw ? tagsRaw.split(',').map(t => t.trim()).filter(Boolean) : [],
  };

  const res = await fetch(API + '/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });

  if (res.ok) {
    document.getElementById('form-panel').classList.add('hidden');
    document.getElementById('report-form').reset();
    if (pendingMarker) { map.removeLayer(pendingMarker); pendingMarker = null; }
    loadReports();
  } else {
    const err = await res.json();
    errEl.textContent = 'Erro: ' + (err.detail || JSON.stringify(err));
    errEl.classList.remove('hidden');
  }
};

document.getElementById('btn-apply-filters').onclick = loadReports;

document.getElementById('btn-refresh-iluminacao').onclick = async () => {
  const statusEl = document.getElementById('iluminacao-status');
  statusEl.textContent = 'Baixando...';
  try {
    const res = await fetch('/iluminacao/refresh', { method: 'POST' });
    if (res.ok) {
      statusEl.textContent = 'Download iniciado. Recarregue a página em alguns segundos.';
    } else {
      statusEl.textContent = 'Erro ao iniciar download.';
    }
  } catch (e) {
    statusEl.textContent = 'Erro: ' + e.message;
  }
};

// Semantic search
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

// Init
loadReports();
