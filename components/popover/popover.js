// KATA Popover — independent non-modal panels.
(() => {
  let nextId = 0;
  function ensureId(element, suffix) {
    if (element.id) return element.id;
    let id;
    do { id = `kata-popover-${++nextId}-${suffix}`; } while (document.getElementById(id));
    element.id = id;
    return id;
  }
  const instances = [];
  // Keep the centred panel inside the viewport with a margin of one --k-space-4 on each side.
  function fit(panel) {
    panel.style.setProperty('--kpop-shift', '0px');
    const margin = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--k-space-4')) || 16;
    const rect = panel.getBoundingClientRect();
    const view = document.documentElement.clientWidth;
    let shift = 0;
    if (rect.left < margin) shift = margin - rect.left;
    else if (rect.right > view - margin) shift = view - margin - rect.right;
    panel.style.setProperty('--kpop-shift', `${Math.round(shift)}px`);
  }
  document.querySelectorAll('[data-popover]').forEach(wrap => {
    if (wrap.hasAttribute('data-kata-ready')) return;
    const trigger = wrap.querySelector('[data-popover-btn]');
    const panel = wrap.querySelector('[data-popover-panel]');
    if (!trigger || !panel) return;
    wrap.setAttribute('data-kata-ready', '');
    ensureId(trigger, 'trigger');
    trigger.setAttribute('aria-controls', ensureId(panel, 'panel'));
    trigger.setAttribute('aria-haspopup', 'dialog');
    if (!panel.hasAttribute('aria-label') && !panel.hasAttribute('aria-labelledby')) panel.setAttribute('aria-labelledby', ensureId(trigger, 'trigger'));
    let open = false;
    let timer;
    let composing = false;
    panel.hidden = true;
    panel.inert = true;
    trigger.setAttribute('aria-expanded', 'false');
    function finish() { if (!open) panel.hidden = true; clearTimeout(timer); }
    function close(restore = false) {
      if (!open) return;
      open = false;
      composing = false;
      panel.classList.remove('open');
      trigger.setAttribute('aria-expanded', 'false');
      panel.inert = true;
      const style = getComputedStyle(panel);
      const ms = value => value.split(',').map(part => parseFloat(part) * (part.trim().endsWith('ms') ? 1 : 1000));
      const duration = Math.max(...ms(style.transitionDuration));
      const delay = Math.max(0, ...ms(style.transitionDelay));
      clearTimeout(timer);
      if (duration === 0) finish();
      else timer = setTimeout(finish, duration + delay + 50);
      if (restore) trigger.focus();
    }
    function show() {
      clearTimeout(timer);
      open = true;
      composing = false;
      panel.hidden = false;
      panel.inert = false;
      fit(panel);
      void panel.offsetWidth;
      panel.classList.add('open');
      trigger.setAttribute('aria-expanded', 'true');
    }
    trigger.addEventListener('click', () => { if (open) close(); else show(); });
    wrap.addEventListener('compositionstart', () => { composing = true; });
    wrap.addEventListener('compositionend', () => { composing = false; });
    wrap.addEventListener('keydown', event => {
      if (composing || event.isComposing || event.keyCode === 229) return;
      if (event.key === 'Escape' && open) { event.preventDefault(); event.stopPropagation(); close(true); }
    });
    wrap.addEventListener('focusout', event => {
      if (!event.relatedTarget) return;
      if (!wrap.contains(event.relatedTarget)) close();
    });
    instances.push({ wrap, close, panel, isOpen: () => open });
    panel.addEventListener('transitionend', event => { if (event.target === panel && event.propertyName === 'opacity' && !open) finish(); });
    panel.addEventListener('transitioncancel', event => { if (event.target === panel && !open) finish(); });
  });
  // One outside-press and one resize listener per script load, shared by its instances.
  if (!instances.length) return;
  document.addEventListener('pointerdown', event => { instances.forEach(instance => { if (!instance.wrap.contains(event.target)) instance.close(); }); });
  window.addEventListener('resize', () => instances.forEach(instance => { if (instance.isOpen()) fit(instance.panel); }));
})();
