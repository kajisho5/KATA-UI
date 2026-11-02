// KATA Sparkles — scatters the specks; each twinkles on its own clock.
document.querySelectorAll('[data-sparkles]').forEach(function (stage) {
  var N = 26;
  for (var i = 0; i < N; i++) {
    var s = document.createElement('span');
    s.className = 'k-spk-i';
    s.setAttribute('aria-hidden', 'true');
    var size = 2 + Math.random() * 3.4;
    s.style.width = size.toFixed(1) + 'px';
    s.style.height = size.toFixed(1) + 'px';
    s.style.left = (Math.random() * 98) + '%';
    s.style.top = (Math.random() * 92) + '%';
    s.style.animationDuration = (1.5 + Math.random() * 2.2).toFixed(2) + 's';
    s.style.animationDelay = (-Math.random() * 3).toFixed(2) + 's';
    stage.appendChild(s);
  }
});
