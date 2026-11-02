// KATA Glow Cards — feeds each card the pointer's position.
document.querySelectorAll('.k-glow').forEach(function (card) {
  card.addEventListener('pointermove', function (e) {
    var r = card.getBoundingClientRect();
    card.style.setProperty('--mx', (e.clientX - r.left) + 'px');
    card.style.setProperty('--my', (e.clientY - r.top) + 'px');
  });
});
