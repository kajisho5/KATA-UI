// KATA Bounce Letters — splits the line; the click sends a wave.
document.querySelectorAll('[data-bounce]').forEach(function (el) {
  var text = el.textContent.trim();
  el.setAttribute('aria-label', text);
  el.textContent = '';
  var wrap = document.createElement('span');
  wrap.setAttribute('aria-hidden', 'true');
  text.split('').forEach(function (ch) {
    var s = document.createElement('span');
    s.className = 'ch';
    s.textContent = ch === ' ' ? ' ' : ch;
    wrap.appendChild(s);
  });
  el.appendChild(wrap);
  var letters = wrap.querySelectorAll('.ch');
  el.addEventListener('click', function () {
    letters.forEach(function (s, i) { s.style.transitionDelay = (i * 26) + 'ms'; });
    el.classList.add('waving');
    setTimeout(function () {
      el.classList.remove('waving');
      setTimeout(function () { letters.forEach(function (s) { s.style.transitionDelay = ''; }); }, 420);
    }, 340 + letters.length * 26);
  });
});
