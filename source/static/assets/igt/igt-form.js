/*!
 * Integral Gym Tech – envío del formulario de contacto (reemplaza a Contact Form 7).
 * Conserva las clases de CF7 para que el diseño sea idéntico al original.
 */
(function () {
  'use strict';

  var MSG = {
    required: 'Por favor, completa este campo.',
    email: 'Ingresa un correo electrónico válido.',
    tel: 'Ingresa un número de teléfono válido.',
    invalid: 'Uno o más campos tienen un error. Por favor, revísalos e inténtalo de nuevo.',
    sent: '¡Gracias por tu mensaje! Un asesor de Integral Gym Tech te contactará muy pronto.',
    failed: 'Hubo un error al enviar tu mensaje. Inténtalo de nuevo o escríbenos por WhatsApp al 442 127 0018.',
    sending: 'Enviando…'
  };

  function setStatus(form, status) {
    ['init', 'submitting', 'sent', 'invalid', 'failed', 'spam'].forEach(function (s) {
      form.classList.remove(s);
    });
    form.classList.add(status);
    form.setAttribute('data-status', status);
  }

  function clearTips(form) {
    form.querySelectorAll('.wpcf7-not-valid-tip').forEach(function (t) { t.remove(); });
    form.querySelectorAll('.wpcf7-not-valid').forEach(function (c) {
      c.classList.remove('wpcf7-not-valid');
      c.setAttribute('aria-invalid', 'false');
    });
  }

  function tip(control, text) {
    control.classList.add('wpcf7-not-valid');
    control.setAttribute('aria-invalid', 'true');
    var span = document.createElement('span');
    span.className = 'wpcf7-not-valid-tip';
    span.setAttribute('aria-hidden', 'true');
    span.textContent = text;
    control.parentNode.appendChild(span);
  }

  function validate(form) {
    var ok = true;
    form.querySelectorAll('.wpcf7-form-control').forEach(function (c) {
      var v = (c.value || '').trim();
      if (c.classList.contains('wpcf7-validates-as-required') && !v) { tip(c, MSG.required); ok = false; return; }
      if (v && c.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) { tip(c, MSG.email); ok = false; return; }
      if (v && c.type === 'tel' && v.replace(/\D/g, '').length < 8) { tip(c, MSG.tel); ok = false; }
    });
    return ok;
  }

  function output(form, text) {
    var out = form.querySelector('.wpcf7-response-output');
    if (out) { out.textContent = text; out.setAttribute('aria-hidden', 'false'); }
  }

  function init(form) {
    var ts = form.querySelector('input[name="ts"]');
    if (ts) ts.value = String(Date.now());
    form.setAttribute('novalidate', 'novalidate');

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      clearTips(form);
      if (!validate(form)) {
        setStatus(form, 'invalid');
        output(form, MSG.invalid);
        return;
      }
      var btn = form.querySelector('button[type="submit"]');
      setStatus(form, 'submitting');
      if (btn) btn.disabled = true;

      var data = new FormData(form);
      data.append('ajax', '1');
      fetch(form.getAttribute('action'), { method: 'POST', body: data, headers: { 'Accept': 'application/json' } })
        .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
        .then(function (res) {
          if (res && res.ok) {
            setStatus(form, 'sent');
            output(form, MSG.sent);
            form.reset();
            if (ts) ts.value = String(Date.now());
            if (window.dataLayer) window.dataLayer.push({ event: 'generate_lead', form: 'contacto' });
            if (typeof window.gtag === 'function') window.gtag('event', 'generate_lead');
            if (typeof window.fbq === 'function') window.fbq('track', 'Lead');
          } else if (res && res.errors) {
            Object.keys(res.errors).forEach(function (name) {
              var c = form.querySelector('[name="' + name + '"]');
              if (c) tip(c, res.errors[name]);
            });
            setStatus(form, 'invalid');
            output(form, MSG.invalid);
          } else {
            setStatus(form, 'failed');
            output(form, (res && res.message) || MSG.failed);
          }
        })
        .catch(function () {
          setStatus(form, 'failed');
          output(form, MSG.failed);
        })
        .then(function () { if (btn) btn.disabled = false; });
    });
  }

  function ready() {
    document.querySelectorAll('form.igt-form').forEach(init);
    // Mensaje tras envío sin JavaScript (?enviado=1)
    if (/[?&]enviado=1/.test(location.search)) {
      var f = document.querySelector('form.igt-form');
      if (f) { setStatus(f, 'sent'); output(f, MSG.sent); }
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', ready);
  else ready();
})();
