const split = document.querySelector('[data-split]');
const splitA = split.querySelector('.k-split-a');
const splitH = split.querySelector('[data-split-h]');
let splitPct = 38;
function splitSet(p) {
  splitPct = Math.max(20, Math.min(80, p));
  splitA.style.width = splitPct + '%';
  splitH.setAttribute('aria-valuenow', String(Math.round(splitPct)));
}
splitSet(splitPct);
splitH.addEventListener('pointerdown', e => {
  e.preventDefault();
  splitH.setPointerCapture(e.pointerId);
  const move = ev => {
    const r = split.getBoundingClientRect();
    splitSet((ev.clientX - r.left) / r.width * 100);
  };
  const up = () => {
    splitH.removeEventListener('pointermove', move);
    splitH.removeEventListener('pointerup', up);
  };
  splitH.addEventListener('pointermove', move);
  splitH.addEventListener('pointerup', up);
});
splitH.addEventListener('keydown', e => {
  const step = e.shiftKey ? 10 : 2;
  if (e.key === 'ArrowLeft') { e.preventDefault(); splitSet(splitPct - step); }
  if (e.key === 'ArrowRight') { e.preventDefault(); splitSet(splitPct + step); }
});
