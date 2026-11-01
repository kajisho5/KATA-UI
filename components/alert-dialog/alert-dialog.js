const alertDlg = document.querySelector('[data-alert-dialog]');
document.querySelector('[data-alert-open]').addEventListener('click', () => alertDlg.showModal());
alertDlg.querySelectorAll('[data-alert-close]').forEach(b => b.addEventListener('click', () => alertDlg.close()));
alertDlg.addEventListener('cancel', e => e.preventDefault());
