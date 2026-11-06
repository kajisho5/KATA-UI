// KATA Hover Card — opens on hover (with delay) and on focus; Escape dismisses (WCAG 1.4.13).
(() => {
  'use strict';
  const instances = [];
  // Keep the centred card inside the viewport with a margin of one --k-space-4 on each side.
  function fit(wrap) {
    const card = wrap.querySelector('.card');
    if (!card) return;
    wrap.style.setProperty('--khover-shift', '0px');
    const margin = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--k-space-4')) || 16;
    const rect = card.getBoundingClientRect();
    const view = document.documentElement.clientWidth;
    let shift = 0;
    if (rect.left < margin) shift = margin - rect.left;
    else if (rect.right > view - margin) shift = view - margin - rect.right;
    wrap.style.setProperty('--khover-shift', `${Math.round(shift)}px`);
  }
  document.querySelectorAll('[data-hover]').forEach(wrap => {
    if (wrap.hasAttribute('data-kata-ready')) return;
    wrap.setAttribute('data-kata-ready', '');
    let openT, closeT;
    const show = () => { clearTimeout(closeT); fit(wrap); wrap.classList.add('open'); };
    const hide = () => { clearTimeout(openT); clearTimeout(closeT); wrap.classList.remove('open'); };
    wrap.addEventListener('pointerenter', () => { clearTimeout(closeT); openT = setTimeout(show, 300); });
    wrap.addEventListener('pointerleave', () => { clearTimeout(openT); closeT = setTimeout(hide, 180); });
    wrap.addEventListener('focusin', show);
    wrap.addEventListener('focusout', event => { if (!wrap.contains(event.relatedTarget)) { clearTimeout(openT); closeT = setTimeout(hide, 180); } });
    instances.push({ wrap, hide });
  });
  // One shared Escape listener per script load; a second load finds no new card and adds none.
  if (!instances.length) return;
  document.addEventListener('keydown', event => {
    if (event.key !== 'Escape' || event.isComposing || event.keyCode === 229) return;
    instances.forEach(({ wrap, hide }) => { if (wrap.classList.contains('open')) hide(); });
  });
})();
