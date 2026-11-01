const cp = document.querySelector('[data-cp]');
const cpOut = cp.querySelector('[data-cp-hex]');
const cpChip = cp.querySelector('[data-cp-chip]');
function cpHex(rgb) {
  const m = rgb.match(/\d+/g).map(Number);
  return '#' + m.slice(0, 3).map(n => n.toString(16).padStart(2, '0')).join('').toUpperCase();
}
function cpSelect(el, color) {
  cp.querySelectorAll('.k-cp-sw').forEach(s => { s.classList.remove('sel'); s.setAttribute('aria-checked', 'false'); s.innerHTML = ''; });
  if (el) { el.classList.add('sel'); el.setAttribute('aria-checked', 'true'); el.innerHTML = cp.dataset.check; }
  cpOut.textContent = color;
  cpChip.style.background = color;
}
cp.querySelectorAll('.k-cp-sw').forEach(sw => {
  sw.addEventListener('click', () => cpSelect(sw, cpHex(getComputedStyle(sw).backgroundColor)));
});
const cpCustom = cp.querySelector('[data-cp-custom]');
cpCustom.addEventListener('input', e => cpSelect(null, e.target.value.toUpperCase()));
const cpFirst = cp.querySelector('.k-cp-sw.sel');
if (cpFirst) cpSelect(cpFirst, cpHex(getComputedStyle(cpFirst).backgroundColor));
