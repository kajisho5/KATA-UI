const carTrack = document.querySelector('[data-car-track]');
const carSlides = [...carTrack.children];
const carDots = [...document.querySelectorAll('[data-car-dot]')];
function carGo(i) {
  carTrack.scrollTo({ left: carSlides[i].offsetLeft - carTrack.offsetLeft, behavior: 'smooth' });
}
function carIndex() {
  const x = carTrack.scrollLeft + 8;
  let best = 0;
  carSlides.forEach((s, i) => { if (s.offsetLeft - carTrack.offsetLeft <= x) best = i; });
  return best;
}
document.querySelector('[data-car-prev]').addEventListener('click', () => carGo(Math.max(0, carIndex() - 1)));
document.querySelector('[data-car-next]').addEventListener('click', () => carGo(Math.min(carSlides.length - 1, carIndex() + 1)));
carDots.forEach((d, i) => d.addEventListener('click', () => carGo(i)));
carTrack.addEventListener('scroll', () => {
  const i = carIndex();
  carDots.forEach((d, j) => d.setAttribute('aria-current', j === i ? 'true' : 'false'));
}, { passive: true });
