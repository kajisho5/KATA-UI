// KATA Scrollspy — IntersectionObserver against the real scroll container.
document.querySelectorAll('[data-spy]').forEach(function (root) {
  var body = root.querySelector('.k-spy-body');
  var links = {};
  root.querySelectorAll('nav a[href^="#"]').forEach(function (a) { links[a.getAttribute('href').slice(1)] = a; });
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (!en.isIntersecting) return;
      Object.values(links).forEach(function (a) { a.classList.remove('on'); a.removeAttribute('aria-current'); });
      var a = links[en.target.id];
      if (a) { a.classList.add('on'); a.setAttribute('aria-current', 'location'); }
    });
  }, { root: body, rootMargin: '0px 0px -62% 0px', threshold: 0 });
  body.querySelectorAll('section[id]').forEach(function (s) { io.observe(s); });
});
