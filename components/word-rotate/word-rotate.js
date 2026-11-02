// KATA Word Rotate — steps the stack; wraps without a visible rewind.
document.querySelectorAll('[data-wrot]').forEach(function (el) {
  var inner = el.querySelector('.k-wrot-in');
  var words = inner.children.length;
  if (words < 2) return;
  inner.appendChild(inner.children[0].cloneNode(true));
  var i = 0;
  setInterval(function () {
    i++;
    inner.style.transform = 'translateY(-' + (i * 1.26) + 'em)';
    if (i === words) {
      setTimeout(function () {
        inner.style.transition = 'none';
        inner.style.transform = 'translateY(0)';
        i = 0;
        requestAnimationFrame(function () { requestAnimationFrame(function () { inner.style.transition = ''; }); });
      }, 580);
    }
  }, 2100);
});
