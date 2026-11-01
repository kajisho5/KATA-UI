const tagsBox = document.querySelector('[data-tags]');
const tagsIn = tagsBox.querySelector('.k-tags-in');
const X_SVG = tagsBox.dataset.x;
function tagAdd(text) {
  const val = text.trim().replace(/,$/, '');
  if (!val) return;
  const exists = [...tagsBox.querySelectorAll('.k-chip')].some(c => c.dataset.tag === val.toLowerCase());
  if (exists) return;
  const chip = document.createElement('span');
  chip.className = 'k-chip';
  chip.dataset.tag = val.toLowerCase();
  chip.innerHTML = `<span></span><button class="k-chip-x" type="button" aria-label="Remove tag ${val}">${X_SVG}</button>`;
  chip.querySelector('span').textContent = val;
  chip.querySelector('.k-chip-x').addEventListener('click', () => chip.remove());
  tagsBox.insertBefore(chip, tagsIn);
}
tagsIn.addEventListener('keydown', e => {
  if (e.key === 'Enter' || e.key === ',') { e.preventDefault(); tagAdd(tagsIn.value); tagsIn.value = ''; }
  if (e.key === 'Backspace' && !tagsIn.value) {
    const chips = tagsBox.querySelectorAll('.k-chip');
    if (chips.length) chips[chips.length - 1].remove();
  }
});
tagsIn.addEventListener('blur', () => { tagAdd(tagsIn.value); tagsIn.value = ''; });
tagsBox.querySelectorAll('.k-chip-x').forEach(b => b.addEventListener('click', () => b.closest('.k-chip').remove()));
tagsBox.addEventListener('click', e => { if (e.target === tagsBox) tagsIn.focus(); });
