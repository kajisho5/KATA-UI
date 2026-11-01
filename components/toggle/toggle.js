document.querySelectorAll('.k-tgl').forEach(btn => {
  btn.addEventListener('click', () => {
    btn.setAttribute('aria-pressed', String(btn.getAttribute('aria-pressed') !== 'true'));
  });
});
