// KATA Sidebar — collapsible groups. Everything else is plain links.
(function () {
  document.querySelectorAll('[data-side-toggle]').forEach(function (btn) {
    if (btn.hasAttribute('data-kata-ready')) return;
    btn.setAttribute('data-kata-ready', '');
    btn.addEventListener('click', function () {
      var group = btn.closest('.k-side-group');
      if (!group) return;
      var open = group.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });
})();
