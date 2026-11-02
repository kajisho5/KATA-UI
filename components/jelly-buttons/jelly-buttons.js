// KATA Jelly Buttons — a full wobble on every press.
document.querySelectorAll('.k-jelly').forEach(function (b) {
  b.addEventListener('click', function () {
    b.classList.remove('squish');
    void b.offsetWidth;
    b.classList.add('squish');
  });
  b.addEventListener('animationend', function () { b.classList.remove('squish'); });
});
