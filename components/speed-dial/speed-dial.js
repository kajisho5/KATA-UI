// KATA Speed Dial — open and shut; Escape shuts it from anywhere.
document.querySelectorAll('[data-dial]').forEach(function (el) {
  var main = el.querySelector('.main');
  main.addEventListener('click', function () {
    var open = el.classList.toggle('open');
    main.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && el.classList.contains('open')) {
      el.classList.remove('open');
      main.setAttribute('aria-expanded', 'false');
    }
  });
});
