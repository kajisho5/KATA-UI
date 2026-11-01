document.querySelectorAll('[data-tabs]').forEach(tabs => {
  const thumb = tabs.querySelector('.thumb');
  const pane = tabs.parentElement.querySelector('[data-tabpane]');
  const btns = [...tabs.querySelectorAll('button')];
  const PANES = ['Overview panel — the essentials of the project live here.','Details panel — labor, day rates and travel, itemized.','History panel — created, edited and sent.'];
  function setTab(i){
    btns.forEach((b, j) => b.classList.toggle('on', j === i));
    thumb.style.left = btns[i].offsetLeft + 'px';
    thumb.style.width = btns[i].offsetWidth + 'px';
    if (pane) pane.textContent = PANES[i];
  }
  btns.forEach((b, i) => b.addEventListener('click', () => setTab(i)));
  setTab(0);
});
