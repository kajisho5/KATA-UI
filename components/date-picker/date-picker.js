const dp = document.querySelector('[data-dp]');
const dpInput = dp.querySelector('[data-dp-input]');
const dpPanel = dp.querySelector('[data-dp-panel]');
const dpGrid = dp.querySelector('[data-dp-grid]');
const dpTitle = dp.querySelector('[data-dp-title]');
const MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December'];
let dpView = new Date(); dpView.setDate(1);
let dpSel = null;
function dpRender() {
  dpTitle.textContent = MONTHS[dpView.getMonth()] + ' ' + dpView.getFullYear();
  const y = dpView.getFullYear(), m = dpView.getMonth();
  const first = new Date(y, m, 1).getDay();
  const days = new Date(y, m + 1, 0).getDate();
  const prevDays = new Date(y, m, 0).getDate();
  const today = new Date();
  let html = '';
  for (let i = 0; i < 42; i++) {
    const d = i - first + 1;
    let date, out = false;
    if (d < 1) { date = new Date(y, m - 1, prevDays + d); out = true; }
    else if (d > days) { date = new Date(y, m + 1, d - days); out = true; }
    else date = new Date(y, m, d);
    const isToday = date.toDateString() === today.toDateString();
    const isSel = dpSel && date.toDateString() === dpSel.toDateString();
    html += `<button type="button" class="k-dp-day${out ? ' out' : ''}${isToday ? ' today' : ''}${isSel ? ' sel' : ''}" data-d="${date.toISOString()}"${isToday ? ' aria-current="date"' : ''}>${date.getDate()}</button>`;
    if (i >= 35 && (i - first + 1) >= days + (7 - (first + days) % 7) % 7 && out) break;
  }
  dpGrid.innerHTML = html;
}
function dpOpen() { dpPanel.hidden = false; dpInput.setAttribute('aria-expanded', 'true'); dpRender(); }
function dpClose() { dpPanel.hidden = true; dpInput.setAttribute('aria-expanded', 'false'); }
dpInput.addEventListener('click', () => dpPanel.hidden ? dpOpen() : dpClose());
dp.querySelector('[data-dp-btn]').addEventListener('click', () => dpPanel.hidden ? dpOpen() : dpClose());
dp.querySelector('[data-dp-prev]').addEventListener('click', () => { dpView.setMonth(dpView.getMonth() - 1); dpRender(); });
dp.querySelector('[data-dp-next]').addEventListener('click', () => { dpView.setMonth(dpView.getMonth() + 1); dpRender(); });
dpGrid.addEventListener('click', e => {
  const b = e.target.closest('[data-d]');
  if (!b) return;
  dpSel = new Date(b.dataset.d);
  dpInput.value = dpSel.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  dpClose();
  dpInput.focus();
});
document.addEventListener('click', e => { if (!dp.contains(e.target)) dpClose(); });
dp.addEventListener('keydown', e => {
  if (e.key === 'Escape') { dpClose(); dpInput.focus(); }
  if (e.key === 'PageDown' && !dpPanel.hidden) { e.preventDefault(); dpView.setMonth(dpView.getMonth() + 1); dpRender(); }
  if (e.key === 'PageUp' && !dpPanel.hidden) { e.preventDefault(); dpView.setMonth(dpView.getMonth() - 1); dpRender(); }
});
dpRender();
