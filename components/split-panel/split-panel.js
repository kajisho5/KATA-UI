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

  document.querySelectorAll('[data-split]').forEach(root => {
    if (root.dataset.kataReady) return;
    const pane = root.querySelector('.k-split-a');
    const handle = root.querySelector('[data-split-h]');
    if (!pane || !handle) return;
    root.dataset.kataReady = 'true';
    identify(root, 'kata-split'); identify(pane, 'kata-split-pane');
    handle.setAttribute('role', 'separator');
    if (!handle.hasAttribute('tabindex')) handle.tabIndex = 0;
    if (!handle.hasAttribute('aria-label')) handle.setAttribute('aria-label', 'Resize panes');
    handle.setAttribute('aria-controls', pane.id);
    // aria-orientation="horizontal" means a horizontal bar between stacked panes.
    const stacked = handle.getAttribute('aria-orientation') === 'horizontal';
    root.classList.toggle('k-split-v', stacked);
    const read = (name, fallback) => { const n = parseFloat(handle.getAttribute(name)); return Number.isFinite(n) ? n : fallback; };
    const min = read('aria-valuemin', 20), max = read('aria-valuemax', 80);
    handle.setAttribute('aria-valuemin', String(min)); handle.setAttribute('aria-valuemax', String(max));
    let value = read('aria-valuenow', 38);

    function set(next, notify) {
      const clamped = Math.max(min, Math.min(max, next));
      const changed = Math.round(clamped) !== Math.round(value);
      value = clamped;
      pane.style[stacked ? 'height' : 'width'] = value + '%';
      handle.setAttribute('aria-valuenow', String(Math.round(value)));
      if (notify && changed) root.dispatchEvent(new CustomEvent('kata-split-panel-change', { bubbles: true, detail: { value: Math.round(value) } }));
    }
    set(value, false);
    const rtl = () => getComputedStyle(root).direction === 'rtl';
    function fromPointer(event) {
      const box = root.getBoundingClientRect();
      if (stacked) return (event.clientY - box.top) / box.height * 100;
      return (rtl() ? box.right - event.clientX : event.clientX - box.left) / box.width * 100;
    }

    let start = null;
    handle.addEventListener('pointerdown', event => {
      if (event.button !== 0) return;
      event.preventDefault();
      start = value;
      handle.setPointerCapture(event.pointerId);
      handle.focus();
    });
    handle.addEventListener('pointermove', event => {
      if (start !== null && handle.hasPointerCapture(event.pointerId)) set(fromPointer(event), false);
    });
    // Capture ends on pointerup, pointercancel or loss; report one change per drag.
    handle.addEventListener('lostpointercapture', () => {
      if (start === null) return;
      const before = start; start = null;
      if (Math.round(before) !== Math.round(value)) root.dispatchEvent(new CustomEvent('kata-split-panel-change', { bubbles: true, detail: { value: Math.round(value) } }));
    });
    handle.addEventListener('keydown', event => {
      if (event.isComposing || event.keyCode === 229) return;
      const step = event.shiftKey ? 10 : 2;
      let next = null;
      if (stacked) {
        if (event.key === 'ArrowUp') next = value - step;
        else if (event.key === 'ArrowDown') next = value + step;
      } else if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
        // The handle moves in the arrow's visual direction; in RTL the first pane sits on the right.
        const toward = (event.key === 'ArrowRight') !== rtl() ? 1 : -1;
        next = value + toward * step;
      }
      if (event.key === 'Home') next = min;
      else if (event.key === 'End') next = max;
      if (next === null) return;
      event.preventDefault(); set(next, true);
    });
  });
})();
