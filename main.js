(function () {
  var nav = document.querySelector('.nav');
  var toggle = document.querySelector('.nav-toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });
    nav.querySelectorAll('.nav-links a').forEach(function (a) {
      a.addEventListener('click', function () { nav.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); });
    });
  }

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var items = document.querySelectorAll('.reveal');
  if (items.length && !reduce && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('in'); });
  }

  var form = document.querySelector('form.apply');
  if (form) {
    var next = form.querySelector('input[name="_next"]');
    if (next) next.value = window.location.origin + '/apply?sent=1';
    var params = new URLSearchParams(window.location.search);
    var sent = document.getElementById('sent');
    if (params.get('sent') === '1' && sent) {
      sent.hidden = false;
      form.hidden = true;
      sent.scrollIntoView({ block: 'center' });
    }
    form.addEventListener('submit', function (ev) {
      var bad = false;
      form.querySelectorAll('.field').forEach(function (f) {
        var input = f.querySelector('input, select, textarea');
        if (!input) return;
        var ok = input.checkValidity();
        f.classList.toggle('invalid', !ok);
        if (!ok && !bad) { bad = true; input.focus(); }
      });
      if (bad) { ev.preventDefault(); return; }
      var btn = form.querySelector('button[type="submit"]');
      if (btn) { btn.disabled = true; btn.textContent = 'Sending your application'; }
    });
  }
})();
