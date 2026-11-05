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
  function exitController(panel, finish) {
    let timer, listener;
    function cancel() {
      clearTimeout(timer);
      if (listener) {
        panel.removeEventListener('transitionend', listener);
        panel.removeEventListener('animationend', listener);
      }
      listener = null;
      panel.classList.remove('kata-closing');
    }
    function close() {
      cancel();
      panel.classList.add('kata-closing');
      const style = getComputedStyle(panel);
      const seconds = value => value.split(',').map(part => parseFloat(part) * (part.trim().endsWith('ms') ? 1 : 1000) || 0);
      function longest(durations, delays, iterations) {
        const d = seconds(durations), t = seconds(delays);
        const n = (iterations || '1').split(',').map(Number);
        return Math.max(0, ...d.map((value, index) => value * (Number.isFinite(n[index % n.length]) ? n[index % n.length] : 1) + t[index % t.length]));
      }
      const duration = Math.max(longest(style.transitionDuration, style.transitionDelay), longest(style.animationDuration, style.animationDelay, style.animationIterationCount));
      const started = performance.now();
      const complete = () => { cancel(); finish(); };
      if (!duration) { complete(); return; }
      listener = event => {
        if (event.target === panel && performance.now() - started >= duration - 16) complete();
      };
      panel.addEventListener('transitionend', listener);
      panel.addEventListener('animationend', listener);
      timer = setTimeout(complete, duration + 50);
    }
    return { cancel, close };
  }

  document.querySelectorAll('[data-dp]').forEach(root => {
    if (root.dataset.kataReady) return;
    const input = root.querySelector('[data-dp-input]'), panel = root.querySelector('[data-dp-panel]');
    const grid = root.querySelector('[data-dp-grid]'), title = root.querySelector('[data-dp-title]');
    const trigger = root.querySelector('[data-dp-btn]');
    if (!input || !panel || !grid || !title || !trigger) return;
    root.dataset.kataReady = 'true'; identify(root, 'kata-date-picker');
    const inputId = identify(input, 'kata-date-input'), panelId = identify(panel, 'kata-date-panel');
    const label = root.querySelector('[data-dp-label],label'); if (label && !label.htmlFor) label.htmlFor = inputId;
    identify(grid, 'kata-date-grid'); identify(title, 'kata-date-title');
    input.setAttribute('aria-controls', panelId); input.setAttribute('aria-haspopup', 'dialog');
    trigger.setAttribute('aria-controls', panelId); trigger.setAttribute('aria-haspopup', 'dialog');
    panel.setAttribute('aria-labelledby', title.id);
    grid.setAttribute('role', 'grid'); grid.setAttribute('aria-labelledby', title.id);
    title.setAttribute('aria-live', 'polite'); title.setAttribute('aria-atomic', 'true');
    const weekdays = root.querySelector('.k-dp-wd');
    if (weekdays) {
      weekdays.setAttribute('role', 'row');
      weekdays.querySelectorAll('span').forEach(day => day.setAttribute('role', 'columnheader'));
      grid.prepend(weekdays);
    }
    const same = (a, b) => a && b && a.toDateString() === b.toDateString();
    const key = date => [date.getFullYear(), String(date.getMonth() + 1).padStart(2, '0'), String(date.getDate()).padStart(2, '0')].join('-');
    const parse = value => {
      const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(value);
      if (!match) return null;
      const date = new Date(+match[1], +match[2] - 1, +match[3]); return key(date) === value ? date : null;
    };
    let selected = parse(input.value), focused = selected || new Date();
    let view = new Date(focused.getFullYear(), focused.getMonth(), 1), composing = false, opener = input, restore = false;
    let compositionEnding = false;
    const exit = exitController(panel, () => {
      panel.hidden = true; input.setAttribute('aria-expanded', 'false'); trigger.setAttribute('aria-expanded', 'false');
      if (restore && opener.isConnected) opener.focus();
    });
    function render(moveFocus = false) {
      title.textContent = view.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
      grid.querySelectorAll('[data-dp-week]').forEach(row => row.remove());
      const first = new Date(view.getFullYear(), view.getMonth(), 1 - view.getDay());
      for (let week = 0; week < 6; week++) {
        const row = document.createElement('div'); row.dataset.dpWeek = ''; row.setAttribute('role', 'row');
        for (let day = 0; day < 7; day++) {
          const date = new Date(first.getFullYear(), first.getMonth(), first.getDate() + week * 7 + day);
          const cell = document.createElement('button'); cell.type = 'button'; cell.className = 'k-dp-day';
          cell.setAttribute('role', 'gridcell'); cell.dataset.d = key(date); identify(cell, 'kata-date-day');
          cell.textContent = date.getDate(); cell.setAttribute('aria-label', date.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' }));
          cell.setAttribute('aria-selected', String(!!same(selected, date)));
          cell.classList.toggle('out', date.getMonth() !== view.getMonth());
          cell.classList.toggle('sel', !!same(selected, date)); cell.classList.toggle('today', !!same(new Date(), date));
          if (same(new Date(), date)) cell.setAttribute('aria-current', 'date');
          cell.tabIndex = same(focused, date) ? 0 : -1; row.append(cell);
        }
        grid.append(row);
      }
      if (moveFocus) grid.querySelector('[tabindex="0"]')?.focus();
    }
    function close(focus = false) { if (!panel.hidden) { restore = focus; exit.close(); } }
    function open(source = input) {
      exit.cancel(); opener = source; focused = selected || focused;
      view = new Date(focused.getFullYear(), focused.getMonth(), 1);
      panel.hidden = false; input.setAttribute('aria-expanded', 'true'); trigger.setAttribute('aria-expanded', 'true'); render(true);
    }
    function monthMove(amount) {
      const month = new Date(focused.getFullYear(), focused.getMonth() + amount, 1);
      focused = new Date(month.getFullYear(), month.getMonth(), Math.min(focused.getDate(), new Date(month.getFullYear(), month.getMonth() + 1, 0).getDate()));
      view = new Date(focused.getFullYear(), focused.getMonth(), 1);
    }
    function select(date) {
      if (!date || composing) return;
      selected = date; focused = date;
      input.value = date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
      input.dataset.date = key(date);
      input.dispatchEvent(new Event('input', { bubbles: true })); input.dispatchEvent(new Event('change', { bubbles: true })); close(true);
    }
    [input, trigger].forEach(button => button.addEventListener('click', () => panel.hidden || panel.classList.contains('kata-closing') ? open(button) : close(true)));
    root.querySelector('[data-dp-prev]')?.addEventListener('click', () => { monthMove(-1); render(); });
    root.querySelector('[data-dp-next]')?.addEventListener('click', () => { monthMove(1); render(); });
    grid.addEventListener('click', event => { const cell = event.target.closest('[data-d]'); if (cell && grid.contains(cell)) select(parse(cell.dataset.d)); });
    grid.addEventListener('focusin', event => {
      const cell = event.target.closest('[data-d]'); if (!cell) return;
      focused = parse(cell.dataset.d); grid.querySelectorAll('[data-d]').forEach(day => { day.tabIndex = day === cell ? 0 : -1; });
    });
    root.addEventListener('compositionstart', () => { composing = true; });
    root.addEventListener('compositionend', () => { composing = false; compositionEnding = true; setTimeout(() => { compositionEnding = false; }, 0); });
    root.addEventListener('keydown', event => {
      if (composing || compositionEnding || event.isComposing || event.keyCode === 229) return;
      if (event.key === 'Escape' && !panel.hidden) { event.preventDefault(); close(true); return; }
      if (panel.hidden && (event.target === input || event.target === trigger) && ['ArrowDown', 'Enter', ' '].includes(event.key)) { event.preventDefault(); open(event.target); return; }
      if (panel.hidden || !event.target.closest('[data-d]')) return;
      const horizontal = getComputedStyle(grid).direction === 'rtl' ? -1 : 1;
      const movement = { ArrowLeft: -horizontal, ArrowRight: horizontal, ArrowUp: -7, ArrowDown: 7 };
      if (event.key in movement) focused = new Date(focused.getFullYear(), focused.getMonth(), focused.getDate() + movement[event.key]);
      else if (event.key === 'Home' || event.key === 'End') focused = new Date(focused.getFullYear(), focused.getMonth(), focused.getDate() + (event.key === 'Home' ? -focused.getDay() : 6 - focused.getDay()));
      else if (event.key === 'PageUp' || event.key === 'PageDown') monthMove((event.key === 'PageUp' ? -1 : 1) * (event.shiftKey ? 12 : 1));
      else if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); select(focused); return; }
      else return;
      event.preventDefault(); view = new Date(focused.getFullYear(), focused.getMonth(), 1); render(true);
    });
    root.addEventListener('focusout', event => { if (event.relatedTarget && !root.contains(event.relatedTarget)) close(); });
    document.addEventListener('pointerdown', event => { if (!root.contains(event.target)) close(); });
    input.setAttribute('aria-expanded', 'false'); trigger.setAttribute('aria-expanded', 'false'); render();
  });
})();
