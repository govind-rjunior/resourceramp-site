(function () {
  var doc = document.documentElement;
  doc.classList.add('js');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Navigation */
  var nav = document.querySelector('.nav');
  var toggle = document.querySelector('.nav-toggle');
  function closeMenu() {
    if (!nav || !nav.classList.contains('open')) return;
    nav.classList.remove('open');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Open menu');
  }
  if (nav && toggle) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });
    nav.querySelectorAll('.nav-links a').forEach(function (a) { a.addEventListener('click', closeMenu); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { closeMenu(); } });
    document.addEventListener('click', function (e) { if (!nav.contains(e.target)) closeMenu(); });
    window.matchMedia('(min-width: 1081px)').addEventListener('change', closeMenu);
  }

  /* Section reveal */
  var items = document.querySelectorAll('.reveal');
  if (items.length && !reduce && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('in'); });
  }

  /* FAQ: one answer open at a time where the name attribute is not supported */
  var faqs = document.querySelectorAll('.faq details');
  faqs.forEach(function (d) {
    d.addEventListener('toggle', function () {
      if (!d.open) return;
      faqs.forEach(function (o) { if (o !== d && o.open) o.open = false; });
    });
  });

  /* Lightbox */
  var lb = document.getElementById('lightbox');
  var zooms = Array.prototype.slice.call(document.querySelectorAll('[data-zoom]'));
  if (lb && zooms.length && typeof lb.showModal === 'function') {
    var lbImg = lb.querySelector('img');
    var lbCap = lb.querySelector('figcaption');
    var group = [], index = 0, opener = null;
    function show(i) {
      index = (i + group.length) % group.length;
      var el = group[index];
      var fig = el.closest('figure');
      var thumb = fig ? fig.querySelector('img') : null;
      var cap = fig ? fig.querySelector('figcaption') : null;
      lbImg.src = el.getAttribute('data-zoom');
      lbImg.alt = thumb ? thumb.alt : '';
      lbCap.textContent = cap ? cap.textContent : '';
      var many = group.length > 1;
      lb.querySelectorAll('.lb-nav').forEach(function (b) { b.hidden = !many; });
    }
    zooms.forEach(function (el) {
      el.addEventListener('click', function () {
        var scope = el.closest('.gallery') || document;
        group = Array.prototype.slice.call(scope.querySelectorAll('[data-zoom]'));
        opener = el;
        show(group.indexOf(el));
        lb.showModal();
      });
    });
    lb.querySelector('.lb-close').addEventListener('click', function () { lb.close(); });
    lb.querySelector('.lb-prev').addEventListener('click', function () { show(index - 1); });
    lb.querySelector('.lb-next').addEventListener('click', function () { show(index + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) lb.close(); });
    lb.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') show(index - 1);
      if (e.key === 'ArrowRight') show(index + 1);
    });
    lb.addEventListener('close', function () { if (opener) opener.focus(); });
  } else {
    zooms.forEach(function (el) { el.hidden = true; });
  }

  /* Reels: the still becomes the player in place, nothing loads until asked */
  document.querySelectorAll('[data-reel]').forEach(function (frame) {
    var btn = frame.querySelector('.reel-play');
    if (!btn) return;
    btn.addEventListener('click', function () {
      var kind = frame.getAttribute('data-reel');
      var src = frame.getAttribute('data-src');
      var player;
      if (kind === 'video') {
        document.querySelectorAll('.reel-frame video').forEach(function (v) { v.pause(); });
        player = document.createElement('video');
        player.src = src;
        player.controls = true;
        player.autoplay = true;
        player.playsInline = true;
        player.preload = 'auto';
        if (frame.getAttribute('data-poster')) player.poster = frame.getAttribute('data-poster');
      } else {
        player = document.createElement('iframe');
        player.src = src;
        player.title = btn.getAttribute('aria-label') || 'Video';
        player.allow = 'autoplay; fullscreen; encrypted-media';
        player.allowFullscreen = true;
        frame.style.aspectRatio = '4 / 5';
        frame.style.background = '#fff';
      }
      frame.querySelectorAll('img, .reel-play, .reel-len').forEach(function (n) { n.remove(); });
      frame.appendChild(player);
      player.focus && player.focus();
    });
  });

  /* Application form */
  var form = document.querySelector('form.apply');
  if (form) {
    var sent = document.getElementById('sent');
    var failed = document.getElementById('failed');
    var mailLink = document.getElementById('mail-fallback');
    var copyBtn = document.getElementById('copy-fallback');
    var btn = form.querySelector('button[type="submit"]');
    var btnLabel = btn ? btn.textContent : '';
    var next = form.querySelector('input[name="_next"]');
    if (next) next.value = window.location.origin + '/apply?sent=1';

    function showSent() {
      if (failed) failed.hidden = true;
      sent.hidden = false;
      form.hidden = true;
      sent.scrollIntoView({ block: 'center', behavior: reduce ? 'auto' : 'smooth' });
      sent.focus({ preventScroll: true });
    }
    if (new URLSearchParams(window.location.search).get('sent') === '1' && sent) showSent();

    function answers() {
      var lines = [];
      form.querySelectorAll('input, select, textarea').forEach(function (el) {
        if (!el.name || el.name.charAt(0) === '_' || el.type === 'hidden') return;
        if (el.type === 'checkbox') { if (el.checked) lines.push(el.name + ': yes'); return; }
        if (el.value.trim()) lines.push(el.name + ': ' + el.value.trim());
      });
      return lines.join('\n\n');
    }
    function showFailed() {
      var body = answers();
      var short = body.length > 1500 ? body.slice(0, 1500) + '\n\n[Answers cut short here. Use "Copy the answers" on the page and paste the rest.]' : body;
      if (mailLink) mailLink.href = 'mailto:ramp@resource.bz?subject=' + encodeURIComponent('Cohort 1 application') + '&body=' + encodeURIComponent(short);
      failed.hidden = false;
      failed.scrollIntoView({ block: 'center', behavior: reduce ? 'auto' : 'smooth' });
      failed.focus({ preventScroll: true });
      if (btn) { btn.disabled = false; btn.textContent = 'Try sending again'; }
    }
    if (copyBtn) {
      copyBtn.addEventListener('click', function () {
        var text = answers();
        var done = function () { copyBtn.textContent = 'Copied'; setTimeout(function () { copyBtn.textContent = 'Copy the answers'; }, 2400); };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(done, function () { copyBtn.textContent = 'Could not copy. Select the text in the form.'; });
        } else {
          var ta = document.createElement('textarea');
          ta.value = text; document.body.appendChild(ta); ta.select();
          try { document.execCommand('copy'); done(); } catch (err) { copyBtn.textContent = 'Could not copy. Select the text in the form.'; }
          ta.remove();
        }
      });
    }

    form.querySelectorAll('.field input, .field select, .field textarea').forEach(function (input) {
      var clear = function () {
        var f = input.closest('.field');
        if (f && f.classList.contains('invalid') && input.checkValidity()) f.classList.remove('invalid');
      };
      input.addEventListener('input', clear);
      input.addEventListener('change', clear);
    });

    form.addEventListener('submit', function (ev) {
      var bad = null;
      form.querySelectorAll('.field').forEach(function (f) {
        var input = f.querySelector('input, select, textarea');
        if (!input) return;
        var ok = input.checkValidity();
        f.classList.toggle('invalid', !ok);
        input.setAttribute('aria-invalid', ok ? 'false' : 'true');
        if (!ok && !bad) bad = input;
      });
      if (bad) { ev.preventDefault(); bad.focus(); return; }

      var honey = form.querySelector('input[name="_honey"]');
      if (honey && honey.value) { ev.preventDefault(); showSent(); return; }
      if (!window.fetch || !window.FormData) return; /* plain POST fallback */

      ev.preventDefault();
      if (failed) failed.hidden = true;
      if (btn) { btn.disabled = true; btn.textContent = 'Sending the application'; }
      var endpoint = form.getAttribute('action').replace('formsubmit.co/', 'formsubmit.co/ajax/');
      var data = new FormData(form);
      data.delete('_next');
      var timer = setTimeout(function () { controller && controller.abort(); }, 20000);
      var controller = 'AbortController' in window ? new AbortController() : null;
      fetch(endpoint, { method: 'POST', headers: { 'Accept': 'application/json' }, body: data, signal: controller ? controller.signal : undefined })
        .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, body: j }; }); })
        .then(function (res) {
          clearTimeout(timer);
          var success = res.ok && res.body && String(res.body.success) === 'true';
          if (success) { if (btn) btn.textContent = btnLabel; showSent(); }
          else showFailed();
        })
        .catch(function () { clearTimeout(timer); showFailed(); });
    });
  }
})();
