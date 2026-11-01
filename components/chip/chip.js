document.querySelectorAll('.k-chip-x').forEach(btn => {
  btn.addEventListener('click', () => btn.closest('.k-chip').remove());
});
