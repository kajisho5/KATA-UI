// KATA Time Picker — hours and five-minute steps; typing still works.
document.querySelectorAll('[data-tp]').forEach(function (el) {
  var input = el.querySelector('[data-tp-input]');
  var btn = el.querySelector('[data-tp-btn]');
  var panel = el.querySelector('[data-tp-panel]');
  var hCol = el.querySelector('[data-tp-h]');
  var mCol = el.querySelector('[data-tp-m]');
  function pad(n) { return String(n).padStart(2, '0'); }
  function build(col, values, cur) {
    col.querySelectorAll('.k-tp-opt').forEach(function (o) { o.remove(); });
    values.forEach(function (v) {
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'k-tp-opt' + (v === cur ? ' sel' : ''); b.textContent = v; b.setAttribute('data-v', v);
      col.appendChild(b);
    });
  }
  function render() {
    var m = /^(\d{1,2}):(\d{2})/.exec(input.value || '');
    build(hCol, Array.from({ length: 24 }, function (_, i) { return pad(i); }), m ? pad(+m[1]) : '');
    build(mCol, Array.from({ length: 12 }, function (_, i) { return pad(i * 5); }), m ? m[2] : '');
  }
  function open() { render(); panel.hidden = false; btn.setAttribute('aria-expanded', 'true'); }
  function close() { panel.hidden = true; btn.setAttribute('aria-expanded', 'false'); }
  btn.addEventListener('click', function () { panel.hidden ? open() : close(); });
  input.addEventListener('focus', open);
  panel.addEventListener('click', function (e) {
    var b = e.target.closest('.k-tp-opt'); if (!b) return;
    var m = /^(\d{1,2}):(\d{2})/.exec(input.value || '');
    var h = m ? pad(+m[1]) : '09', min = m ? m[2] : '00';
    if (b.parentElement === hCol) h = b.getAttribute('data-v'); else min = b.getAttribute('data-v');
    input.value = h + ':' + min;
    input.dispatchEvent(new Event('change', { bubbles: true }));
    render();
  });
  document.addEventListener('click', function (e) { if (!el.contains(e.target)) close(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
  render();
});
