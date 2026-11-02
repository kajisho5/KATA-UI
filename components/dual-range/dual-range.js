// KATA Dual Range — keeps the gap, paints the fill, mirrors the numbers.
document.querySelectorAll('[data-dr]').forEach(function (root) {
  var lo = root.querySelector('[data-dr-lo]');
  var hi = root.querySelector('[data-dr-hi]');
  var fill = root.querySelector('.k-dr-fill');
  var outLo = root.querySelector('[data-dr-out-lo]');
  var outHi = root.querySelector('[data-dr-out-hi]');
  var GAP = Number(root.getAttribute('data-dr-gap') || 50);
  var min = Number(lo.min), max = Number(lo.max);
  var fmt = function (v) { return '$' + Number(v).toLocaleString('en-US'); };
  function paint() {
    var a = Number(lo.value), b = Number(hi.value);
    var pa = (a - min) / (max - min) * 100, pb = (b - min) / (max - min) * 100;
    fill.style.left = pa + '%';
    fill.style.width = (pb - pa) + '%';
    outLo.textContent = fmt(a);
    outHi.textContent = fmt(b);
    lo.setAttribute('aria-valuetext', fmt(a));
    hi.setAttribute('aria-valuetext', fmt(b));
  }
  lo.addEventListener('input', function () { if (Number(lo.value) > Number(hi.value) - GAP) lo.value = Number(hi.value) - GAP; paint(); });
  hi.addEventListener('input', function () { if (Number(hi.value) < Number(lo.value) + GAP) hi.value = Number(lo.value) + GAP; paint(); });
  paint();
});
