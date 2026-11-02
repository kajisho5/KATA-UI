document.querySelectorAll('[data-modal]').forEach(dlg => {
  dlg.querySelectorAll('[data-modal-close]').forEach(b => b.addEventListener('click', () => dlg.close()));
});
document.querySelectorAll('[data-modal-open]').forEach(btn => {
  btn.addEventListener('click', () => {
    const all = [...document.querySelectorAll('[data-modal]')];
    const dlg = all.find(d => btn.compareDocumentPosition(d) & Node.DOCUMENT_POSITION_FOLLOWING) || all[0];
    if (dlg) dlg.showModal();
  });
});
