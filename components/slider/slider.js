// KATA Slider — keep the filled track and the readout in sync.
document.querySelectorAll('[data-slider]').forEach(function (root) {
  var input = root.querySelector('input[type="range"]');
  var out = root.querySelector('[data-slider-val]');
  if (!input) return;
  function sync() {
    var min = parseFloat(input.min || 0);
    var max = parseFloat(input.max || 100);
    var pct = ((parseFloat(input.value) - min) / (max - min)) * 100;
    input.style.setProperty('--p', pct + '%');
    if (out) out.textContent = input.value;
  }
  input.addEventListener('input', sync);
  sync();
});
