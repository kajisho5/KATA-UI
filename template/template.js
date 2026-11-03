// Optional initializer. Delete this file when the component needs no behavior.
(() => {
  document.querySelectorAll('[data-tpl]').forEach(root => {
    if (root.hasAttribute('data-kata-ready')) return;
    root.setAttribute('data-kata-ready', '');
    // Add behavior and its keyboard/IME/focus handling before describing it in meta.json.
  });
})();
