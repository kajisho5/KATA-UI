const fz = document.querySelector('[data-follow]');
const fFrame = fz.querySelector('[data-frame]');
const fTag = fz.querySelector('[data-frame-tag]');
let fTx = fz.clientWidth / 2, fTy = fz.clientHeight / 2, fX = fTx, fY = fTy;
const fReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
function fPlace() {
  fFrame.style.transform = `translate(${fX}px,${fY}px) translate(-50%,-50%)`;
  fTag.style.transform = `translate(${fX}px,${fY}px) translate(-50%,-168%)`;
}
fPlace();
fz.addEventListener('pointermove', e => {
  const r = fz.getBoundingClientRect();
  fTx = Math.max(64, Math.min(r.width - 64, e.clientX - r.left));
  fTy = Math.max(48, Math.min(r.height - 48, e.clientY - r.top));
});
fz.addEventListener('pointerleave', () => { fTx = fz.clientWidth / 2; fTy = fz.clientHeight / 2; });
if (!fReduced) {
  (function fLoop() {
    fX += (fTx - fX) * 0.16;
    fY += (fTy - fY) * 0.16;
    fPlace();
    requestAnimationFrame(fLoop);
  })();
}
