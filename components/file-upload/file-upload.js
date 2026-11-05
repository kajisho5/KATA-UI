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
  function size(bytes) {
    return bytes > 1048576 ? (bytes / 1048576).toFixed(1) + ' MB' : Math.max(1, Math.round(bytes / 1024)) + ' KB';
  }

  document.querySelectorAll('[data-upload]').forEach(root => {
    if (root.dataset.kataReady) return;
    const input = root.querySelector('input[type="file"]');
    const zone = root.querySelector('.k-up-zone');
    const list = root.querySelector('[data-up-list]');
    if (!input || !zone || !list) return;
    root.dataset.kataReady = 'true';
    identify(root, 'kata-upload'); identify(input, 'kata-upload-input');
    // A hidden input cannot take focus; the visually hidden input keeps keyboard browsing.
    input.hidden = false;
    input.classList.add('k-up-in');
    const status = document.createElement('span');
    status.className = 'k-up-status'; status.setAttribute('role', 'status');
    identify(status, 'kata-upload-status'); root.append(status);
    let depth = 0;

    const nameOf = item => (item.querySelector('.nm')?.textContent || '').trim();
    function prepare(item) {
      const button = item.querySelector('.rm');
      if (!button) return;
      button.type = 'button';
      button.setAttribute('aria-label', 'Remove ' + nameOf(item));
    }
    list.querySelectorAll('.k-up-item').forEach(prepare);

    function add(files) {
      const added = [...files];
      if (!added.length) return;
      added.forEach(file => {
        const item = document.createElement('li'); item.className = 'k-up-item';
        const icon = document.createElement('span'); icon.className = 'fi';
        // Icons are application-owned markup; file names only use textContent.
        icon.innerHTML = list.dataset.icon || '';
        const name = document.createElement('span'); name.className = 'nm'; name.textContent = file.name;
        const bytes = document.createElement('span'); bytes.className = 'sz'; bytes.textContent = size(file.size);
        const button = document.createElement('button'); button.className = 'rm'; button.type = 'button';
        if (list.dataset.rmIcon) button.innerHTML = list.dataset.rmIcon; else button.textContent = '×';
        item.append(icon, name, bytes, button); prepare(item); list.append(item);
      });
      const names = added.map(file => file.name);
      status.textContent = (names.length === 1 ? 'Added ' : 'Added ' + names.length + ' files: ') + names.join(', ') + '.';
      root.dispatchEvent(new CustomEvent('kata-file-upload-add', { bubbles: true, detail: { files: added } }));
    }
    function remove(item) {
      const items = [...list.querySelectorAll('.k-up-item')], index = items.indexOf(item), name = nameOf(item);
      item.remove();
      const next = list.querySelectorAll('.k-up-item')[Math.min(index, items.length - 2)];
      (next?.querySelector('.rm') || input).focus();
      status.textContent = 'Removed ' + name + '.';
      root.dispatchEvent(new CustomEvent('kata-file-upload-remove', { bubbles: true, detail: { name } }));
    }

    input.addEventListener('change', () => { add(input.files); input.value = ''; });
    list.addEventListener('click', event => {
      const button = event.target.closest('.rm');
      if (button && list.contains(button)) remove(button.closest('.k-up-item'));
    });
    // A depth count keeps child elements from flickering this zone's drag state.
    zone.addEventListener('dragenter', event => { event.preventDefault(); depth++; zone.classList.add('drag'); });
    zone.addEventListener('dragover', event => { event.preventDefault(); });
    zone.addEventListener('dragleave', () => { depth = Math.max(0, depth - 1); if (!depth) zone.classList.remove('drag'); });
    zone.addEventListener('drop', event => {
      event.preventDefault(); depth = 0; zone.classList.remove('drag');
      if (event.dataTransfer) add(event.dataTransfer.files);
    });
  });
})();
