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
  const headers = [];

  document.querySelectorAll('[data-hdr-btn]').forEach(button => {
    if (button.dataset.kataReady) return;
    const root = button.closest('.k-hdr') || button.parentElement;
    const panel = root.querySelector('[data-hdr-panel]');
    if (!panel) return;
    button.dataset.kataReady = 'true';
    identify(root, 'kata-hdr'); identify(panel, 'kata-hdr-panel');
    button.type = 'button';
    button.setAttribute('aria-controls', panel.id);
    function set(open, restore) {
      panel.classList.toggle('open', open);
      button.setAttribute('aria-expanded', String(open));
      if (!open && restore) button.focus();
    }
    set(panel.classList.contains('open'), false);
    button.addEventListener('click', () => set(button.getAttribute('aria-expanded') !== 'true', false));
    root.addEventListener('keydown', event => {
      if (event.key !== 'Escape' || event.isComposing || event.keyCode === 229) return;
      if (button.getAttribute('aria-expanded') !== 'true') return;
      event.preventDefault(); set(false, root.contains(document.activeElement));
    });
    // Following a link in the menu closes it.
    panel.addEventListener('click', event => { if (event.target.closest('a')) set(false, false); });
    headers.push({ root, button, set });
  });

  // One outside-dismissal listener for every header on the page, registered once.
  if (headers.length && !document.documentElement.dataset.kataHdrDismiss) {
    document.documentElement.dataset.kataHdrDismiss = 'true';
    document.addEventListener('pointerdown', event => {
      document.querySelectorAll('[data-hdr-btn][aria-expanded="true"]').forEach(button => {
        const root = button.closest('.k-hdr') || button.parentElement;
        if (root.contains(event.target)) return;
        const panel = root.querySelector('[data-hdr-panel]');
        if (panel) panel.classList.remove('open');
        button.setAttribute('aria-expanded', 'false');
      });
    });
  }
})();
