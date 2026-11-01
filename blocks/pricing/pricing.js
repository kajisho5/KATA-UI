const billSwitch = document.querySelector('[data-billing]');
billSwitch.addEventListener('change', () => {
  document.querySelectorAll('[data-m]').forEach(el => {
    el.textContent = billSwitch.checked ? el.dataset.y : el.dataset.m;
  });
});
