/* KATA Tour — KATATour.start([{el, title, text}, ...]); Skip and Escape always work. */
(function () {
  var card = null, ring = null, steps = [], idx = 0, target = null;
  function ensure() {
    if (card) return;
    ring = document.createElement('div');
    ring.className = 'k-tour-ring';
    ring.hidden = true;
    ring.style.position = 'fixed';
    ring.style.zIndex = '90';
    document.body.appendChild(ring);
    card = document.createElement('div');
    card.className = 'k-tour';
    card.hidden = true;
    card.style.position = 'fixed';
    card.style.zIndex = '91';
    card.setAttribute('role', 'dialog');
    card.setAttribute('aria-label', 'Product tour');
    card.innerHTML = '<span class="k-tour-arrow"></span><h4 data-t></h4><p data-x></p>' +
      '<div class="k-tour-ft"><span class="k-tour-dots" data-d></span>' +
      '<button type="button" class="btn btn-ghost btn-sm" data-skip>Skip</button>' +
      '<button type="button" class="btn btn-pri btn-sm" data-next>Next</button></div>';
    document.body.appendChild(card);
    card.querySelector('[data-skip]').addEventListener('click', end);
    card.querySelector('[data-next]').addEventListener('click', function () {
      idx++;
      if (idx >= steps.length) end(); else show();
    });
    document.addEventListener('keydown', function (e) {
      if (!card || card.hidden) return;
      if (e.key === 'Escape') end();
      if (e.key === 'ArrowRight') card.querySelector('[data-next]').click();
    });
    window.addEventListener('resize', place);
    window.addEventListener('scroll', place, true);
  }
  function place() {
    if (!target || card.hidden) return;
    var r = target.getBoundingClientRect();
    ring.style.left = (r.left - 5) + 'px';
    ring.style.top = (r.top - 5) + 'px';
    ring.style.width = (r.width + 10) + 'px';
    ring.style.height = (r.height + 10) + 'px';
    var cw = card.offsetWidth, ch = card.offsetHeight;
    var below = r.bottom + 14 + ch <= window.innerHeight - 10;
    card.classList.toggle('flip', !below);
    card.style.top = (below ? r.bottom + 14 : r.top - ch - 14) + 'px';
    card.style.left = Math.max(10, Math.min(r.left, window.innerWidth - cw - 10)) + 'px';
    var ax = r.left + r.width / 2 - card.offsetLeft - 6;
    card.querySelector('.k-tour-arrow').style.left = Math.max(14, Math.min(ax, cw - 26)) + 'px';
  }
  function show() {
    var s = steps[idx];
    target = document.querySelector(s.el);
    if (!target) { idx++; if (idx < steps.length) show(); else end(); return; }
    card.querySelector('[data-t]').textContent = s.title;
    card.querySelector('[data-x]').textContent = s.text;
    var dots = card.querySelector('[data-d]');
    dots.innerHTML = '';
    steps.forEach(function (_, i) {
      var d = document.createElement('i');
      if (i === idx) d.className = 'on';
      dots.appendChild(d);
    });
    card.querySelector('[data-next]').textContent = idx === steps.length - 1 ? 'Done' : 'Next';
    card.hidden = false;
    ring.hidden = false;
    place();
    card.querySelector('[data-next]').focus();
  }
  function end() {
    if (!card) return;
    card.hidden = true;
    ring.hidden = true;
  }
  window.KATATour = {
    start: function (s) { steps = s || []; idx = 0; ensure(); if (steps.length) show(); },
    end: end
  };
})();
