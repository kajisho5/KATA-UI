(() => {
  let nextId = 0;
  function ensureId(element, suffix) {
    if (element.id) return element.id;
    let id;
    do { id = `kata-combo-${++nextId}-${suffix}`; } while (document.getElementById(id));
    element.id = id;
    return id;
  }

  document.querySelectorAll('[data-combo]').forEach(combo => {
    if (combo.hasAttribute('data-kata-ready')) return;
    const input = combo.querySelector('[data-combo-input]');
    const list = combo.querySelector('[data-combo-list]');
    if (!input || !list) return;
    combo.setAttribute('data-kata-ready', '');
    const items = [...list.querySelectorAll('[data-val]')];
    const label = combo.querySelector('label');
    if (label) label.htmlFor = ensureId(input, 'input');
    input.setAttribute('role', 'combobox');
    input.setAttribute('aria-autocomplete', 'list');
    input.setAttribute('aria-controls', ensureId(list, 'list'));
    list.setAttribute('role', 'listbox');
    if (label) list.setAttribute('aria-labelledby', ensureId(label, 'label'));
    items.forEach(item => {
      ensureId(item, 'option');
      item.setAttribute('role', 'option');
      item.setAttribute('aria-selected', String(item.getAttribute('aria-selected') === 'true'));
    });
    // Support older markup, moving the empty message out of the listbox.
    let empty = combo.querySelector('.none');
    if (!empty) {
      empty = document.createElement('p');
      empty.className = 'none';
      empty.textContent = 'No matches.';
    }
    list.after(empty);
    let status = combo.querySelector('[role="status"]');
    if (!status) {
      status = document.createElement('span');
      status.className = 'k-combo-status';
      status.setAttribute('role', 'status');
      combo.append(status);
    }
    status.setAttribute('aria-atomic', 'true');
    let active = null;
    let composing = false;
    const enabled = item => item.getAttribute('aria-disabled') !== 'true';
    const visible = () => items.filter(item => !item.hidden && enabled(item));
    function clearActive() {
      active = null;
      items.forEach(item => item.classList.remove('act'));
      input.removeAttribute('aria-activedescendant');
    }
    function close() {
      list.hidden = true;
      empty.hidden = true;
      input.setAttribute('aria-expanded', 'false');
      clearActive();
      status.textContent = '';
    }
    function filter() {
      const query = input.value.trim().toLowerCase();
      clearActive();
      items.forEach(item => { item.hidden = !item.dataset.val.toLowerCase().includes(query); });
    }
    function open() {
      if (input.disabled || input.readOnly) return;
      list.hidden = false;
      input.setAttribute('aria-expanded', 'true');
      const count = visible().length;
      empty.hidden = count !== 0;
    }
    function highlight(item) {
      clearActive();
      if (!item) return;
      active = item;
      item.classList.add('act');
      input.setAttribute('aria-activedescendant', item.id);
      item.scrollIntoView({ block: 'nearest', behavior: 'instant' });
    }
    function pick(item) {
      if (!enabled(item) || input.disabled || input.readOnly) return;
      input.value = item.dataset.val;
      items.forEach(option => option.setAttribute('aria-selected', String(option === item)));
      close();
      input.dispatchEvent(new Event('change', { bubbles: true }));
    }
    function showAll() {
      clearActive();
      items.forEach(item => { item.hidden = false; });
      status.textContent = '';
      open();
    }
    function refresh() {
      filter();
      open();
      const count = visible().length;
      const message = count === 1
        ? (combo.dataset.comboResultOne || '{count} result available.')
        : (combo.dataset.comboResultMany || '{count} results available.');
      status.textContent = message.replaceAll('{count}', String(count));
    }
    input.addEventListener('focus', showAll);
    input.addEventListener('click', showAll);
    input.addEventListener('compositionstart', () => { composing = true; clearActive(); });
    input.addEventListener('compositionend', () => {
      composing = false;
      items.forEach(item => item.setAttribute('aria-selected', 'false'));
    });
    input.addEventListener('input', event => {
      if (composing || event.isComposing) return;
      items.forEach(item => item.setAttribute('aria-selected', 'false'));
      refresh();
    });
    input.addEventListener('keydown', event => {
      if (composing || event.isComposing || event.keyCode === 229 || input.disabled || input.readOnly) return;
      if (event.altKey && event.key === 'ArrowDown') {
        event.preventDefault();
        showAll();
        return;
      }
      if (event.key === 'Escape') {
        if (!list.hidden) { event.preventDefault(); event.stopPropagation(); close(); }
        return;
      }
      if (event.key === 'Tab') { close(); return; }
      if (event.key === 'Enter') {
        if (!list.hidden && active) { event.preventDefault(); pick(active); }
        return;
      }
      const arrow = event.key === 'ArrowDown' || event.key === 'ArrowUp';
      const boundary = event.key === 'Home' || event.key === 'End';
      if (!arrow && !(boundary && !list.hidden)) return;
      if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
      event.preventDefault();
      if (list.hidden) showAll();
      const options = visible();
      const index = options.indexOf(active);
      let next;
      if (event.key === 'Home') next = 0;
      else if (event.key === 'End') next = options.length - 1;
      else if (event.key === 'ArrowDown') next = index < 0 ? 0 : (index + 1) % options.length;
      else next = index < 0 ? options.length - 1 : (index - 1 + options.length) % options.length;
      highlight(options[next]);
    });
    items.forEach(item => {
      item.addEventListener('pointerdown', event => { event.preventDefault(); });
      item.addEventListener('click', () => { pick(item); });
    });
    combo.addEventListener('focusout', event => {
      if (!event.relatedTarget) return;
      if (!combo.contains(event.relatedTarget)) close();
    });
    document.addEventListener('click', event => { if (!combo.contains(event.target)) close(); });
    close();
  });
})();
