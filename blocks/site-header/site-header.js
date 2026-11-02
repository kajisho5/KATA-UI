const hdrBtn = document.querySelector('[data-hdr-btn]');
const hdrPanel = document.querySelector('[data-hdr-panel]');
if (hdrBtn && hdrPanel) hdrBtn.addEventListener('click', () => {
  const open = hdrPanel.classList.toggle('open');
  hdrBtn.setAttribute('aria-expanded', String(open));
});
