document.querySelectorAll('[data-hover]').forEach(wrap => {
  let openT, closeT;
  const open = () => { clearTimeout(closeT); openT = setTimeout(() => wrap.classList.add('open'), 300); };
  const close = () => { clearTimeout(openT); closeT = setTimeout(() => wrap.classList.remove('open'), 180); };
  wrap.addEventListener('pointerenter', open);
  wrap.addEventListener('pointerleave', close);
  wrap.addEventListener('focusin', () => { clearTimeout(closeT); wrap.classList.add('open'); });
  wrap.addEventListener('focusout', close);
});
