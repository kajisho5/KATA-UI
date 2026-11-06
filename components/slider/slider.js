// KATA Slider — keep the filled track and the readout in sync.
(() => {
  document.querySelectorAll('[data-slider]').forEach(root => {
    if (root.hasAttribute('data-kata-ready')) return;
    const input = root.querySelector('input[type="range"]');
    const out = root.querySelector('[data-slider-val]');
    if (!input) return;
    root.setAttribute('data-kata-ready', '');
    function sync() {
      const min = parseFloat(input.min || 0);
      const max = parseFloat(input.max || 100);
      const pct = ((parseFloat(input.value) - min) / (max - min)) * 100;
      input.style.setProperty('--p', pct + '%');
      if (out) out.textContent = input.value;
    }
    input.addEventListener('input', sync);
    sync();
  });
})();
