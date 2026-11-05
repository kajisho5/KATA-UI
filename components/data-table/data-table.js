(() => {
  'use strict';
  let serial = 0;
  function identify(element, prefix) {
    if (!element.id) {
      let candidate;
      do { candidate = prefix + '-' + (++serial); } while (document.getElementById(candidate));
      element.id = candidate;
    }
    return element.id;
  }

  document.querySelectorAll('[data-dt]').forEach(root => {
    if (root.dataset.kataReady) return;
    const table = root.querySelector('table'), body = table?.tBodies[0]; if (!body) return;
    root.dataset.kataReady = 'true'; identify(root, 'kata-data-table'); identify(table, 'kata-data-grid');
    if (!table.caption && !table.hasAttribute('aria-labelledby') && !table.hasAttribute('aria-label')) table.setAttribute('aria-label', 'Data table');
    const status = document.createElement('span'); status.className = 'k-dt-status'; status.setAttribute('role', 'status');
    identify(status, 'kata-data-status'); root.append(status);
    const sorters = [...table.querySelectorAll('[data-sort]')];
    sorters.forEach(button => {
      identify(button, 'kata-data-sort'); button.setAttribute('aria-controls', table.id);
      button.addEventListener('click', () => {
        const header = button.closest('th'), column = header.cellIndex;
        const direction = button.dataset.dir === 'asc' ? 'desc' : 'asc';
        sorters.forEach(other => {
          other.dataset.dir = ''; other.closest('th').setAttribute('aria-sort', 'none');
        });
        button.dataset.dir = direction;
        const aria = direction === 'asc' ? 'ascending' : 'descending';
        // aria-sort belongs on the column header, not its native button.
        header.setAttribute('aria-sort', aria); button.removeAttribute('aria-sort');
        const rows = [...body.rows];
        rows.sort((a, b) => {
          const x = a.cells[column].dataset.v ?? a.cells[column].textContent.trim();
          const y = b.cells[column].dataset.v ?? b.cells[column].textContent.trim();
          const order = button.dataset.sort === 'num' ? Number(x) - Number(y) : String(x).localeCompare(String(y));
          return direction === 'asc' ? order : -order;
        });
        rows.forEach(row => body.append(row)); status.textContent = button.textContent.trim() + ' sorted ' + aria + '.';
        root.dispatchEvent(new CustomEvent('kata-data-table-sort', { bubbles: true, detail: { column, direction } }));
      });
    });
    const all = table.querySelector('thead input[type="checkbox"]');
    const selected = () => [...body.querySelectorAll('input[type="checkbox"]:checked')];
    function selection() {
      const boxes = [...body.querySelectorAll('input[type="checkbox"]')];
      if (all) { all.checked = boxes.length > 0 && boxes.every(box => box.checked); all.indeterminate = selected().length > 0 && !all.checked; }
      status.textContent = selected().length + ' rows selected.';
    }
    table.querySelectorAll('input[type="checkbox"]').forEach((input, index) => {
      identify(input, 'kata-data-select');
      if (!input.hasAttribute('aria-label')) input.setAttribute('aria-label', input === all ? 'Select all rows' : 'Select row ' + index);
      input.addEventListener('change', () => {
        if (input === all) body.querySelectorAll('input[type="checkbox"]:not(:disabled)').forEach(box => { box.checked = all.checked; });
        selection();
      });
    });
  });
})();
