// KATA Dropdown — menu button (WAI-ARIA APG pattern), independent instances.
(() => {
  let nextId = 0;
  function ensureId(element, suffix) {
    if (element.id) return element.id;
    let id;
    do { id = `kata-dropdown-${++nextId}-${suffix}`; } while (document.getElementById(id));
    element.id = id;
    return id;
  }
  const ITEMS = 'a[href],button,[role="menuitem"]';
  const instances = [];
  function emit(root, open) { root.dispatchEvent(new CustomEvent('kata-dropdown-toggle', { bubbles: true, detail: { open } })); }
  document.querySelectorAll('[data-dd-trigger]').forEach(trigger => {
    const root = trigger.closest('.dd') || trigger.parentElement;
    const menu = root && root.querySelector('[data-dd-menu]');
    if (!menu || root.hasAttribute('data-kata-ready')) return;
    root.setAttribute('data-kata-ready', '');
    const menuId = ensureId(menu, 'menu');
    trigger.setAttribute('aria-haspopup', 'menu');
    trigger.setAttribute('aria-controls', menuId);
    trigger.setAttribute('aria-expanded', 'false');
    menu.setAttribute('role', 'menu');
    if (!menu.hasAttribute('aria-label') && !menu.hasAttribute('aria-labelledby')) menu.setAttribute('aria-labelledby', ensureId(trigger, 'trigger'));
    const items = () => [...menu.querySelectorAll(ITEMS)].filter(item => !item.hidden && item.getAttribute('aria-disabled') !== 'true' && !item.disabled);
    menu.querySelectorAll(ITEMS).forEach(item => { item.setAttribute('role', 'menuitem'); item.tabIndex = -1; });
    menu.querySelectorAll('hr').forEach(hr => hr.setAttribute('role', 'separator'));
    menu.querySelectorAll('.mh').forEach(heading => heading.setAttribute('role', 'presentation'));
    const isOpen = () => menu.classList.contains('open');
    function open(focus) {
      if (!isOpen()) {
        instances.forEach(other => { if (other.root !== root) other.close(false); });
        menu.classList.add('open');
        trigger.setAttribute('aria-expanded', 'true');
        emit(root, true);
      }
      const list = items();
      const target = focus === 'last' ? list[list.length - 1] : list[0];
      if (target) target.focus();
    }
    function close(returnFocus) {
      if (!isOpen()) return;
      menu.classList.remove('open');
      trigger.setAttribute('aria-expanded', 'false');
      if (returnFocus) trigger.focus();
      emit(root, false);
    }
    instances.push({ root, close });
    trigger.addEventListener('click', () => { if (isOpen()) close(true); else open('first'); });
    trigger.addEventListener('keydown', event => {
      if (event.isComposing || event.keyCode === 229) return;
      if (event.key === 'ArrowDown') { event.preventDefault(); open('first'); }
      else if (event.key === 'ArrowUp') { event.preventDefault(); open('last'); }
      else if (event.key === 'Escape' && isOpen()) { event.preventDefault(); close(true); }
    });
    menu.addEventListener('keydown', event => {
      if (event.isComposing || event.keyCode === 229) return;
      const list = items();
      const index = list.indexOf(document.activeElement);
      let next = null;
      if (event.key === 'ArrowDown') next = list[(index + 1) % list.length];
      else if (event.key === 'ArrowUp') next = list[(index - 1 + list.length) % list.length];
      else if (event.key === 'Home' || event.key === 'PageUp') next = list[0];
      else if (event.key === 'End' || event.key === 'PageDown') next = list[list.length - 1];
      else if (event.key === 'Escape') { event.preventDefault(); close(true); return; }
      else if (event.key === 'Tab') { close(false); return; }
      else if (event.key === ' ' && document.activeElement?.matches('a[href]')) { event.preventDefault(); document.activeElement.click(); return; }
      if (next) { event.preventDefault(); next.focus(); }
    });
    menu.addEventListener('click', event => { if (event.target.closest(ITEMS)) close(true); });
    // A null relatedTarget (window switch, removed node) never closes the menu.
    root.addEventListener('focusout', event => { if (event.relatedTarget && !root.contains(event.relatedTarget)) close(false); });
  });
  // One outside-press and one window-blur listener per script load, shared by its instances.
  if (!instances.length) return;
  document.addEventListener('pointerdown', event => { instances.forEach(instance => { if (!instance.root.contains(event.target)) instance.close(false); }); });
  window.addEventListener('blur', () => instances.forEach(instance => instance.close(false)));
})();
