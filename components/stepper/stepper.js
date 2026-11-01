// KATA Stepper — bounded increment control.
document.querySelectorAll('[data-stepper]').forEach(function (root) {
  var out = root.querySelector('[data-step-val]');
  var min = parseFloat(root.dataset.min || '-Infinity');
  var max = parseFloat(root.dataset.max || 'Infinity');
  var step = parseFloat(root.dataset.step || '1');
  function render() {
    var v = parseFloat(out.textContent) || 0;
    root.querySelectorAll('[data-step-btn]').forEach(function (b) {
      var d = parseFloat(b.dataset.stepBtn);
      b.disabled = (d < 0 && v <= min) || (d > 0 && v >= max);
    });
  }
  root.querySelectorAll('[data-step-btn]').forEach(function (b) {
    b.addEventListener('click', function () {
      var v = parseFloat(out.textContent) || 0;
      v = Math.min(max, Math.max(min, v + parseFloat(b.dataset.stepBtn) * step));
      out.textContent = String(v);
      render();
    });
  });
  render();
});
