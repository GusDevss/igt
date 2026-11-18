/*!
 * Integral Gym Tech – interacciones del sitio (sin dependencias)
 */
const $ = (s, c = document) => c.querySelector(s);
const $$ = (s, c = document) => Array.from(c.querySelectorAll(s));
const root = document.documentElement;
const finePointer = matchMedia('(hover:hover) and (pointer:fine)').matches;
const reduceMotion = matchMedia('(prefers-reduced-motion:reduce)').matches;

/* ------------------------------------------------------------ cabecera fija */
function stickyHeader() {
  let ticking = false;
  const update = () => {
    document.body.classList.toggle('is-stuck', scrollY > 100);
    ticking = false;
  };
  addEventListener('scroll', () => { if (!ticking) { requestAnimationFrame(update); ticking = true; } }, { passive: true });
  update();
}

/* ------------------------------------------------------------ panel lateral y menú móvil */
function overlays() {
  let lastFocus = null;
  const open = (el, btn) => {
    lastFocus = btn;
    el.classList.add('is-open');
    el.setAttribute('aria-hidden', 'false');
    if (btn) btn.setAttribute('aria-expanded', 'true');
    root.style.overflow = 'hidden';
    const f = $('button, a, input', el);
    if (f) setTimeout(() => f.focus({ preventScroll: true }), 50);
  };
  const close = (el) => {
    el.classList.remove('is-open');
    el.setAttribute('aria-hidden', 'true');
    $$(`[aria-controls="${el.id}"]`).forEach((b) => b.setAttribute('aria-expanded', 'false'));
    root.style.overflow = '';
    if (lastFocus) lastFocus.focus({ preventScroll: true });
  };
  $$('[data-open]').forEach((btn) => btn.addEventListener('click', () => open($('#' + btn.dataset.open), btn)));
  $$('.panel, .mnav').forEach((el) => {
    $$('[data-close]', el).forEach((c) => c.addEventListener('click', () => close(el)));
    $$('a[href^="#"]', el).forEach((a) => a.addEventListener('click', () => close(el)));
  });
  addEventListener('keydown', (e) => {
    if (e.key === 'Escape') $$('.panel.is-open, .mnav.is-open').forEach(close);
  });
  // submenús del menú móvil
  $$('.mnav__item.has-sub').forEach((li) => {
    const t = $('.mnav__toggle', li);
    const sub = $('.mnav__sub', li);
    const toggle = (e) => {
      e.preventDefault();
      const on = !sub.classList.contains('is-open');
      sub.classList.toggle('is-open', on);
      t.setAttribute('aria-expanded', String(on));
    };
    t.addEventListener('click', toggle);
    const link = $('.mnav__link', li);
    if (!link.hasAttribute('data-real')) link.addEventListener('click', toggle);
  });
  // menú de escritorio: los enlaces "#" no navegan
  $$('.nav__item.has-sub > .nav__link:not([data-real])').forEach((a) => a.addEventListener('click', (e) => e.preventDefault()));
}

/* ------------------------------------------------------------ búsqueda (menú móvil) */
const SEARCH = [
  ['/cardio/', 'cardio caminadora caminadoras eliptica elipticas bicicleta spinning remo escaladora'],
  ['/peso-libre/', 'peso libre mancuernas discos barras rack racks bumpers bancos'],
  ['/peso-integrado/', 'peso integrado maquinas fuerza prensa polea jalon'],
  ['/multifuncionales/', 'multifuncional multifuncionales multiestacion crossover'],
  ['/pilates/', 'pilates reformer cadillac chair'],
  ['/accesorios/', 'accesorios kettlebell ligas tapetes piso funcional'],
  ['/reacondicionado/', 'reacondicionado seminuevo usado usados'],
  ['/mantenimiento-de-equipo/', 'mantenimiento reparacion servicio tecnico preventivo correctivo'],
  ['/arrendamiento/', 'arrendamiento leasing financiamiento credito mensualidades'],
  ['/diseno-de-espacios/', 'diseno render 3d espacios layout'],
  ['/gimnasio-casa/', 'casa hogar home gym'],
  ['/hoteles/', 'hotel hoteles'], ['/empresas/', 'empresa empresas corporativo'],
  ['/universidades/', 'universidad universidades escuela'], ['/gubernamentales/', 'gobierno gubernamental municipio'],
  ['/clinicas-fisioterapia/', 'clinica fisioterapia rehabilitacion'], ['/estudio-pilates/', 'estudio pilates'],
  ['/condominios-residenciales/', 'condominio condominios residencial fraccionamiento'],
  ['/gimnasio-apertura-remodelacion/', 'apertura remodelacion abrir gimnasio'],
  ['/nosotros/', 'nosotros igt empresa quienes somos buge'],
  ['/productos/', 'productos tienda catalogo comprar venta equipo maquina maquinas rack smith banco mancuerna disco'],
];
function search() {
  $$('[data-search]').forEach((f) => f.addEventListener('submit', (e) => {
    e.preventDefault();
    const q = f.q.value.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').trim();
    if (!q) return;
    let best = null; let score = 0;
    SEARCH.forEach(([url, words]) => {
      const s = q.split(/\s+/).reduce((n, w) => n + (words.includes(w) ? 2 : words.split(' ').some((x) => x.startsWith(w)) ? 1 : 0), 0);
      if (s > score) { score = s; best = url; }
    });
    location.href = best || '/#contacto';
  }));
}

