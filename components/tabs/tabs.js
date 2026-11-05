// KATA Tabs — WAI-ARIA APG tabs with automatic activation, independent instances.
(() => {
  let nextId = 0;
  function ensureId(element, suffix) {
    if (element.id) return element.id;
    let id;
    do { id = `kata-tabs-${++nextId}-${suffix}`; } while (document.getElementById(id));
    element.id = id;
    return id;
  }
  // Panels are the [data-tabpane] elements after the tab list, up to the next tab list.
  function panelsFor(list, count) {
    const panels = [];
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT);
    walker.currentNode = list;
    let node;
    while (panels.length < count && (node = walker.nextNode())) {
      if (node.matches('[data-tabs]')) break;
      if (list.contains(node)) continue;
      if (node.matches('[data-tabpane]')) panels.push(node);
    }
    return panels;
  }
  const instances = [];
  function place(instance) {
    const active = instance.tabs[instance.index];
    if (!instance.thumb || !active) return;
    instance.thumb.style.left = active.offsetLeft + 'px';
    instance.thumb.style.width = active.offsetWidth + 'px';
  }
  const resize = typeof ResizeObserver === 'function' ? new ResizeObserver(entries => entries.forEach(entry => { const instance = instances.find(item => item.list === entry.target); if (instance) place(instance); })) : null;
  document.querySelectorAll('[data-tabs]').forEach(list => {
    if (list.hasAttribute('data-kata-ready')) return;
    const tabs = [...list.querySelectorAll('button')];
    if (!tabs.length) return;
    list.setAttribute('data-kata-ready', '');
    list.setAttribute('role', 'tablist');
    const thumb = list.querySelector('.thumb');
    if (thumb) thumb.setAttribute('aria-hidden', 'true');
    const panels = panelsFor(list, tabs.length);
    const instance = { list, tabs, thumb, index: Math.max(0, tabs.findIndex(tab => tab.classList.contains('on'))) };
    tabs.forEach((tab, i) => {
      tab.setAttribute('role', 'tab');
      ensureId(tab, 'tab');
      const panel = panels[i];
      if (panel) {
        panel.setAttribute('role', 'tabpanel');
        tab.setAttribute('aria-controls', ensureId(panel, 'panel'));
        if (!panel.hasAttribute('aria-labelledby') && !panel.hasAttribute('aria-label')) panel.setAttribute('aria-labelledby', tab.id);
        // A panel without focusable content takes focus itself, so Tab reaches it (APG).
        if (!panel.hasAttribute('tabindex') && !panel.querySelector('a[href],button,input,select,textarea,[tabindex]')) panel.tabIndex = 0;
      }
    });
    function select(i, focus, quiet) {
      instance.index = i;
      tabs.forEach((tab, j) => {
        const on = j === i;
        tab.classList.toggle('on', on);
        tab.setAttribute('aria-selected', String(on));
        tab.tabIndex = on ? 0 : -1;
        if (panels[j]) panels[j].hidden = !on;
      });
      place(instance);
      if (focus) tabs[i].focus();
      if (!quiet) list.dispatchEvent(new CustomEvent('kata-tabs-change', { bubbles: true, detail: { index: i, tab: tabs[i], panel: panels[i] || null } }));
    }
    tabs.forEach((tab, i) => tab.addEventListener('click', () => select(i, false)));
    list.addEventListener('keydown', event => {
      if (event.isComposing || event.keyCode === 229) return;
      const i = tabs.indexOf(document.activeElement);
      if (i < 0) return;
      // Horizontal arrows follow the visual direction: in RTL, ArrowLeft moves forward.
      const rtl = getComputedStyle(list).direction === 'rtl';
      let next = null;
      if (event.key === 'ArrowRight') next = rtl ? i - 1 : i + 1;
      else if (event.key === 'ArrowLeft') next = rtl ? i + 1 : i - 1;
      else if (event.key === 'Home') next = 0;
      else if (event.key === 'End') next = tabs.length - 1;
      if (next === null) return;
      event.preventDefault();
      select((next + tabs.length) % tabs.length, true);
    });
    instances.push(instance);
    select(instance.index, false, true);
    if (resize) resize.observe(list);
  });
})();
