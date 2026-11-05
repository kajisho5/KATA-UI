(function () {
'use strict';
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
  setTimeout(() => {
    el.setAttribute('data-closing', '');
    // Commit the visible state before starting the exit transition.
    void el.offsetWidth;
    el.style.opacity = '0';
    const style = getComputedStyle(el);
    const milliseconds = value => value.split(',').map(part => parseFloat(part) * (part.trim().endsWith('ms') ? 1 : 1000));
    const duration = Math.max(...milliseconds(style.transitionDuration));
    const delay = Math.max(...milliseconds(style.transitionDelay));
    if (duration === 0) { el.remove(); return; }
    const timer = setTimeout(() => el.remove(), duration + Math.max(0, delay) + 50);
    const finish = event => {
      if (event.target !== el || event.propertyName !== 'opacity') return;
      clearTimeout(timer);
      el.remove();
    };
    el.addEventListener('transitionend', finish);
    el.addEventListener('transitioncancel', finish);
  }, 4000);
}
document.querySelectorAll('[data-toast-demo]').forEach(btn => {
  if (btn.dataset.kataReady) return;
  btn.dataset.kataReady = 'true';
  btn.addEventListener('click', () => toast('Saved', 'Your draft is synced automatically.', btn));
});

})();
