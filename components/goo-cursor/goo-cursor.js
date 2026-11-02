// KATA Goo Cursor — a chain of lazy blobs under a goo filter.
document.querySelectorAll('[data-goo]').forEach(function (stage) {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var svgNS = 'http://www.w3.org/2000/svg';
  var svg = document.createElementNS(svgNS, 'svg');
  svg.setAttribute('width', '0'); svg.setAttribute('height', '0');
  svg.style.position = 'absolute';
  var filter = document.createElementNS(svgNS, 'filter');
  filter.setAttribute('id', 'k-goo-filter');
  var blur = document.createElementNS(svgNS, 'feGaussianBlur');
  blur.setAttribute('in', 'SourceGraphic'); blur.setAttribute('stdDeviation', '9');
  var matrix = document.createElementNS(svgNS, 'feColorMatrix');
  matrix.setAttribute('values', '1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 22 -11');
  filter.appendChild(blur); filter.appendChild(matrix);
  svg.appendChild(filter);
  stage.appendChild(svg);
  var field = stage.querySelector('.k-goo-field');
  field.style.filter = 'url(#k-goo-filter)';
  var SIZES = [44, 34, 27, 21, 16, 12];
  var blobs = SIZES.map(function (s, i) {
    var el = document.createElement('span');
    el.className = 'k-goo-b';
    el.style.width = s + 'px'; el.style.height = s + 'px';
    field.appendChild(el);
    return { el: el, x: stage.clientWidth / 2, y: stage.clientHeight / 2, ease: .34 - i * .045 };
  });
  var mouse = { x: stage.clientWidth / 2, y: stage.clientHeight / 2 };
  stage.addEventListener('pointermove', function (e) {
    var r = stage.getBoundingClientRect();
    mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top;
  });
  (function frame() {
    var tx = mouse.x, ty = mouse.y;
    blobs.forEach(function (b) {
      b.x += (tx - b.x) * b.ease;
      b.y += (ty - b.y) * b.ease;
      b.el.style.left = b.x + 'px';
      b.el.style.top = b.y + 'px';
      tx = b.x; ty = b.y;
    });
    requestAnimationFrame(frame);
  })();
});
