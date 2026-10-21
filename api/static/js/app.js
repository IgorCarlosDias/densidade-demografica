/* BioAtlas — interações do front-end */
(function () {
  'use strict';

  const ICONIC = {
    Mammalia:  { color: '#c8714a', label: 'Mamífero' },
    Aves:      { color: '#3b82c4', label: 'Ave' },
    Reptilia:  { color: '#8a9a3b', label: 'Réptil' },
    Amphibia:  { color: '#2fa58a', label: 'Anfíbio' },
    Actinopterygii: { color: '#2b6cb0', label: 'Peixe' },
    Insecta:   { color: '#d69e2e', label: 'Inseto' },
    Arachnida: { color: '#7b4b2a', label: 'Aracnídeo' },
    Mollusca:  { color: '#b05f8a', label: 'Molusco' },
    Plantae:   { color: '#2f6b45', label: 'Planta' },
    Fungi:     { color: '#8b5cf6', label: 'Fungo' },
    Unknown:   { color: '#6b7a70', label: 'Ser vivo' },
  };
  const iconic = (k) => ICONIC[k] || ICONIC.Unknown;

  const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => (
    { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]
  ));
  const fmtDate = (d) => d ? new Date(d + 'T12:00:00').toLocaleDateString('pt-BR', { day: '2-digit', month: 'short', year: 'numeric' }) : 'Data desconhecida';
  const fmtNum = (n) => Number(n).toLocaleString('pt-BR');

  /* ---------- Topbar ao rolar ---------- */
  const topbar = document.querySelector('.topbar');
  const onScroll = () => topbar.classList.toggle('scrolled', window.scrollY > 40);
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- Reveal + contadores ---------- */
  const countUp = (el) => {
    const target = parseInt(el.dataset.count, 10) || 0;
    const dur = 1400, start = performance.now();
    const tick = (now) => {
      const p = Math.min((now - start) / dur, 1);
      const eased = 1 - Math.pow(1 - p, 4);
      el.textContent = fmtNum(Math.round(target * eased));
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };

  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (!e.isIntersecting) return;
      e.target.classList.add('in');
      e.target.querySelectorAll('[data-count]').forEach(countUp);
      io.unobserve(e.target);
    });
  }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
  document.querySelectorAll('.reveal').forEach((el) => io.observe(el));

  /* ---------- Loader na busca ---------- */
  const loader = document.getElementById('loader');
  const showLoader = () => loader.classList.add('show');
  document.getElementById('search-form').addEventListener('submit', showLoader);
  document.querySelectorAll('.chip').forEach((c) => c.addEventListener('click', showLoader));
  window.addEventListener('pageshow', () => loader.classList.remove('show'));

  /* ---------- Dados ---------- */
  const observacoes = JSON.parse(document.getElementById('obs-data').textContent || '[]');
  if (!observacoes.length) return;

  const results = document.getElementById('resultados');
  if (results) setTimeout(() => results.scrollIntoView({ behavior: 'smooth', block: 'start' }), 500);

  /* ---------- Mapa ---------- */
  const map = L.map('map', { scrollWheelZoom: false, zoomControl: true }).setView([-14, -52], 3);

  // Provedores 100% livres e sem exigência de API Key
  const esriTopo = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community',
    maxZoom: 18,
  });

  const esriSatellite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
    maxZoom: 18,
  });

  const osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 19,
  });

  // Camada padrão ativa: Topográfico (foco em relevo e bioma)
  esriTopo.addTo(map);

  // Seletor de visualização (Topográfico, Satélite e OpenStreetMap)
  L.control.layers({
    '🌿 Relevo & Bioma': esriTopo,
    '🛰️ Satélite': esriSatellite,
    '🗺️ OpenStreetMap': osm,
  }, null, { position: 'topright' }).addTo(map);

  map.on('click', () => map.scrollWheelZoom.enable());

  const cluster = L.markerClusterGroup({
    showCoverageOnHover: false,
    maxClusterRadius: 50,
    iconCreateFunction: (c) => {
      const n = c.getChildCount();
      const size = n < 10 ? 36 : n < 50 ? 46 : 58;
      return L.divIcon({ html: `<div class="marker-cluster-custom" style="width:${size}px;height:${size}px">${n}</div>`, className: '', iconSize: [size, size] });
    },
  });

  const markers = {};
  observacoes.forEach((o) => {
    const ic = iconic(o.iconic);
    const icon = L.divIcon({ html: `<div class="marker-pin" style="background:${ic.color}"></div>`, className: '', iconSize: [16, 16], iconAnchor: [8, 8] });
    const popup = `
      <div class="pop">
        ${o.photo ? `<img src="${esc(o.photo)}" alt="${esc(o.preferred_common_name)}" loading="lazy">` : ''}
        <div class="pop-body">
          <h5>${esc(o.preferred_common_name)}</h5>
          <i>${esc(o.scientific_name)}</i>
          <p>📍 ${esc(o.place_guess)}<br>📅 ${fmtDate(o.observed_on)}${o.observer ? `<br>👤 @${esc(o.observer)}` : ''}</p>
          <a href="https://www.inaturalist.org/observations/${encodeURIComponent(o.id)}" target="_blank" rel="noopener">Ver observação ↗</a>
        </div>
      </div>`;
    const m = L.marker([o.lat, o.lon], { icon }).bindPopup(popup, { maxWidth: 240 });
    markers[o.id] = m;
    cluster.addLayer(m);
  });
  map.addLayer(cluster);
  if (cluster.getLayers().length) map.fitBounds(cluster.getBounds().pad(0.15), { maxZoom: 8 });

  /* ---------- Galeria ---------- */
  const gallery = document.getElementById('gallery');
  const moreBtn = document.getElementById('load-more');
  const PAGE = 12;
  const withPhoto = observacoes.filter((o) => o.photo);
  let shown = 0;

  const renderPage = () => {
    const slice = withPhoto.slice(shown, shown + PAGE);
    slice.forEach((o, i) => {
      const card = document.createElement('article');
      card.className = 'obs';
      card.style.setProperty('--d', `${i * 0.06}s`);
      card.innerHTML = `
        <div class="obs-img">
          <img src="${esc(o.photo)}" alt="${esc(o.preferred_common_name)}" loading="lazy">
          <span class="badge ${o.quality === 'research' ? 'research' : ''}">${o.quality === 'research' ? '✓ Pesquisa' : iconic(o.iconic).label}</span>
        </div>
        <div class="obs-body">
          <h5>${esc(o.preferred_common_name)}</h5>
          <p class="place">📍 ${esc(o.place_guess)}</p>
          <div class="meta"><span>${fmtDate(o.observed_on)}</span><span>${o.observer ? '@' + esc(o.observer) : ''}</span></div>
        </div>`;
      card.addEventListener('click', () => {
        document.getElementById('map').scrollIntoView({ behavior: 'smooth', block: 'center' });
        setTimeout(() => cluster.zoomToShowLayer(markers[o.id], () => markers[o.id].openPopup()), 600);
      });
      gallery.appendChild(card);
    });
    shown += slice.length;
    moreBtn.hidden = shown >= withPhoto.length;
  };
  moreBtn.addEventListener('click', renderPage);
  renderPage();
})();
