const up = document.querySelector('[data-upload]');
const upInput = up.querySelector('input[type="file"]');
const upZone = up.querySelector('.k-up-zone');
const upList = up.querySelector('[data-up-list]');
const FILE_SVG = upList.dataset.icon;
function upSize(n) {
  return n > 1048576 ? (n / 1048576).toFixed(1) + ' MB' : Math.max(1, Math.round(n / 1024)) + ' KB';
}
function upAdd(files) {
  [...files].forEach(f => {
    const li = document.createElement('li');
    li.className = 'k-up-item';
    li.innerHTML = `<span class="fi">${FILE_SVG}</span><span class="nm"></span><span class="sz">${upSize(f.size)}</span><button class="rm" type="button" aria-label="Remove file">✕</button>`;
    li.querySelector('.nm').textContent = f.name;
    li.querySelector('.rm').addEventListener('click', () => li.remove());
    upList.appendChild(li);
  });
}
upInput.addEventListener('change', () => { upAdd(upInput.files); upInput.value = ''; });
['dragenter', 'dragover'].forEach(ev => upZone.addEventListener(ev, e => { e.preventDefault(); upZone.classList.add('drag'); }));
['dragleave', 'drop'].forEach(ev => upZone.addEventListener(ev, e => { e.preventDefault(); upZone.classList.remove('drag'); }));
upZone.addEventListener('drop', e => upAdd(e.dataTransfer.files));
upList.querySelectorAll('.rm').forEach(b => b.addEventListener('click', () => b.closest('.k-up-item').remove()));
