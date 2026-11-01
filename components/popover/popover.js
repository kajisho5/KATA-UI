const wrap = document.querySelector('[data-popover]');
const popBtn = wrap.querySelector('[data-popover-btn]');
const popPanel = wrap.querySelector('[data-popover-panel]');
function setPop(open) {
  popPanel.classList.toggle('open', open);
  popBtn.setAttribute('aria-expanded', String(open));
}
popBtn.addEventListener('click', () => setPop(!popPanel.classList.contains('open')));
document.addEventListener('click', e => { if (!wrap.contains(e.target)) setPop(false); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') { setPop(false); popBtn.focus(); } });
