// Field: links the hint and, while the field is invalid, the error to the control
// with aria-describedby, and keeps aria-invalid in step with data-invalid. Existing
// IDs are kept; missing ones are generated, so a pasted sample can appear twice.
// When data-invalid is added after load (for example on submit), the error gets
// role="alert" so it is announced once; it is not announced while typing.
(() => {
  let nextId = 0;
  function ensureId(element, suffix) {
    if (element.id) return element.id;
    let id;
    do { id = `kata-field-${++nextId}-${suffix}`; } while (document.getElementById(id));
    element.id = id;
    return id;
  }

  function sync(field, announce) {
    const control = field.querySelector('input, textarea, select');
    if (!control) return;
    const label = field.querySelector('label');
    if (label && !label.contains(control) && !label.htmlFor) label.htmlFor = ensureId(control, 'control');
    const hint = field.querySelector('.hint');
    const err = field.querySelector('.err');
    const invalid = field.hasAttribute('data-invalid');
    const own = [hint, err].filter(Boolean).map(el => el.id).filter(Boolean);
    const ids = (control.getAttribute('aria-describedby') || '').split(/\s+/).filter(id => id && !own.includes(id));
    if (hint) ids.push(ensureId(hint, 'hint'));
    if (err && invalid) ids.push(ensureId(err, 'error'));
    if (ids.length) control.setAttribute('aria-describedby', ids.join(' '));
    else control.removeAttribute('aria-describedby');
    if (invalid) control.setAttribute('aria-invalid', 'true');
    else control.removeAttribute('aria-invalid');
    if (err) {
      if (invalid && announce) err.setAttribute('role', 'alert');
      else if (!invalid) err.removeAttribute('role');
    }
  }

  document.querySelectorAll('.k-field').forEach(field => {
    if (field.hasAttribute('data-kata-ready')) return;
    field.setAttribute('data-kata-ready', '');
    sync(field, false);
    new MutationObserver(() => sync(field, true)).observe(field, { attributes: true, attributeFilter: ['data-invalid'] });
  });
})();
