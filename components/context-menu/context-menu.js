const ctxZone = document.querySelector('[data-ctx-zone]');
const ctxMenu = document.querySelector('[data-ctx]');
function ctxOpen(x, y) {
  ctxMenu.hidden = false;
  const r = ctxMenu.getBoundingClientRect();
  ctxMenu.style.left = Math.min(x, window.innerWidth - r.width - 10) + 'px';
  ctxMenu.style.top = Math.min(y, window.innerHeight - r.height - 10) + 'px';
  const first = ctxMenu.querySelector('button');
  if (first) first.focus();
}
function ctxClose() { ctxMenu.hidden = true; }
ctxZone.addEventListener('contextmenu', e => { e.preventDefault(); ctxOpen(e.clientX, e.clientY); });
ctxZone.addEventListener('keydown', e => {
  if (e.key === 'F10' && e.shiftKey || e.key === 'ContextMenu') {
    e.preventDefault();
    const r = ctxZone.getBoundingClientRect();
    ctxOpen(r.left + 24, r.top + 24);
  }
});
ctxMenu.querySelectorAll('button').forEach(b => b.addEventListener('click', ctxClose));
document.addEventListener('click', e => { if (!ctxMenu.contains(e.target)) ctxClose(); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') { ctxClose(); ctxZone.focus(); } });
window.addEventListener('blur', ctxClose);
