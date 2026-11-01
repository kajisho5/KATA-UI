const fz = document.querySelector('[data-follow]');
const fFrame = fz.querySelector('[data-frame]');
const fTag = fz.querySelector('[data-frame-tag]');
const fReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
let fTx = 0, fTy = 0, fX = 0, fY = 0, fMoved = false;
function fCenter() { fTx = fz.clientWidth / 2; fTy = fz.clientHeight / 2; }
function fPlace() {
  fFrame.style.left = fX + 'px'; fFrame.style.top = fY + 'px';
  fTag.style.left = fX + 'px'; fTag.style.top = fY + 'px';
}
fCenter(); fX = fTx; fY = fTy; fPlace();
fz.addEventListener('pointermove', e => {
  const r = fz.getBoundingClientRect();
  fMoved = true;
  fTx = Math.max(64, Math.min(r.width - 64, e.clientX - r.left));
  fTy = Math.max(48, Math.min(r.height - 48, e.clientY - r.top));
});
fz.addEventListener('pointerleave', () => { fMoved = false; fCenter(); });
window.addEventListener('resize', () => { if (!fMoved) { fCenter(); fX = fTx; fY = fTy; fPlace(); } });
if (!fReduced) {
  (function fLoop() {
    fX += (fTx - fX) * 0.16;
    fY += (fTy - fY) * 0.16;
    fPlace();
    requestAnimationFrame(fLoop);
  })();
}
