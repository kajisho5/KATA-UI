// KATA Sidebar — collapsible groups. Everything else is plain links.
document.querySelectorAll('[data-side-toggle]').forEach(function (btn) {
  btn.addEventListener('click', function () {
    var group = btn.closest('.k-side-group');
    if (!group) return;
    var open = group.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
});
