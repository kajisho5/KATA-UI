// KATA Toggle — a button that keeps its own pressed state in aria-pressed.
(() => {
  document.querySelectorAll('.k-tgl').forEach(button => {
    // A second load must not bind a second listener: two would flip the state back on every click.
    if (button.hasAttribute('data-kata-ready')) return;
    button.setAttribute('data-kata-ready', '');
    button.addEventListener('click', () => {
      button.setAttribute('aria-pressed', String(button.getAttribute('aria-pressed') !== 'true'));
      button.dispatchEvent(new CustomEvent('kata-toggle-change', { bubbles: true, detail: { pressed: button.getAttribute('aria-pressed') === 'true' } }));
    });
  });
})();
