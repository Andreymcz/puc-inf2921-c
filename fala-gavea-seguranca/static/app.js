const API = '/security_reports';
const GAVEA_CENTER = [-22.9756, -43.2296];
const CATEGORY_COLORS = { iluminacao: '#f0c040', transito: '#4090f0', vandalismo: '#f04040', outro: '#90c090' };
const CATEGORY_LABELS = { iluminacao: 'Iluminação', transito: 'Trânsito', vandalismo: 'Vandalismo', outro: 'Outro' };
const STATUS_LABELS = { pendente: '🔴 Pendente', em_analise: '🟡 Em análise', resolvido: '🟢 Resolvido' };

const map = L.map('map').setView(GAVEA_CENTER, 15);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  maxZoom: 19
}).addTo(map);

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
  return params.toString() ? '?' + params.toString() : '';
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

    if (lat != null && lon != null) {
      const marker = L.marker([lat, lon], { icon: makeIcon(p.category) })
        .addTo(map)
        .bindPopup(`
          <strong>${CATEGORY_LABELS[p.category] || p.category}</strong><br>
          ${p.text}<br>
          <em>${STATUS_LABELS[p.status] || p.status}</em>
          ${p.territory_name ? '<br>📍 ' + p.territory_name : ''}
          <br><small>${new Date(p.created_at).toLocaleDateString('pt-BR')}</small>
          <br><button onclick="updateStatus('${p.id}')">Atualizar status</button>
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

  const body = {
    text: document.getElementById('f-text').value,
    category: document.getElementById('f-category').value,
    author_id: 'cidadao-' + Math.random().toString(36).slice(2, 8),
    territory_name: document.getElementById('f-territory').value || null,
    lat: document.getElementById('f-lat').value ? parseFloat(document.getElementById('f-lat').value) : null,
    lon: document.getElementById('f-lon').value ? parseFloat(document.getElementById('f-lon').value) : null,
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

// Init
loadReports();
