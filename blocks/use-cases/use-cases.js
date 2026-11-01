const ucRows = [...document.querySelectorAll('[data-uc-row]')];
const ucScenes = [...document.querySelectorAll('[data-uc-scene]')];
ucRows.forEach((row, i) => {
  row.addEventListener('click', () => {
    ucRows.forEach((r, j) => {
      r.classList.toggle('open', j === i);
      r.setAttribute('aria-expanded', String(j === i));
    });
    ucScenes.forEach((sc, j) => { sc.hidden = j !== i; });
  });
});
