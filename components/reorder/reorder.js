const rankList = document.querySelector('[data-rank]');
const rankBtn = document.querySelector('[data-rank-btn]');
const rankReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
function rankSort() {
  const items = [...rankList.children];
  const first = new Map(items.map(li => [li, li.getBoundingClientRect().top]));
  items.forEach(li => { li.dataset.score = Math.max(40, Math.min(99, +li.dataset.score + Math.round((Math.random() - 0.5) * 36))); });
  items.sort((a, b) => +b.dataset.score - +a.dataset.score).forEach(li => rankList.appendChild(li));
  [...rankList.children].forEach((li, i) => {
    li.querySelector('.no').textContent = i + 1;
    li.querySelector('.val').textContent = li.dataset.score;
    const dy = first.get(li) - li.getBoundingClientRect().top;
    if (dy && !rankReduced) li.animate([{ transform: `translateY(${dy}px)` }, { transform: 'none' }], { duration: 560, easing: 'cubic-bezier(.3,.7,.3,1)' });
  });
}
rankBtn.addEventListener('click', rankSort);
let rankTimer = null;
if (!rankReduced) {
  rankTimer = setInterval(rankSort, 3000);
  rankList.closest('.k-glass').addEventListener('pointerenter', () => clearInterval(rankTimer));
  rankList.closest('.k-glass').addEventListener('pointerleave', () => { clearInterval(rankTimer); rankTimer = setInterval(rankSort, 3000); });
}
