document.querySelectorAll('[data-dd-trigger]').forEach(btn => {
  const menu = btn.parentElement.querySelector('[data-dd-menu]');
  btn.addEventListener('click', e => { e.stopPropagation(); menu.classList.toggle('open'); });
  document.addEventListener('click', () => menu.classList.remove('open'));
  document.addEventListener('keydown', e => { if (e.key === 'Escape') menu.classList.remove('open'); });
});
