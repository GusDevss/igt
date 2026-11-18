/*!
 * Integral Gym Tech – tienda: filtros del catálogo, lista de cotización, galería del producto.
 */
(() => {
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => Array.from(c.querySelectorAll(s));
  const norm = (s) => (s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
  const KEY = 'igt-cotizacion';

  /* ------------------------------------------------------------ catálogo: filtros, búsqueda y orden */
  function catalog() {
    const root = $('[data-shop]');
    if (!root) return;
    const grid = $('[data-grid]', root);
    const cards = $$('.prd', grid);
    cards.forEach((c, i) => { c.dataset.i = i; });
    const q = $('[data-filter-q]', root);
    const sort = $('[data-sort]', root);
    const count = $('[data-shop-count]', root);
    const none = $('[data-none]', root);
    const active = $('[data-active]', root);
    const catBtns = $$('[data-filter-cat]', root);
    const muscBtns = $$('[data-filter-musc]', root);
    const CAT_NAMES = {};
    catBtns.forEach((b) => { CAT_NAMES[b.dataset.filterCat] = $('span', b).textContent; });
    const params = new URLSearchParams(location.search);
    const state = { cat: params.get('categoria') || '', musc: params.getAll('musculo'), q: params.get('q') || '', sort: params.get('orden') || 'feat' };

    const apply = (push) => {
      const words = norm(state.q).split(/\s+/).filter(Boolean);
      let n = 0;
      cards.forEach((c) => {
        const hay = norm(c.dataset.name + ' ' + c.dataset.tags);
        const musc = c.dataset.musc.split('|');
        const ok = (!state.cat || c.dataset.cat === state.cat)
          && (!state.musc.length || state.musc.some((m) => musc.includes(m)))
          && words.every((w) => hay.includes(w));
        c.hidden = !ok;
        if (ok) n += 1;
      });
      // orden
      const by = {
        feat: (a, b) => (b.dataset.feat - a.dataset.feat) || (a.dataset.i - b.dataset.i),
        az: (a, b) => a.dataset.name.localeCompare(b.dataset.name, 'es'),
        za: (a, b) => b.dataset.name.localeCompare(a.dataset.name, 'es'),
        cat: (a, b) => a.dataset.cat.localeCompare(b.dataset.cat) || a.dataset.name.localeCompare(b.dataset.name, 'es'),
      }[state.sort] || (() => 0);
      const sorted = cards.slice().sort(by);
      if (push || state.sort !== 'feat' || sorted.some((c, i) => grid.children[i] !== c)) sorted.forEach((c) => grid.appendChild(c));
      // UI
      catBtns.forEach((b) => { const on = b.dataset.filterCat === state.cat; b.classList.toggle('is-on', on); b.setAttribute('aria-pressed', String(on)); });
      muscBtns.forEach((b) => { const on = state.musc.includes(b.dataset.filterMusc); b.classList.toggle('is-on', on); b.setAttribute('aria-pressed', String(on)); });
      count.textContent = `Mostrando ${n} ${n === 1 ? 'producto' : 'productos'}`;
      none.hidden = n > 0;
      const tags = [];
      if (state.cat) tags.push(['cat', state.cat, CAT_NAMES[state.cat]]);
      state.musc.forEach((m) => tags.push(['musc', m, m]));
      if (state.q) tags.push(['q', state.q, `“${state.q}”`]);
      active.innerHTML = tags.map(([t, v, l]) => `<button type="button" class="chip is-on" data-rm="${t}" data-v="${v}">${l} <span aria-hidden="true">×</span><span class="sr">Quitar filtro</span></button>`).join('')
        + (tags.length ? '<button type="button" class="link" data-reset>Limpiar todo</button>' : '');
      // animación de entrada
      if (push) { grid.classList.remove('is-anim'); void grid.offsetWidth; grid.classList.add('is-anim'); }
      // URL compartible
      const p = new URLSearchParams();
      if (state.cat) p.set('categoria', state.cat);
      state.musc.forEach((m) => p.append('musculo', m));
      if (state.q) p.set('q', state.q);
      if (state.sort !== 'feat') p.set('orden', state.sort);
      const url = location.pathname + (p.toString() ? '?' + p : '');
      if (push) history.replaceState(null, '', url);
    };

    catBtns.forEach((b) => b.addEventListener('click', () => { state.cat = b.dataset.filterCat; apply(true); if (innerWidth < 1024) grid.scrollIntoView({ behavior: 'smooth', block: 'start' }); }));
    muscBtns.forEach((b) => b.addEventListener('click', () => {
      const m = b.dataset.filterMusc;
      state.musc = state.musc.includes(m) ? state.musc.filter((x) => x !== m) : state.musc.concat(m);
      apply(true);
    }));
    let t = 0;
    q.addEventListener('input', () => { clearTimeout(t); t = setTimeout(() => { state.q = q.value.trim(); apply(true); }, 160); });
    sort.addEventListener('change', () => { state.sort = sort.value; apply(true); });
    root.addEventListener('click', (e) => {
      const rm = e.target.closest('[data-rm]');
      if (rm) {
        if (rm.dataset.rm === 'cat') state.cat = '';
        if (rm.dataset.rm === 'musc') state.musc = state.musc.filter((x) => x !== rm.dataset.v);
        if (rm.dataset.rm === 'q') { state.q = ''; q.value = ''; }
        apply(true);
      }
      if (e.target.closest('[data-reset]')) { state.cat = ''; state.musc = []; state.q = ''; q.value = ''; apply(true); }
    });
    q.value = state.q; sort.value = state.sort;
    if (state.cat || state.musc.length || state.q || state.sort !== 'feat') apply(false);
  }

  /* ------------------------------------------------------------ lista de cotización */
  const load = () => { try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch (e) { return []; } };
  const save = (l) => { try { localStorage.setItem(KEY, JSON.stringify(l)); } catch (e) { /* sin almacenamiento */ } };

  function quote() {
    let list = load();
    const listEl = $('[data-quote-list]');
    const empty = $('[data-quote-empty]');
    const form = $('[data-quote-form]');
    const wa = $('[data-quote-wa]');
    const out = form && $('.quote__out', form);
    const counters = $$('[data-quote-count]');
    const btn = $('.qbtn');

    const text = () => list.map((i) => `• ${i.name} — ${i.qty} ${i.unit === 'kg' ? 'kg' : (i.qty === 1 ? 'pieza' : 'piezas')}`).join('\n');
    const render = () => {
      const total = list.reduce((n, i) => n + (i.unit === 'kg' ? 1 : i.qty), 0);
      counters.forEach((c) => { c.textContent = total; });
      if (btn) btn.classList.toggle('has-items', list.length > 0);
      if (!listEl) return;
      empty.hidden = list.length > 0;
      form.hidden = list.length === 0;
      listEl.innerHTML = list.map((i) => `
        <li class="qitem" data-slug="${i.slug}">
          <a href="/productos/${i.slug}/" class="qitem__n">${i.name}</a>
          <div class="qty qty--sm"><button type="button" data-q-step="-1" aria-label="Menos">−</button><input type="number" min="1" value="${i.qty}" aria-label="Cantidad de ${i.name}" data-q-input><button type="button" data-q-step="1" aria-label="Más">+</button><span class="qty__u">${i.unit === 'kg' ? 'kg' : 'pzas'}</span></div>
          <button type="button" class="qitem__rm" data-q-rm aria-label="Quitar ${i.name}">×</button>
        </li>`).join('');
      if (form) form.elements.productos.value = text();
      if (wa) wa.href = 'https://wa.me/5214421270018?text=' + encodeURIComponent('Hola, me gustaría cotizar los siguientes equipos:\n' + text());
    };
    const add = (slug, name, unit, qty) => {
      const it = list.find((i) => i.slug === slug);
      if (it) it.qty += qty; else list.push({ slug, name, unit, qty });
      save(list); render();
    };

    document.addEventListener('click', (e) => {
      const b = e.target.closest('[data-quote-add]');
      if (!b) return;
      let qty = 1;
      if (b.hasAttribute('data-use-qty')) { const inp = $('[data-qty-input]'); qty = Math.max(1, parseInt(inp && inp.value, 10) || 1); }
      add(b.dataset.slug, b.dataset.name, b.dataset.unit, qty);
      b.classList.add('is-added');
      const label = $('span:not(.sr)', b) || b;
      const prev = label.textContent;
      label.textContent = b.classList.contains('pdp__add') ? 'Agregado a tu cotización' : 'Agregado';
      setTimeout(() => { b.classList.remove('is-added'); label.textContent = prev; }, 1600);
      if (btn) { btn.classList.remove('bump'); void btn.offsetWidth; btn.classList.add('bump'); }
    });
    if (listEl) {
      listEl.addEventListener('click', (e) => {
        const li = e.target.closest('.qitem'); if (!li) return;
        const it = list.find((i) => i.slug === li.dataset.slug);
        if (e.target.closest('[data-q-rm]')) list = list.filter((i) => i !== it);
        const st = e.target.closest('[data-q-step]');
        if (st) it.qty = Math.max(1, it.qty + +st.dataset.qStep);
        save(list); render();
      });
      listEl.addEventListener('change', (e) => {
        const li = e.target.closest('.qitem'); if (!li || !e.target.matches('[data-q-input]')) return;
        const it = list.find((i) => i.slug === li.dataset.slug);
        it.qty = Math.max(1, parseInt(e.target.value, 10) || 1); save(list); render();
      });
    }
    if (form) {
      if (form.elements.ts) form.elements.ts.value = String(Date.now());
      form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const f = form.elements;
        const okMail = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(f['your-email'].value.trim());
        const okTel = f['your-tel'].value.replace(/\D/g, '').length >= 8;
        const okName = f['your-name'].value.trim().length > 1;
        [['your-name', okName], ['your-email', okMail], ['your-tel', okTel]].forEach(([n, ok]) => f[n].classList.toggle('is-bad', !ok));
        if (!okName || !okMail || !okTel) { out.textContent = 'Revisa tu nombre, correo y teléfono.'; out.className = 'quote__out is-err'; return; }
        out.textContent = 'Enviando…'; out.className = 'quote__out';
        const data = new FormData(form); data.append('ajax', '1');
        try {
          const r = await fetch(form.action, { method: 'POST', body: data, headers: { Accept: 'application/json' } });
          const res = await r.json().catch(() => ({}));
          if (res.ok) {
            out.textContent = '¡Listo! Recibimos tu cotización; un asesor te contactará muy pronto.'; out.className = 'quote__out is-ok';
            list = []; save(list); setTimeout(render, 2500);
            if (window.dataLayer) window.dataLayer.push({ event: 'generate_lead', form: 'cotizacion_productos' });
          } else { out.textContent = res.message || 'No pudimos enviar tu cotización. Inténtalo de nuevo o envíala por WhatsApp.'; out.className = 'quote__out is-err'; }
        } catch (err) { out.textContent = 'No pudimos enviar tu cotización. Envíala por WhatsApp.'; out.className = 'quote__out is-err'; }
      });
    }
    render();
    addEventListener('storage', (e) => { if (e.key === KEY) { list = load(); render(); } });
  }

  /* ------------------------------------------------------------ ficha de producto */
  function product() {
    const g = $('[data-gallery]');
    if (!g) return;
    const slides = $$('[data-slide]', g);
    const thumbs = $$('[data-thumb]', g);
    thumbs.forEach((t) => t.addEventListener('click', () => {
      const i = +t.dataset.thumb;
      slides.forEach((s) => s.classList.toggle('is-on', +s.dataset.slide === i));
      thumbs.forEach((x) => x.classList.toggle('is-on', x === t));
    }));
    const stage = $('[data-zoom].is-zoomable', g);
    if (stage && matchMedia('(hover:hover)').matches) {
      stage.addEventListener('mousemove', (e) => {
        const r = stage.getBoundingClientRect();
        stage.style.setProperty('--zx', ((e.clientX - r.left) / r.width * 100) + '%');
        stage.style.setProperty('--zy', ((e.clientY - r.top) / r.height * 100) + '%');
      });
      stage.addEventListener('mouseenter', () => stage.classList.add('is-zoom'));
      stage.addEventListener('mouseleave', () => stage.classList.remove('is-zoom'));
    }
    $$('[data-qty]').forEach((q) => {
      const inp = $('input', q);
      $$('[data-step]', q).forEach((b) => b.addEventListener('click', () => {
        inp.value = Math.max(1, (parseInt(inp.value, 10) || 1) + +b.dataset.step);
      }));
    });
    // mensaje sugerido en el formulario de contacto
    const msg = $('#f-mensaje');
    const name = $('.pdp__t');
    if (msg && name && !msg.value) msg.value = `Hola, me interesa cotizar: ${name.textContent.trim()}.`;
  }

  catalog();
  quote();
  product();
})();
