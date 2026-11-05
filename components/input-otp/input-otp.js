(() => {
  'use strict';
  let serial = 0;
  function identify(element, prefix) {
    if (!element.id) {
      let candidate;
      do { candidate = prefix + '-' + (++serial); } while (document.getElementById(candidate));
      element.id = candidate;
    }
    return element.id;
  }

  document.querySelectorAll('[data-otp]').forEach(root => {
    if (root.dataset.kataReady) return;
    const inputs = [...root.querySelectorAll('input')]; if (!inputs.length) return;
    root.dataset.kataReady = 'true'; root.dir = 'ltr'; identify(root, 'kata-otp');
    let composing = false, finishing = false, completed = '';
    function update() {
      const value = inputs.map(input => input.value).join(''); root.dataset.value = value;
      if (inputs.every(input => /^\d$/.test(input.value))) {
        if (completed !== value) { completed = value; root.dispatchEvent(new Event('change', { bubbles: true })); }
      } else completed = '';
    }
    function fill(index, value) {
      const digits = value.replace(/\D/g, '');
      if (!digits) { inputs[index].value = ''; update(); return; }
      const next = digits.slice(0, inputs.length - index);
      [...next].forEach((digit, offset) => { inputs[index + offset].value = digit; });
      inputs[Math.min(index + next.length, inputs.length - 1)].focus(); update();
    }
    inputs.forEach((input, index) => {
      identify(input, 'kata-otp-digit'); input.inputMode = 'numeric';
      if (!input.hasAttribute('aria-label') && !input.labels?.length) input.setAttribute('aria-label', 'Digit ' + (index + 1));
      input.autocomplete = index === 0 ? 'one-time-code' : 'off';
      input.addEventListener('input', event => { if (!composing && !finishing && !event.isComposing) fill(index, input.value); });
      input.addEventListener('keydown', event => {
        if (composing || finishing || event.isComposing || event.keyCode === 229) return;
        if (event.key === 'Backspace') { event.preventDefault(); input.value = ''; inputs[Math.max(0, index - 1)].focus(); update(); }
        if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
          event.preventDefault(); inputs[Math.max(0, Math.min(inputs.length - 1, index + (event.key === 'ArrowRight' ? 1 : -1)))].focus();
        }
        if (event.key === 'Enter') event.preventDefault();
      });
      input.addEventListener('paste', event => {
        if (composing || finishing) return;
        event.preventDefault(); fill(index, event.clipboardData?.getData('text') || '');
      });
    });
    root.addEventListener('compositionstart', () => { composing = true; });
    root.addEventListener('compositionend', event => {
      composing = false; finishing = true;
      const index = inputs.indexOf(event.target); if (index >= 0) fill(index, event.target.value);
      setTimeout(() => { finishing = false; }, 0);
    });
    root.dataset.value = inputs.map(input => input.value).join('');
  });
})();
