const hdrBtn = document.querySelector('[data-hdr-btn]');
const hdrPanel = document.querySelector('[data-hdr-panel]');
hdrBtn.addEventListener('click', () => {
  const open = hdrPanel.classList.toggle('open');
  hdrBtn.setAttribute('aria-expanded', String(open));
});
