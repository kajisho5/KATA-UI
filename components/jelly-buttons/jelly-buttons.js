// KATA Jelly Buttons — a full wobble on every press.
(function () {
  'use strict';
  document.querySelectorAll('.k-jelly').forEach(function (button) {
    if (button.dataset.kataReady) return;
    button.dataset.kataReady = 'true';
    let timer;
    function finish() { clearTimeout(timer); button.classList.remove('squish'); }
    button.addEventListener('click', function () {
      finish();
      void button.offsetWidth;
      button.classList.add('squish');
      const style = getComputedStyle(button);
      const ms = value => Math.max(...value.split(',').map(part => parseFloat(part) * (part.trim().endsWith('ms') ? 1 : 1000)));
      const duration = ms(style.animationDuration);
      if (style.animationName === 'none' || duration === 0) { finish(); return; }
      // No end event is guaranteed after cancellation, removal, or a zero-duration override.
      timer = setTimeout(finish, duration + Math.max(0, ms(style.animationDelay)) + 50);
    });
    button.addEventListener('animationend', function (event) { if (event.target === button) finish(); });
    button.addEventListener('animationcancel', function (event) { if (event.target === button) finish(); });
  });
})();
