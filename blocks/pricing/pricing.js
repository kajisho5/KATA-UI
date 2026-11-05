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

  document.querySelectorAll('[data-billing]').forEach(toggle => {
    if (toggle.dataset.kataReady) return;
    // Each switch only rewrites the prices inside its own pricing section.
    const root = toggle.closest('.pricing') || toggle.closest('section') || toggle.parentElement;
    toggle.dataset.kataReady = 'true';
    identify(root, 'kata-pricing');
    if (!toggle.hasAttribute('aria-label') && !toggle.hasAttribute('aria-labelledby')) toggle.setAttribute('aria-label', 'Yearly billing');
    const status = document.createElement('span');
    status.className = 'pricing-status'; status.setAttribute('role', 'status');
    identify(status, 'kata-pricing-status'); root.append(status);
    function apply(announce) {
      root.querySelectorAll('[data-m]').forEach(amount => {
        amount.textContent = toggle.checked ? amount.dataset.y : amount.dataset.m;
      });
      if (announce) status.textContent = toggle.checked ? 'Showing yearly prices.' : 'Showing monthly prices.';
    }
    toggle.addEventListener('change', () => apply(true));
    // A restored checked state (back/forward cache, form restore) shows matching prices.
    if (toggle.checked) apply(false);
  });
})();
