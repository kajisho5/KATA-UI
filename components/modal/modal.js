const dlg = document.querySelector('[data-modal]');
document.querySelector('[data-modal-open]').addEventListener('click', () => dlg.showModal());
dlg.querySelectorAll('[data-modal-close]').forEach(b => b.addEventListener('click', () => dlg.close()));
