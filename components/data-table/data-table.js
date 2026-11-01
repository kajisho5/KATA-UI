const dt = document.querySelector('[data-dt]');
const dtBody = dt.querySelector('tbody');
dt.querySelectorAll('[data-sort]').forEach(btn => {
  btn.addEventListener('click', () => {
    const th = btn.closest('th');
    const col = [...th.parentNode.children].indexOf(th);
    const type = btn.dataset.sort;
    const dir = btn.dataset.dir === 'asc' ? 'desc' : 'asc';
    dt.querySelectorAll('[data-sort]').forEach(b => { b.dataset.dir = ''; b.closest('th').removeAttribute('aria-sort'); });
    btn.dataset.dir = dir;
    th.setAttribute('aria-sort', dir === 'asc' ? 'ascending' : 'descending');
    const rows = [...dtBody.rows];
    rows.sort((a, b) => {
      const x = a.cells[col].dataset.v ?? a.cells[col].textContent.trim();
      const y = b.cells[col].dataset.v ?? b.cells[col].textContent.trim();
      const cmp = type === 'num' ? (+x - +y) : String(x).localeCompare(String(y));
      return dir === 'asc' ? cmp : -cmp;
    });
    rows.forEach(r => dtBody.appendChild(r));
  });
});
