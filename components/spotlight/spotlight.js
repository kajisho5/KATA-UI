// KATA Spotlight — the beam follows the pointer; the lit layer is a clone
// the script makes, so the author writes the words once.
document.querySelectorAll('[data-spot]').forEach(function (el) {
  var inner = el.querySelector('.k-spot-in');
  if (inner) {
    var lit = document.createElement('div');
    lit.className = 'k-spot-lit';
    lit.setAttribute('aria-hidden', 'true');
    var clone = inner.cloneNode(true);
    clone.querySelectorAll('[id]').forEach(function (n) { n.removeAttribute('id'); });
    clone.querySelectorAll('a, button, input, select, textarea, [tabindex]').forEach(function (n) { n.setAttribute('tabindex', '-1'); });
    lit.appendChild(clone);
    el.appendChild(lit);
  }
  el.addEventListener('pointermove', function (e) {
    var r = el.getBoundingClientRect();
    el.style.setProperty('--mx', ((e.clientX - r.left) / r.width) * 100 + '%');
    el.style.setProperty('--my', ((e.clientY - r.top) / r.height) * 100 + '%');
  });
});
