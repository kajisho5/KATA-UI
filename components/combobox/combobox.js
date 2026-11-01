const combo = document.querySelector('[data-combo]');
const comboInput = combo.querySelector('[data-combo-input]');
const comboList = combo.querySelector('[data-combo-list]');
const comboItems = [...comboList.querySelectorAll('[data-val]')];
let comboActive = -1;
function comboOpen() {
  comboList.hidden = false;
  comboInput.setAttribute('aria-expanded', 'true');
}
function comboClose() {
  comboList.hidden = true;
  comboInput.setAttribute('aria-expanded', 'false');
  comboActive = -1;
  comboItems.forEach(li => li.classList.remove('act'));
}
function comboFilter() {
  const q = comboInput.value.trim().toLowerCase();
  let visible = 0;
  comboItems.forEach(li => {
    const hit = li.dataset.val.toLowerCase().includes(q);
    li.style.display = hit ? '' : 'none';
    if (hit) visible++;
  });
  comboList.querySelector('.none').style.display = visible ? 'none' : '';
}
function comboSetActive(i) {
  const vis = comboItems.filter(li => li.style.display !== 'none');
  if (!vis.length) return;
  comboActive = (i + vis.length) % vis.length;
  comboItems.forEach(li => li.classList.remove('act'));
  vis[comboActive].classList.add('act');
  comboInput.setAttribute('aria-activedescendant', vis[comboActive].id);
  vis[comboActive].scrollIntoView({ block: 'nearest' });
}
function comboPick(li) {
  comboInput.value = li.dataset.val;
  comboItems.forEach(x => x.setAttribute('aria-selected', x === li ? 'true' : 'false'));
  comboClose();
}
comboInput.addEventListener('focus', () => { comboFilter(); comboOpen(); });
comboInput.addEventListener('input', () => { comboFilter(); comboOpen(); });
comboInput.addEventListener('keydown', e => {
  if (e.key === 'ArrowDown') { e.preventDefault(); if (comboList.hidden) comboOpen(); comboSetActive(comboActive + 1); }
  if (e.key === 'ArrowUp') { e.preventDefault(); comboSetActive(comboActive - 1); }
  if (e.key === 'Enter') {
    const vis = comboItems.filter(li => li.style.display !== 'none');
    if (!comboList.hidden && vis[comboActive]) { e.preventDefault(); comboPick(vis[comboActive]); }
  }
  if (e.key === 'Escape') comboClose();
});
comboItems.forEach(li => li.addEventListener('click', () => comboPick(li)));
document.addEventListener('click', e => { if (!combo.contains(e.target)) comboClose(); });
