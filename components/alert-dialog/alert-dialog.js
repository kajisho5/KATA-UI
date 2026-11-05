// KATA Alert Dialog — independent native modal instances.
(() => {
  let nextId = 0;
  function ensureId(element, suffix) {
    if (element.id) return element.id;
    let id;
    do { id = `kata-alert-dialog-${++nextId}-${suffix}`; } while (document.getElementById(id));
    element.id = id;
    return id;
  }
  const dialogs = [...document.querySelectorAll('[data-alert-dialog]')];
  const triggers = [...document.querySelectorAll('[data-alert-open]')];
  function targetOf(trigger) {
    const controls = trigger.getAttribute('aria-controls');
    if (controls) {
      const target = dialogs.find(dialog => dialog.id === controls);
      if (target) return target;
    }
    return dialogs.find(dialog => trigger.compareDocumentPosition(dialog) & Node.DOCUMENT_POSITION_FOLLOWING) || dialogs[dialogs.length - 1];
  }
  dialogs.forEach(dialog => {
    if (dialog.hasAttribute('data-kata-ready') || !(dialog instanceof HTMLDialogElement)) return;
    dialog.setAttribute('data-kata-ready', '');
    const id = ensureId(dialog, 'dialog');
    const heading = dialog.querySelector('h1,h2,h3,h4,h5,h6');
    const description = dialog.querySelector('p');
    if (!dialog.hasAttribute('aria-label') && !dialog.hasAttribute('aria-labelledby') && heading) dialog.setAttribute('aria-labelledby', ensureId(heading, 'title'));
    if (!dialog.hasAttribute('aria-describedby') && description) dialog.setAttribute('aria-describedby', ensureId(description, 'description'));
    if (!dialog.hasAttribute('tabindex')) dialog.tabIndex = -1;
    let opener = null;
    let composing = false;
    function focusables() {
      return [...dialog.querySelectorAll('button,a[href],input,select,textarea,[tabindex]')].filter(element => element.tabIndex >= 0 && !element.disabled && !element.closest('[inert]') && element.getClientRects().length && getComputedStyle(element).visibility !== 'hidden');
    }
    // Native close is immediate; it never waits for a CSS end event.
    function close() { composing = false; if (dialog.open) dialog.close(); }
    triggers.filter(trigger => targetOf(trigger) === dialog).forEach(trigger => {
      ensureId(trigger, 'trigger');
      trigger.setAttribute('aria-controls', id);
      trigger.setAttribute('aria-haspopup', 'dialog');
      trigger.addEventListener('click', () => {
        if (dialog.open) return;
        composing = false;
        opener = trigger;
        dialog.showModal();
        (focusables().find(element => element.hasAttribute('data-autofocus') || element.hasAttribute('autofocus')) || focusables().find(element => element.matches('button:not(.btn-pri):not(.btn-danger):not([data-primary])')) || dialog).focus();
      });
    });
    dialog.querySelectorAll('[data-alert-close]').forEach(button => button.addEventListener('click', close));
    dialog.addEventListener('compositionstart', () => { composing = true; });
    dialog.addEventListener('compositionend', () => { composing = false; });
    dialog.addEventListener('keydown', event => {
      if (composing || event.isComposing || event.keyCode === 229) {
        if (event.key === 'Escape') event.preventDefault();
        return;
      }
      if (event.key !== 'Tab') return;
      const items = focusables();
      const first = items[0], last = items[items.length - 1];
      if (!first) { event.preventDefault(); dialog.focus(); return; }
      if (event.shiftKey && (document.activeElement === first || document.activeElement === dialog)) { event.preventDefault(); last.focus(); }
      else if (!event.shiftKey && (document.activeElement === last || document.activeElement === dialog)) { event.preventDefault(); first.focus(); }
    });
    dialog.addEventListener('close', () => {
      if (dialog.open) return; // Ignore a queued close event from an earlier opening.
      composing = false;
      if (opener?.isConnected && !opener.disabled && !document.querySelectorAll('dialog[open]').length) opener.focus();
    });
  });
})();
