/*!
 * Integral Gym Tech – visor de catálogos tipo libro.
 * Las páginas del PDF se pre-renderizan a WebP en el build; aquí solo se muestran y se animan.
 */
(() => {
  const ICONS = {
    zin: '<path d="M10 4a6 6 0 1 0 3.7 10.7l4.3 4.3 1.4-1.4-4.3-4.3A6 6 0 0 0 10 4Zm0 2a4 4 0 1 1 0 8 4 4 0 0 1 0-8Zm-1 1.5v1.5H7.5v2H9v1.5h2V11h1.5V9H11V7.5Z"/>',
    zout: '<path d="M10 4a6 6 0 1 0 3.7 10.7l4.3 4.3 1.4-1.4-4.3-4.3A6 6 0 0 0 10 4Zm0 2a4 4 0 1 1 0 8 4 4 0 0 1 0-8ZM7.5 9v2h5V9Z"/>',
    first: '<path d="M6 5h2v14H6zM19 6.4 17.6 5l-7 7 7 7 1.4-1.4L13.4 12z"/>',
    prev: '<path d="M15.4 5 14 3.6 5.6 12l8.4 8.4 1.4-1.4-7-7z"/>',
    next: '<path d="M8.6 5 10 3.6l8.4 8.4-8.4 8.4L8.6 19l7-7z"/>',
    last: '<path d="M16 5h2v14h-2zM5 6.4 6.4 5l7 7-7 7L5 17.6 10.6 12z"/>',
    share: '<path d="M17 15a3 3 0 0 0-2.2 1l-5.9-3.2a3 3 0 0 0 0-1.6L14.8 8A3 3 0 1 0 14 6l-5.9 3.2a3 3 0 1 0 0 5.6l5.9 3.2A3 3 0 1 0 17 15Z"/>',
    full: '<path d="M4 4h6v2H6v4H4zm10 0h6v6h-2V6h-4zM4 14h2v4h4v2H4zm14 0h2v6h-6v-2h4z"/>',
    dl: '<path d="M11 4h2v8.2l2.6-2.6 1.4 1.4-5 5-5-5 1.4-1.4 2.6 2.6zM5 18h14v2H5z"/>',
  };
  const svg = (k) => `<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true">${ICONS[k]}</svg>`;

  function Book(root) {
    const d = JSON.parse(root.dataset.book);
    const src = (i, big) => `${d.base}${String(i + 1).padStart(2, '0')}-${big ? 1300 : 700}.webp`;
    const stage = root.querySelector('.book__stage');
    const spread = root.querySelector('.book__spread');
    let single = innerWidth < 768;
    let pos = 0; // índice de la primera página visible
    let zoom = 1;
    let busy = false;

    const spreads = () => {
      if (single) return Array.from({ length: d.count }, (_, i) => [i]);
      const list = [[0]];
      for (let i = 1; i < d.count; i += 2) list.push(i + 1 < d.count ? [i, i + 1] : [i]);
      return list;
    };
    let S = spreads();
    const idxOf = (page) => S.findIndex((s) => s.includes(page));
    let cur = 0;

    const img = (i, cls) => {
      const el = new Image();
      el.className = 'book__page ' + (cls || '');
      el.src = src(i, false);
      el.srcset = `${src(i, false)} 1x, ${src(i, true)} 2x`;
      el.alt = d.alts[i] || `${d.title} – página ${i + 1}`;
      el.decoding = 'async';
      el.draggable = false;
      return el;
    };
    const preload = (n) => (S[n] || []).forEach((i) => { const p = new Image(); p.src = src(i, devicePixelRatio > 1); });

    const render = () => {
      const pages = S[cur];
      spread.innerHTML = '';
      spread.className = 'book__spread' + (pages.length === 1 ? ' is-single' : '');
      pages.forEach((i, k) => spread.appendChild(img(i, pages.length === 2 ? (k ? 'is-right' : 'is-left') : '')));
      input.value = String(pages[0] + 1);
      prevB.disabled = cur === 0; nextB.disabled = cur === S.length - 1;
      root.querySelectorAll('[data-a="prev"]').forEach((b) => { b.hidden = cur === 0; });
      root.querySelectorAll('[data-a="next"]').forEach((b) => { b.hidden = cur === S.length - 1; });
      preload(cur + 1); preload(cur - 1);
    };

    const turn = (to) => {
      if (busy || to < 0 || to >= S.length || to === cur) return;
      const dir = to > cur ? 1 : -1;
      const from = S[cur]; const dest = S[to];
      const canFlip = !single && from.length === 2 && dest.length === 2 && Math.abs(to - cur) === 1;
      if (!canFlip) {
        busy = true;
        spread.classList.add('is-fading');
        setTimeout(() => { cur = to; render(); spread.classList.remove('is-fading'); busy = false; }, 220);
        return;
      }
      busy = true;
      // hoja que gira sobre el lomo
      const leaf = document.createElement('div');
      leaf.className = 'book__leaf ' + (dir > 0 ? 'to-left' : 'to-right');
      const front = img(dir > 0 ? from[1] : from[0], 'front');
      const back = img(dir > 0 ? dest[0] : dest[1], 'back');
      leaf.append(front, back);
      // debajo: la página que queda descubierta
      const under = spread.querySelector(dir > 0 ? '.is-right' : '.is-left');
      under.src = src(dir > 0 ? dest[1] : dest[0], false);
      under.srcset = `${src(dir > 0 ? dest[1] : dest[0], false)} 1x, ${src(dir > 0 ? dest[1] : dest[0], true)} 2x`;
      spread.appendChild(leaf);
      requestAnimationFrame(() => requestAnimationFrame(() => leaf.classList.add('go')));
      setTimeout(() => { cur = to; render(); busy = false; }, 820);
    };

    // controles
    const mk = (a, label, cls) => `<button type="button" class="${cls}" data-a="${a}" aria-label="${label}">${svg(a === 'prev' || a === 'next' ? a : a)}</button>`;
    root.insertAdjacentHTML('beforeend',
      `${mk('prev', 'Página anterior', 'book__arrow book__arrow--prev')}${mk('next', 'Página siguiente', 'book__arrow book__arrow--next')}
      <div class="book__bar" role="toolbar" aria-label="Controles del catálogo">
        ${mk('zin', 'Acercar', 'book__b')}${mk('zout', 'Alejar', 'book__b')}${mk('first', 'Primera página', 'book__b')}
        <label class="book__num"><span class="sr">Página</span><input type="text" inputmode="numeric" value="1" aria-label="Número de página"></label>
        <span class="book__tot">${d.count}</span>
        ${mk('last', 'Última página', 'book__b')}${mk('share', 'Compartir', 'book__b')}${mk('full', 'Pantalla completa', 'book__b')}
        <a class="book__b" href="${d.pdf}" target="_blank" rel="noopener" aria-label="Descargar PDF">${svg('dl')}</a>
      </div>`);
    const input = root.querySelector('.book__num input');
    const prevB = root.querySelector('.book__arrow--prev');
    const nextB = root.querySelector('.book__arrow--next');

    const setZoom = (z) => {
      zoom = Math.min(2.5, Math.max(1, z));
      spread.style.transform = zoom > 1 ? `scale(${zoom})` : '';
      stage.classList.toggle('is-zoomed', zoom > 1);
    };
    root.addEventListener('click', (e) => {
      const b = e.target.closest('[data-a]');
      if (!b) return;
      const a = b.dataset.a;
      if (a === 'next') turn(cur + 1);
      if (a === 'prev') turn(cur - 1);
      if (a === 'first') turn(0);
      if (a === 'last') turn(S.length - 1);
      if (a === 'zin') setZoom(zoom + 0.5);
      if (a === 'zout') setZoom(zoom - 0.5);
      if (a === 'full') {
        if (document.fullscreenElement) document.exitFullscreen();
        else if (root.requestFullscreen) root.requestFullscreen();
      }
      if (a === 'share') {
        const url = location.href.split('#')[0] + '#catalogo';
        if (navigator.share) navigator.share({ title: document.title, url }).catch(() => {});
        else if (navigator.clipboard) navigator.clipboard.writeText(url).then(() => { b.classList.add('ok'); setTimeout(() => b.classList.remove('ok'), 1200); });
      }
    });
    input.addEventListener('change', () => {
      const n = Math.max(1, Math.min(d.count, parseInt(input.value, 10) || 1)) - 1;
      turn(idxOf(n));
    });
    root.tabIndex = 0;
    root.addEventListener('keydown', (e) => {
      if (e.target === input) return;
      if (e.key === 'ArrowRight') { e.preventDefault(); turn(cur + 1); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); turn(cur - 1); }
    });
    // clic sobre la página derecha/izquierda
    stage.addEventListener('click', (e) => {
      if (zoom > 1) return;
      const r = stage.getBoundingClientRect();
      turn(cur + (e.clientX > r.left + r.width / 2 ? 1 : -1));
    });
    // gestos táctiles
    let sx = 0;
    stage.addEventListener('touchstart', (e) => { sx = e.touches[0].clientX; }, { passive: true });
    stage.addEventListener('touchend', (e) => {
      const dx = e.changedTouches[0].clientX - sx;
      if (Math.abs(dx) > 40 && zoom === 1) turn(cur + (dx < 0 ? 1 : -1));
    });
    addEventListener('resize', () => {
      const s = innerWidth < 768;
      if (s !== single) { const page = S[cur][0]; single = s; S = spreads(); cur = idxOf(page); render(); }
    }, { passive: true });

    root.classList.add('is-ready');
    render();
  }

  document.querySelectorAll('[data-flipbook]').forEach((el) => { try { Book(el); } catch (e) { /* deja la portada y el enlace al PDF */ } });
})();