/* ------------------------------------------------------------ texto de contorno: ajusta el SVG al texto */
function strokes() {
  const fit = () => $$('svg.stroke').forEach((svg) => {
    const t = svg.querySelector('text');
    if (!t) return;
    try {
      const b = t.getBBox();
      if (b.width) { svg.setAttribute('width', Math.ceil(b.width)); svg.setAttribute('height', Math.ceil(b.height)); }
    } catch (e) { /* noop */ }
  });
  fit();
  if (document.fonts) document.fonts.ready.then(fit);
  addEventListener('resize', fit, { passive: true });
}

/* ------------------------------------------------------------ animaciones al entrar en pantalla */
function reveal() {
  const els = $$('[data-reveal]');
  if (!els.length) return;
  if (reduceMotion || !('IntersectionObserver' in window)) { els.forEach((e) => e.classList.add('is-in')); return; }
  const io = new IntersectionObserver((entries) => entries.forEach((en) => {
    if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
  }), { rootMargin: '0px 0px -60px 0px' });
  els.forEach((e) => io.observe(e));
}

/* ------------------------------------------------------------ letras que giran en los botones */
function wobble() {
  if (!finePointer) return;
  $$('[data-wobble]').forEach((el) => {
    const host = el.closest('.btn') || el;
    let busy = false;
    host.addEventListener('mouseenter', () => {
      if (busy) return;
      busy = true;
      if (!el.dataset.split) {
        const txt = el.textContent;
        el.setAttribute('aria-label', txt);
        el.innerHTML = Array.from(txt).map((c) => `<span aria-hidden="true">${c === ' ' ? '&nbsp;' : c}</span>`).join('');
        el.dataset.split = '1';
      }
      const letters = $$('span', el);
      letters.forEach((s, i) => setTimeout(() => {
        s.classList.remove('spin'); void s.offsetWidth; s.classList.add('spin');
      }, 50 * i));
      setTimeout(() => { busy = false; }, (letters.length + 1) * 50 + 300);
    });
  });
}

/* ------------------------------------------------------------ cursor personalizado */
function cursor() {
  const c = $('.cursor');
  if (!c || !finePointer || reduceMotion) return;
  let x = -100; let y = -100; let cx = x; let cy = y; let raf = 0;
  const loop = () => {
    cx += (x - cx) * 0.18; cy += (y - cy) * 0.18;
    c.style.transform = `translate3d(${cx}px,${cy}px,0)`;
    raf = Math.abs(x - cx) + Math.abs(y - cy) > 0.3 ? requestAnimationFrame(loop) : 0;
  };
  addEventListener('mousemove', (e) => {
    x = e.clientX; y = e.clientY;
    document.body.classList.add('has-cursor');
    if (!raf) raf = requestAnimationFrame(loop);
  }, { passive: true });
  document.addEventListener('mouseleave', () => document.body.classList.remove('has-cursor'));
  document.addEventListener('mouseover', (e) => c.classList.toggle('is-link', !!e.target.closest('a, button')));
}

