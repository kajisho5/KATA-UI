// KATA Text reveal — split into words, rise once when visible.
document.querySelectorAll('[data-reveal]').forEach(function (el) {
  var words = el.textContent.trim().split(/\s+/);
  el.textContent = '';
  words.forEach(function (w, i) {
    var outer = document.createElement('span');
    outer.className = 'k-rv-w';
    outer.setAttribute('aria-hidden', 'true');
    var inner = document.createElement('span');
    inner.className = 'k-rv-i';
    inner.style.setProperty('--i', i);
    inner.textContent = w;
    outer.appendChild(inner);
    el.appendChild(outer);
    el.appendChild(document.createTextNode(' '));
  });
  if (!('IntersectionObserver' in window) || window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    el.classList.add('in');
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    if (entries[0].isIntersecting) {
      el.classList.add('in');
      io.disconnect();
    }
  }, { threshold: 0.35 });
  io.observe(el);
});
