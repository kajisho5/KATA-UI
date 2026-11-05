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

  document.querySelectorAll('[data-command]').forEach(dialog => {
    if (dialog.dataset.kataReady) return;
    const input = dialog.querySelector('[data-command-input]');
    const list = dialog.querySelector('.kcmd-list');
    if (!input || !list || typeof dialog.showModal !== 'function') return;
    dialog.dataset.kataReady = 'true';
    const id = identify(dialog, 'kata-command');
    identify(input, 'kata-command-input');
    input.setAttribute('role', 'combobox');
    input.setAttribute('aria-autocomplete', 'list');
    input.setAttribute('aria-expanded', 'false');
    input.setAttribute('aria-controls', identify(list, 'kata-command-list'));
    list.setAttribute('role', 'listbox');
    const items = [...dialog.querySelectorAll('[data-cmd-item]')];
    items.forEach(item => {
      identify(item, 'kata-command-option');
      item.setAttribute('role', 'option');
      item.tabIndex = -1;
      item.parentElement.setAttribute('role', 'presentation');
    });
    let status = dialog.querySelector('[role="status"]');
    if (!status) {
      status = document.createElement('div');
      status.className = 'kcmd-status'; status.setAttribute('role', 'status');
      dialog.append(status);
    }
    const empty = dialog.querySelector('[data-command-empty]');
    let active = 0, composing = false, opener;
    const visible = () => items.filter(item => !item.parentElement.hidden);
    function setActive(index) {
      const options = visible();
      active = options.length ? (index + options.length) % options.length : -1;
      items.forEach(item => {
        const selected = item === options[active];
        item.classList.toggle('active', selected);
        item.setAttribute('aria-selected', String(selected));
      });
      if (options[active] && dialog.open) {
        input.setAttribute('aria-activedescendant', options[active].id);
        options[active].scrollIntoView({ block: 'nearest' });
      } else input.removeAttribute('aria-activedescendant');
    }
    function filter(announce = false) {
      const query = input.value.trim().toLocaleLowerCase();
      items.forEach(item => { item.parentElement.hidden = !item.textContent.toLocaleLowerCase().includes(query); });
      const count = visible().length;
      if (empty) { empty.hidden = count !== 0; empty.style.display = ''; }
      if (announce) status.textContent = count + (count === 1 ? ' result.' : ' results.');
      setActive(0);
    }
    let compositionEnding = false;
    const exit = exitController(dialog, () => {
      input.setAttribute('aria-expanded', 'false'); input.removeAttribute('aria-activedescendant');
      if (dialog.open) dialog.close();
    });
    function close() { if (dialog.open) exit.close(); }
    function open(trigger) {
      exit.cancel(); opener = trigger || document.activeElement;
      if (!dialog.open) dialog.showModal();
      input.value = ''; status.textContent = ''; filter();
      input.setAttribute('aria-expanded', 'true'); input.focus();
    }
    document.querySelectorAll('[data-command-open]').forEach(trigger => {
      const target = trigger.getAttribute('aria-controls');
      const following = [...document.querySelectorAll('[data-command]')].find(candidate => trigger.compareDocumentPosition(candidate) & Node.DOCUMENT_POSITION_FOLLOWING);
      if (target ? target !== id : following !== dialog) return;
      identify(trigger, 'kata-command-trigger');
      trigger.setAttribute('aria-controls', id); trigger.setAttribute('aria-haspopup', 'dialog');
      trigger.addEventListener('click', () => open(trigger));
    });
    dialog.addEventListener('compositionstart', () => { composing = true; });
    dialog.addEventListener('compositionend', () => { composing = false; compositionEnding = true; setTimeout(() => { compositionEnding = false; }, 0); filter(true); });
    input.addEventListener('input', event => { if (!composing && !event.isComposing) filter(true); });
    input.addEventListener('keydown', event => {
      if (composing || compositionEnding || event.isComposing || event.keyCode === 229) return;
      if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
        event.preventDefault(); setActive(active + (event.key === 'ArrowDown' ? 1 : -1));
      } else if (event.key === 'Enter') {
        event.preventDefault(); const item = visible()[active]; if (item) item.click();
      }
    });
    items.forEach(item => item.addEventListener('click', () => {
      if (composing) return;
      dialog.dispatchEvent(new CustomEvent('kata-command-select', { bubbles: true, detail: { item } }));
      close();
    }));
    dialog.addEventListener('keydown', event => {
      if ((composing || compositionEnding || event.isComposing || event.keyCode === 229) && event.key === 'Escape') event.preventDefault();
    });
    dialog.addEventListener('cancel', event => {
      if (composing || compositionEnding) { event.preventDefault(); return; }
      // Native Escape retains the cancel event, including application preventDefault().
    });
    dialog.addEventListener('close', () => {
      if (dialog.open) return;
      exit.cancel(); input.setAttribute('aria-expanded', 'false'); input.removeAttribute('aria-activedescendant');
      if (opener?.isConnected) opener.focus();
    });
    document.addEventListener('keydown', event => {
      if (event.isComposing || composing || event.keyCode === 229 || !(event.metaKey || event.ctrlKey) || event.key.toLowerCase() !== 'k') return;
      const dialogs = [...document.querySelectorAll('[data-command][data-kata-ready]')];
      const focused = document.activeElement;
      const target = dialogs.find(candidate => candidate.open) || dialogs.find(candidate => focused?.getAttribute('aria-controls') === candidate.id) || dialogs[0];
      if (target !== dialog) return;
      event.preventDefault(); if (!dialog.open) open(focused);
    });
    filter();
  });
})();
