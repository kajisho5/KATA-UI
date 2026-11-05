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
  // Group rows and scenes by their section so each copy switches independently.
  const roots = new Set([...document.querySelectorAll('[data-uc-row]')].map(row => row.closest('.k-uc') || row.parentElement.parentElement));

  roots.forEach(root => {
    if (root.dataset.kataReady) return;
    const rows = [...root.querySelectorAll('[data-uc-row]')];
    const scenes = [...root.querySelectorAll('[data-uc-scene]')];
    if (!rows.length) return;
    root.dataset.kataReady = 'true';
    identify(root, 'kata-uc');
    rows.forEach((row, i) => {
      row.type = 'button';
      identify(row, 'kata-uc-row');
      if (scenes[i]) row.setAttribute('aria-controls', identify(scenes[i], 'kata-uc-scene'));
    });
    let current = Math.max(0, rows.findIndex(row => row.classList.contains('open')));
    function show(index, notify) {
      rows.forEach((row, j) => {
        row.classList.toggle('open', j === index);
        row.setAttribute('aria-expanded', String(j === index));
      });
      scenes.forEach((scene, j) => { scene.hidden = j !== index; });
      if (notify && index !== current) root.dispatchEvent(new CustomEvent('kata-use-cases-change', { bubbles: true, detail: { index } }));
      current = index;
    }
    show(current, false);
    rows.forEach((row, i) => row.addEventListener('click', () => show(i, true)));
    root.addEventListener('keydown', event => {
      const row = event.target.closest('[data-uc-row]');
      if (!row || !rows.includes(row) || event.isComposing || event.keyCode === 229) return;
      const index = rows.indexOf(row), last = rows.length - 1;
      let next = null;
      if (event.key === 'ArrowDown') next = index === last ? 0 : index + 1;
      else if (event.key === 'ArrowUp') next = index === 0 ? last : index - 1;
      else if (event.key === 'Home') next = 0;
      else if (event.key === 'End') next = last;
      if (next === null) return;
      // Arrows move focus only, as in an accordion; Enter or Space switches the case.
      event.preventDefault(); rows[next].focus();
    });
  });
})();
