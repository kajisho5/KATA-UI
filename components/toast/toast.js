function toastBox(near){
  const all = [...document.querySelectorAll('[data-toasts]')];
  if (!all.length) return null;
  if (!near) return all[0];
  return all.find(t => near.compareDocumentPosition(t) & Node.DOCUMENT_POSITION_FOLLOWING) || all[0];
}
function toast(title, sub, near){
  const toasts = toastBox(near);
  if (!toasts) return;
  const el = document.createElement('div');
  el.className = 'toast';
  el.innerHTML = '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#5dac81" stroke-width="2.4" stroke-linecap="round" style="flex:none;margin-top:1px"><path d="M4 12.5l5 5L20 6.5"/></svg><span><b>' + title + '</b>' + (sub ? '<small>' + sub + '</small>' : '') + '</span>';
  toasts.appendChild(el);
  setTimeout(() => { el.style.transition = 'opacity .3s'; el.style.opacity = '0'; setTimeout(() => el.remove(), 320); }, 4000);
}
document.querySelectorAll('[data-toast-demo]').forEach(btn => {
  btn.addEventListener('click', () => toast('Saved', 'Your draft is synced automatically.', btn));
});
