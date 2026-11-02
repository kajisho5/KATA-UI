// KATA Meteors — seeds the sky: random starts, delays and speeds.
document.querySelectorAll('[data-meteors]').forEach(function (stage) {
  var N = 14;
  for (var i = 0; i < N; i++) {
    var m = document.createElement('span');
    m.className = 'k-meteor';
    m.setAttribute('aria-hidden', 'true');
    m.style.left = (25 + Math.random() * 85) + '%';
    m.style.top = (-8 + Math.random() * 45) + '%';
    m.style.animationDelay = (Math.random() * 9).toFixed(2) + 's';
    m.style.animationDuration = (3.2 + Math.random() * 3.6).toFixed(2) + 's';
    stage.appendChild(m);
  }
});
