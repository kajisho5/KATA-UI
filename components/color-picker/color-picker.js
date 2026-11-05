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
  function hex(rgb) {
    const parts = (rgb.match(/[\d.]+/g) || []).slice(0, 3).map(Number);
    if (parts.length < 3) return rgb;
    return '#' + parts.map(n => Math.round(n).toString(16).padStart(2, '0')).join('').toUpperCase();
  }

  document.querySelectorAll('[data-cp]').forEach(root => {
    if (root.dataset.kataReady) return;
    const swatches = [...root.querySelectorAll('.k-cp-sw')];
    const out = root.querySelector('[data-cp-hex]');
    const chip = root.querySelector('[data-cp-chip]');
    const custom = root.querySelector('[data-cp-custom]');
    if (!swatches.length) return;
    root.dataset.kataReady = 'true';
    identify(root, 'kata-cp');
    swatches.forEach(swatch => { swatch.type = 'button'; swatch.setAttribute('role', 'radio'); identify(swatch, 'kata-cp-swatch'); });
    if (custom) identify(custom, 'kata-cp-custom');

    // Roving tabindex: the checked swatch (or the first one) is the group's single tab stop.
    function rove() {
      const checked = swatches.find(swatch => swatch.getAttribute('aria-checked') === 'true') || swatches[0];
      swatches.forEach(swatch => { swatch.tabIndex = swatch === checked ? 0 : -1; });
    }
    function select(swatch, color, notify) {
      swatches.forEach(item => {
        const on = item === swatch;
        item.classList.toggle('sel', on); item.setAttribute('aria-checked', on ? 'true' : 'false');
        // The check mark is application-owned markup from data-check.
        item.innerHTML = on ? (root.dataset.check || '') : '';
      });
      rove();
      if (out) out.textContent = color;
      if (chip) chip.style.background = color;
      root.dataset.value = color;
      if (notify) root.dispatchEvent(new CustomEvent('kata-color-picker-change', { bubbles: true, detail: { value: color, name: swatch ? swatch.getAttribute('aria-label') : 'Custom' } }));
    }
    const colorOf = swatch => hex(getComputedStyle(swatch).backgroundColor);

    root.addEventListener('click', event => {
      const swatch = event.target.closest('.k-cp-sw');
      if (swatch && swatches.includes(swatch) && swatch.getAttribute('aria-checked') !== 'true') select(swatch, colorOf(swatch), true);
    });
    root.addEventListener('keydown', event => {
      const swatch = event.target.closest('.k-cp-sw');
      if (!swatch || !swatches.includes(swatch) || event.isComposing || event.keyCode === 229) return;
      const index = swatches.indexOf(swatch), last = swatches.length - 1;
      const rtl = getComputedStyle(root).direction === 'rtl';
      let next = null;
      if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
        // Horizontal arrows follow the visual direction; in RTL, Left moves forward.
        const forward = (event.key === 'ArrowRight') !== rtl;
        next = forward ? (index === last ? 0 : index + 1) : (index === 0 ? last : index - 1);
      } else if (event.key === 'ArrowDown') next = index === last ? 0 : index + 1;
      else if (event.key === 'ArrowUp') next = index === 0 ? last : index - 1;
      else if (event.key === 'Home') next = 0;
      else if (event.key === 'End') next = last;
      if (next === null) return;
      event.preventDefault();
      select(swatches[next], colorOf(swatches[next]), true);
      swatches[next].focus();
    });
    if (custom) {
      // Live preview while the native picker moves; one notification when it commits.
      custom.addEventListener('input', () => select(null, custom.value.toUpperCase(), false));
      custom.addEventListener('change', () => select(null, custom.value.toUpperCase(), true));
    }

    const first = swatches.find(swatch => swatch.getAttribute('aria-checked') === 'true');
    if (first) select(first, colorOf(first), false); else rove();
  });
})();
