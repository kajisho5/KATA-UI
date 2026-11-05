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
  // Text goes in as text, never as markup. The check icon is decorative; the title says the outcome.
  el.innerHTML = '<svg class="toast-icon" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true" focusable="false"><path d="M4 12.5l5 5L20 6.5"/></svg><span><b></b></span>';
  el.querySelector('b').textContent = title;
  if (sub) { const small = document.createElement('small'); small.textContent = sub; el.querySelector('span').append(small); }
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
// Each stack is a polite status live region before any toast is added, so screen readers announce new toasts.
document.querySelectorAll('[data-toasts]').forEach(box => {
  if (!box.hasAttribute('role')) box.setAttribute('role', 'status');
  if (!box.hasAttribute('aria-live')) box.setAttribute('aria-live', 'polite');
});
document.querySelectorAll('[data-toast-demo]').forEach(btn => {
  if (btn.dataset.kataReady) return;
  btn.dataset.kataReady = 'true';
  btn.addEventListener('click', () => toast('Saved', 'Your draft is synced automatically.', btn));
});

})();
