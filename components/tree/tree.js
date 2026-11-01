document.querySelectorAll('.k-tree .tg').forEach(btn => {
  btn.addEventListener('click', () => {
    const open = btn.getAttribute('aria-expanded') === 'true';
    btn.setAttribute('aria-expanded', String(!open));
    const ul = btn.closest('li').querySelector(':scope > ul');
    if (ul) ul.hidden = open;
  });
});
