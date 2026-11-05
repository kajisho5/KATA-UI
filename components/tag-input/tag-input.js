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

  document.querySelectorAll('[data-tags]').forEach(root => {
    if (root.dataset.kataReady) return;
    const input = root.querySelector('.k-tags-in');
    if (!input) return;
    root.dataset.kataReady = 'true'; identify(root, 'kata-tags'); identify(input, 'kata-tags-input');
    const status = document.createElement('span'); status.className = 'k-tags-status'; status.setAttribute('role', 'status');
    identify(status, 'kata-tags-status'); root.append(status);
    let composing = false, finishing = false;
    const chips = () => [...root.querySelectorAll('.k-chip')];
    const text = chip => [...chip.childNodes].filter(node => node !== chip.querySelector('button')).map(node => node.textContent).join('').trim();
    function prepare(chip) {
      identify(chip, 'kata-tag');
      chip.dataset.tag = text(chip).toLocaleLowerCase();
      const button = chip.querySelector('.k-chip-x');
      if (button) { identify(button, 'kata-tag-remove'); button.setAttribute('aria-label', 'Remove tag ' + text(chip)); }
    }
    chips().forEach(prepare);
    function announce(action, tag) {
      status.textContent = (action === 'add' ? 'Added ' : 'Removed ') + tag + '.';
      root.dispatchEvent(new CustomEvent('kata-tag-input-' + action, { bubbles: true, detail: { tag, tags: chips().map(text) } }));
    }
    function add(value) {
      const tag = value.trim().replace(/,$/, '').trim();
      if (!tag) return;
      if (chips().some(chip => chip.dataset.tag === tag.toLocaleLowerCase())) { status.textContent = tag + ' is already added.'; return; }
      const chip = document.createElement('span'); chip.className = 'k-chip';
      const label = document.createElement('span'); label.textContent = tag;
      const button = document.createElement('button'); button.type = 'button'; button.className = 'k-chip-x';
      // The icon is application-owned markup; tag text never enters innerHTML.
      if (root.dataset.x) button.innerHTML = root.dataset.x; else button.textContent = '×';
      chip.append(label, button); prepare(chip); root.insertBefore(chip, input); announce('add', tag);
    }
    function remove(chip, moveFocus = false) {
      const list = chips(), index = list.indexOf(chip), tag = text(chip);
      chip.remove();
      if (moveFocus) (chips()[index]?.querySelector('button') || input).focus();
      announce('remove', tag);
    }
    root.addEventListener('compositionstart', () => { composing = true; });
    root.addEventListener('compositionend', () => { composing = false; finishing = true; setTimeout(() => { finishing = false; }, 0); });
    root.addEventListener('keydown', event => {
      if (composing || finishing || event.isComposing || event.keyCode === 229) return;
      const button = event.target.closest('.k-chip-x'), list = chips();
      if (event.target === input && (event.key === 'Enter' || event.key === ',')) {
        event.preventDefault(); add(input.value); input.value = ''; return;
      }
      if (event.key === 'Backspace' || event.key === 'Delete') {
        if (button) { event.preventDefault(); remove(button.closest('.k-chip'), true); }
        else if (event.target === input && event.key === 'Backspace' && !input.value && list.length) { event.preventDefault(); remove(list[list.length - 1]); }
        return;
      }
      if (!['ArrowLeft', 'ArrowRight'].includes(event.key)) return;
      const forward = (event.key === 'ArrowRight') !== (getComputedStyle(root).direction === 'rtl');
      if (button) {
        event.preventDefault(); const index = list.indexOf(button.closest('.k-chip')) + (forward ? 1 : -1);
        if (index >= 0) (list[index]?.querySelector('button') || input).focus();
      } else if (event.target === input && !forward && input.selectionStart === 0 && input.selectionEnd === 0 && list.length) {
        event.preventDefault(); list[list.length - 1].querySelector('button').focus();
      }
    });
    root.addEventListener('click', event => {
      const button = event.target.closest('.k-chip-x');
      if (button && root.contains(button)) remove(button.closest('.k-chip'), true);
      else if (event.target === root) input.focus();
    });
  });
})();
