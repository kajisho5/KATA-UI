// KATA Comparison Slider — the seam is a range input wearing the picture.
document.querySelectorAll('[data-cmp]').forEach(function (el) {
  var range = el.querySelector('input[type=range]');
  function set() { el.style.setProperty('--pos', range.value + '%'); }
  range.addEventListener('input', set);
  set();
});
