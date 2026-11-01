const toasts = document.querySelector('[data-toasts]');
function toast(title, sub){
  const el = document.createElement('div');
  el.className = 'toast';
  el.innerHTML = '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="2.4" stroke-linecap="round" style="flex:none;margin-top:1px"><path d="M4 12.5l5 5L20 6.5"/></svg><span><b>' + title + '</b>' + (sub ? '<small>' + sub + '</small>' : '') + '</span>';
  toasts.appendChild(el);
  setTimeout(() => { el.style.transition = 'opacity .3s'; el.style.opacity = '0'; setTimeout(() => el.remove(), 320); }, 4000);
}
document.querySelector('[data-toast-demo]').addEventListener('click', () => toast('Saved', 'Your draft is synced automatically.'));