/* ------------------------------------------------------------ contadores */
function counters() {
  const els = $$('[data-count]');
  if (!els.length) return;
  const run = (el) => {
    const end = +el.dataset.count; const start = +(el.dataset.from || 0); const dur = 2000; const t0 = performance.now();
    const step = (t) => {
      const p = Math.min(1, (t - t0) / dur);
      el.textContent = Math.round(start + (end - start) * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };
  if (reduceMotion || !('IntersectionObserver' in window)) { els.forEach((e) => { e.textContent = e.dataset.count; }); return; }
  const io = new IntersectionObserver((en) => en.forEach((x) => { if (x.isIntersecting) { run(x.target); io.unobserve(x.target); } }), { threshold: 0.4 });
  els.forEach((e) => io.observe(e));
}

/* ------------------------------------------------------------ pestañas "¿Por qué elegirnos?" */
function tabs() {
  $$('[data-tabs]').forEach((box) => {
    const btns = $$('[role="tab"]', box);
    const select = (b) => {
      btns.forEach((x) => { const on = x === b; x.setAttribute('aria-selected', String(on)); x.tabIndex = on ? 0 : -1; });
      $$('[role="tabpanel"]', box).forEach((p) => {
        const on = p.id === b.getAttribute('aria-controls');
        p.hidden = !on;
        if (on) { p.classList.remove('is-in'); void p.offsetWidth; p.classList.add('is-in'); }
      });
    };
    btns.forEach((b, i) => {
      b.addEventListener('click', () => select(b));
      b.addEventListener('keydown', (e) => {
        const d = { ArrowDown: 1, ArrowRight: 1, ArrowUp: -1, ArrowLeft: -1 }[e.key];
        if (d) { e.preventDefault(); const n = btns[(i + d + btns.length) % btns.length]; n.focus(); select(n); }
      });
    });
  });
}

/* ------------------------------------------------------------ carrusel ligero */
function carousels() {
  $$('[data-carousel]').forEach((el) => {
    const track = $('.car__track', el);
    const slides = $$('.car__slide', el);
    if (!track || slides.length < 2) return;
    const opts = JSON.parse(el.dataset.carousel || '{}');
    let i = 0; let timer = 0;
    const perView = () => {
      const w = innerWidth; const bp = opts.bp || {};
      let v = opts.view || 1;
      Object.keys(bp).map(Number).sort((a, b) => a - b).forEach((k) => { if (w >= k) v = bp[k]; });
      return v;
    };
    const max = () => Math.max(0, slides.length - perView());
    const go = (n, anim = true) => {
      const m = max();
      i = opts.loop ? (n > m ? 0 : n < 0 ? m : n) : Math.max(0, Math.min(m, n));
      track.style.transition = anim ? '' : 'none';
      track.style.transform = `translateX(${-i * (100 / perView())}%)`;
      $$('[data-dir]', el).forEach((b) => { if (!opts.loop) b.disabled = (b.dataset.dir < 0 && i === 0) || (b.dataset.dir > 0 && i === m); });
    };
    const layout = () => { el.style.setProperty('--view', perView()); go(i, false); };
    $$('[data-dir]', el).forEach((b) => b.addEventListener('click', () => { go(i + +b.dataset.dir); restart(); }));
    const restart = () => {
      clearInterval(timer);
      if (opts.autoplay && !reduceMotion) timer = setInterval(() => go(i + 1), opts.autoplay);
    };
    if (opts.pause) { el.addEventListener('mouseenter', () => clearInterval(timer)); el.addEventListener('mouseleave', restart); }
    // gestos táctiles
    let sx = 0;
    track.addEventListener('touchstart', (e) => { sx = e.touches[0].clientX; }, { passive: true });
    track.addEventListener('touchend', (e) => { const dx = e.changedTouches[0].clientX - sx; if (Math.abs(dx) > 40) { go(i + (dx < 0 ? 1 : -1)); restart(); } });
    addEventListener('resize', layout, { passive: true });
    layout(); restart();
  });
}

/* ------------------------------------------------------------ galerías "justified" (filas que llenan el ancho) */
function justify() {
  const gals = $$('[data-justify]');
  if (!gals.length) return;
  const GAP = 10;
  const layout = (g) => {
    const o = JSON.parse(g.dataset.justify);
    const items = $$('.gal__item', g);
    const ratios = items.map((a) => parseFloat(a.style.getPropertyValue('--r')) || 1);
    const W = g.clientWidth;
    if (!W) return;
    const H = innerWidth <= 1366 ? o.hl : o.h;
    const rows = [];
    let start = 0; let acc = 0; let widths = [];
    for (let i = 0; i < items.length; i++) {
      let w = Math.round(H * ratios[i]);
      if (w > W) w = W;
      const next = acc + w;
      if (next > W && W - acc < next - W && i > start) {
        rows.push({ from: start, to: i, sum: acc, widths }); start = i; acc = 0; widths = []; i -= 1; continue;
      }
      widths.push(w); acc = next;
      if (i === items.length - 1) rows.push({ from: start, to: i + 1, sum: (acc / W >= 0.7 ? acc : W), widths });
    }
    let y = 0;
    rows.forEach((r) => {
      const n = r.to - r.from;
      const avail = W - (n - 1) * GAP;
      let x = 0; let h = 0;
      for (let k = 0; k < n; k++) {
        const it = items[r.from + k];
        const w = (r.widths[k] / r.sum) * avail;
        if (!k) h = w / ratios[r.from];
        Object.assign(it.style, { left: x + 'px', top: y + 'px', width: w + 'px', height: h + 'px' });
        x += w + GAP;
      }
      y += h + GAP;
    });
    g.style.height = Math.max(0, y - GAP) + 'px';
    g.classList.add('is-justified');
  };
  const all = () => gals.forEach(layout);
  all();
  let t = 0;
  addEventListener('resize', () => { clearTimeout(t); t = setTimeout(all, 80); }, { passive: true });
}

/* ------------------------------------------------------------ fondos diferidos y animaciones solo en pantalla */
function lazyStuff() {
  const bgs = $$('.bg--lazy');
  const strokes = $$('svg.stroke--draw');
  if (!('IntersectionObserver' in window)) { bgs.forEach((e) => e.classList.add('bg-on')); return; }
  const io = new IntersectionObserver((en) => en.forEach((x) => {
    if (x.isIntersecting) { x.target.classList.add('bg-on'); io.unobserve(x.target); }
  }), { rootMargin: '600px 0px' });
  bgs.forEach((e) => io.observe(e));
  const play = new IntersectionObserver((en) => en.forEach((x) => x.target.classList.toggle('is-off', !x.isIntersecting)));
  strokes.forEach((s) => { s.classList.add('is-off'); play.observe(s); });
}

/* ------------------------------------------------------------ lightbox (galerías y video) */
function lightbox() {
  const items = $$('[data-lightbox]');
  if (!items.length) return;
  const lb = document.createElement('div');
  lb.className = 'lb';
  lb.setAttribute('role', 'dialog');
  lb.setAttribute('aria-modal', 'true');
  lb.innerHTML = '<span class="lb__count"></span><div class="lb__media"></div><button class="lb__btn lb__close" aria-label="Cerrar">&times;</button><button class="lb__btn lb__prev" aria-label="Anterior">&#8249;</button><button class="lb__btn lb__next" aria-label="Siguiente">&#8250;</button>';
  document.body.appendChild(lb);
  let group = []; let i = 0;
  const show = () => {
    const a = group[i];
    const media = $('.lb__media', lb);
    media.innerHTML = a.dataset.lightbox === 'video'
      ? `<video src="${a.getAttribute('href')}" controls autoplay playsinline></video>`
      : `<img src="${a.getAttribute('href')}" alt="${(a.querySelector('img') || {}).alt || ''}">`;
    $('.lb__count', lb).textContent = group.length > 1 ? `${i + 1} / ${group.length}` : '';
    $$('.lb__prev, .lb__next', lb).forEach((b) => { b.hidden = group.length < 2; });
  };
  const close = () => { lb.classList.remove('is-open'); $('.lb__media', lb).innerHTML = ''; root.style.overflow = ''; };
  items.forEach((a) => a.addEventListener('click', (e) => {
    e.preventDefault();
    const g = a.dataset.group;
    group = g ? items.filter((x) => x.dataset.group === g) : [a];
    i = group.indexOf(a);
    lb.classList.add('is-open'); root.style.overflow = 'hidden'; show();
    $('.lb__close', lb).focus();
  }));
  $('.lb__close', lb).addEventListener('click', close);
  lb.addEventListener('click', (e) => { if (e.target === lb) close(); });
  $('.lb__prev', lb).addEventListener('click', () => { i = (i - 1 + group.length) % group.length; show(); });
  $('.lb__next', lb).addEventListener('click', () => { i = (i + 1) % group.length; show(); });
  addEventListener('keydown', (e) => {
    if (!lb.classList.contains('is-open')) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowLeft') $('.lb__prev', lb).click();
    if (e.key === 'ArrowRight') $('.lb__next', lb).click();
  });
}

/* ------------------------------------------------------------ formulario de contacto */
const MSG = {
  required: 'Por favor, completa este campo.',
  email: 'Ingresa un correo electrónico válido.',
  tel: 'Ingresa un número de teléfono válido.',
  invalid: 'Uno o más campos tienen un error. Por favor, revísalos e inténtalo de nuevo.',
  sent: '¡Gracias por tu mensaje! Un asesor de Integral Gym Tech te contactará muy pronto.',
  failed: 'Hubo un error al enviar tu mensaje. Inténtalo de nuevo o escríbenos por WhatsApp al 442 127 0018.',
};
function forms() {
  $$('[data-form]').forEach((form) => {
    const out = $('.form__out', form);
    const ts = form.elements.ts;
    if (ts) ts.value = String(Date.now());
    const state = (s, text) => {
      form.classList.remove('sent', 'invalid', 'failed', 'submitting');
      if (s) form.classList.add(s);
      if (text !== undefined) out.textContent = text;
    };
    const tip = (field, text) => {
      const wrap = field.closest('.field');
      wrap.classList.add('is-invalid');
      field.setAttribute('aria-invalid', 'true');
      const t = document.createElement('span');
      t.className = 'tip';
      t.textContent = text;
      wrap.appendChild(t);
    };
    const clear = () => {
      $$('.tip', form).forEach((t) => t.remove());
      $$('.is-invalid', form).forEach((f) => f.classList.remove('is-invalid'));
      $$('[aria-invalid]', form).forEach((f) => f.removeAttribute('aria-invalid'));
    };
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      clear();
      let ok = true;
      $$('input:not([type=hidden]), select, textarea', form).forEach((f) => {
        if (f.closest('.form__hp')) return;
        const v = f.value.trim();
        if (f.required && !v) { tip(f, MSG.required); ok = false; return; }
        if (v && f.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) { tip(f, MSG.email); ok = false; return; }
        if (v && f.type === 'tel' && v.replace(/\D/g, '').length < 8) { tip(f, MSG.tel); ok = false; }
      });
      if (!ok) { state('invalid', MSG.invalid); return; }
      state('submitting');
      try {
        const data = new FormData(form);
        data.append('ajax', '1');
        const r = await fetch(form.action, { method: 'POST', body: data, headers: { Accept: 'application/json' } });
        const res = await r.json().catch(() => ({}));
        if (res.ok) {
          state('sent', MSG.sent);
          form.reset();
          if (ts) ts.value = String(Date.now());
          if (window.dataLayer) window.dataLayer.push({ event: 'generate_lead', form: 'contacto' });
          if (typeof window.gtag === 'function') window.gtag('event', 'generate_lead');
          if (typeof window.fbq === 'function') window.fbq('track', 'Lead');
        } else if (res.errors) {
          Object.entries(res.errors).forEach(([n, m]) => { const f = form.elements[n]; if (f) tip(f, m); });
          state('invalid', MSG.invalid);
        } else {
          state('failed', res.message || MSG.failed);
        }
      } catch (err) {
        state('failed', MSG.failed);
      }
    });
    if (/[?&]enviado=1/.test(location.search)) state('sent', MSG.sent);
  });
}

/* ------------------------------------------------------------ WhatsApp: muestra el globo un momento */
function whatsapp() {
  const wa = $('.wa');
  if (!wa) return;
  setTimeout(() => { wa.classList.add('show-tip'); setTimeout(() => wa.classList.remove('show-tip'), 6000); }, 3000);
}

/* ------------------------------------------------------------ catálogos (flipbook) bajo demanda */
function catalogs() {
  const books = $$('[data-flipbook]');
  if (!books.length) return;
  const load = () => {
    if (window.__fb) return;
    window.__fb = true;
    const s = document.createElement('script');
    s.src = books[0].dataset.loader;
    s.defer = true;
    document.body.appendChild(s);
  };
  if (!('IntersectionObserver' in window)) { load(); return; }
  const io = new IntersectionObserver((en) => { if (en.some((x) => x.isIntersecting)) { load(); io.disconnect(); } }, { rootMargin: '600px 0px' });
  books.forEach((b) => io.observe(b));
}

root.classList.remove('no-js');
stickyHeader();
lazyStuff();
overlays();
search();
strokes();
reveal();
wobble();
cursor();
counters();
tabs();
carousels();
justify();
lightbox();
forms();
whatsapp();
catalogs();
