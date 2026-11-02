// KATA Hanko — stamps on arrival; click presses it again.
document.querySelectorAll('[data-seal]').forEach(function (seal) {
  function stamp() {
    seal.classList.remove('stamp');
    void seal.offsetWidth;
    seal.classList.add('stamp');
  }
  seal.addEventListener('click', stamp);
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { setTimeout(stamp, 300); io.disconnect(); } }, { threshold: .5 });
    io.observe(seal);
  } else { stamp(); }
});
