const cmdDlg = document.querySelector('[data-command]');
const cmdInput = cmdDlg.querySelector('[data-command-input]');
const cmdItems = [...cmdDlg.querySelectorAll('[data-cmd-item]')];
const cmdEmpty = cmdDlg.querySelector('[data-command-empty]');
let cmdActive = 0;
function openCommand() { cmdDlg.showModal(); cmdInput.value = ''; filterCmd(''); cmdInput.focus(); }
function setActiveCmd(i) {
  cmdActive = Math.max(0, Math.min(i, cmdItems.filter(it => it.offsetParent !== null).length - 1));
  let n = -1;
  cmdItems.forEach(it => { const vis = it.offsetParent !== null; if (vis) n++; it.classList.toggle('active', vis && n === cmdActive); });
}
function filterCmd(q) {
  let any = false;
  cmdItems.forEach(it => { const hit = it.textContent.toLowerCase().includes(q.toLowerCase()); it.parentElement.style.display = hit ? '' : 'none'; if (hit) any = true; });
  cmdEmpty.style.display = any ? 'none' : '';
  setActiveCmd(0);
}
document.querySelector('[data-command-open]').addEventListener('click', openCommand);
document.addEventListener('keydown', e => {
  if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); if (!cmdDlg.open) openCommand(); }
});
cmdInput.addEventListener('input', () => filterCmd(cmdInput.value));
cmdInput.addEventListener('keydown', e => {
  if (e.key === 'ArrowDown') { e.preventDefault(); setActiveCmd(cmdActive + 1); }
  if (e.key === 'ArrowUp') { e.preventDefault(); setActiveCmd(cmdActive - 1); }
  if (e.key === 'Enter') { const vis = cmdItems.filter(it => it.offsetParent !== null); if (vis[cmdActive]) cmdDlg.close(); }
});
cmdItems.forEach(it => it.addEventListener('click', () => cmdDlg.close()));
