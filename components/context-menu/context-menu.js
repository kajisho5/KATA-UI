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

  document.querySelectorAll('[data-ctx-zone]').forEach(zone => {
    if (zone.dataset.kataReady) return;
    const target = zone.getAttribute('aria-controls');
    const menu = target ? document.getElementById(target) : zone.parentElement.querySelector('[data-ctx]');
    if (!menu || menu.dataset.kataReady) return;
    zone.dataset.kataReady = menu.dataset.kataReady = 'true';
    identify(zone, 'kata-context-zone');
    zone.setAttribute('aria-controls', identify(menu, 'kata-context-menu'));
    zone.setAttribute('aria-haspopup', 'menu'); zone.setAttribute('aria-expanded', 'false');
    menu.setAttribute('role', 'menu');
    menu.setAttribute('aria-labelledby', zone.id);
    const items = [...menu.querySelectorAll('[role="menuitem"],button')];
    items.forEach(item => { identify(item, 'kata-context-item'); item.setAttribute('role', 'menuitem'); item.tabIndex = -1; });
    menu.querySelectorAll('hr').forEach(line => line.setAttribute('role', 'separator'));
    const available = () => items.filter(item => !item.disabled && !item.hidden);
    let composing = false, search = '', searchTimer, restore = false;
    let compositionEnding = false;
    const exit = exitController(menu, () => {
      menu.hidden = true; zone.setAttribute('aria-expanded', 'false');
      if (restore && zone.isConnected) zone.focus();
    });
    function close(focus = true) { if (menu.hidden) return; restore = focus; exit.close(); }
    function focusItem(index) {
      const options = available(); const item = options[(index + options.length) % options.length];
      items.forEach(candidate => { candidate.tabIndex = candidate === item ? 0 : -1; });
      item?.focus();
    }
    function open(x, y) {
      exit.cancel(); clearTimeout(searchTimer); search = '';
      menu.hidden = false; zone.setAttribute('aria-expanded', 'true');
      const rect = menu.getBoundingClientRect();
      const margin = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--k-space-2')) || 0;
      const left = Math.max(margin, Math.min(x + rect.width > innerWidth ? x - rect.width : x, innerWidth - rect.width - margin));
      const top = Math.max(margin, Math.min(y + rect.height > innerHeight ? y - rect.height : y, innerHeight - rect.height - margin));
      menu.style.insetInlineStart = (getComputedStyle(menu).direction === 'rtl' ? innerWidth - left - rect.width : left) + 'px';
      menu.style.insetBlockStart = top + 'px'; focusItem(0);
    }
    zone.addEventListener('contextmenu', event => { event.preventDefault(); open(event.clientX, event.clientY); });
    zone.addEventListener('keydown', event => {
      if (composing || compositionEnding || event.isComposing || event.keyCode === 229) return;
      if (event.key === 'ContextMenu' || (event.shiftKey && event.key === 'F10')) {
        event.preventDefault(); const rect = zone.getBoundingClientRect(); open(rect.left, rect.bottom);
      }
    });
    [zone, menu].forEach(element => {
      element.addEventListener('compositionstart', () => { composing = true; });
      element.addEventListener('compositionend', () => { composing = false; compositionEnding = true; setTimeout(() => { compositionEnding = false; }, 0); });
      element.addEventListener('focusout', event => {
        if (!event.relatedTarget || zone.contains(event.relatedTarget) || menu.contains(event.relatedTarget)) return;
        close(false);
      });
    });
    menu.addEventListener('keydown', event => {
      if (composing || compositionEnding || event.isComposing || event.keyCode === 229) return;
      const options = available(), index = options.indexOf(document.activeElement);
      if (['ArrowDown', 'ArrowUp', 'Home', 'End'].includes(event.key)) {
        event.preventDefault(); focusItem(event.key === 'Home' ? 0 : event.key === 'End' ? options.length - 1 : index + (event.key === 'ArrowDown' ? 1 : -1));
      } else if (event.key === 'Escape' || event.key === 'Tab') {
        event.preventDefault(); close();
      } else if (event.key.length === 1 && !event.ctrlKey && !event.metaKey && !event.altKey && event.key !== ' ') {
        event.preventDefault(); clearTimeout(searchTimer); search += event.key.toLocaleLowerCase();
        const query = [...search].every(letter => letter === search[0]) ? search[0] : search;
        for (let offset = 1; offset <= options.length; offset++) {
          const next = (index + offset) % options.length;
          const text = [...options[next].childNodes].filter(node => node.nodeType === Node.TEXT_NODE).map(node => node.textContent).join('').trim().toLocaleLowerCase();
          if (text.startsWith(query)) { focusItem(next); break; }
        }
        searchTimer = setTimeout(() => { search = ''; }, 700);
      }
    });
    items.forEach(item => item.addEventListener('click', () => close()));
    document.addEventListener('pointerdown', event => { if (!zone.contains(event.target) && !menu.contains(event.target)) close(false); });
  });
})();
