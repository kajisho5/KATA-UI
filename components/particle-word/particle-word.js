// KATA Particle Word — samples a word into points; each point gets
// a spring home and a healthy fear of the cursor.
document.querySelectorAll('[data-pw]').forEach(function (stage) {
  var canvas = stage.querySelector('canvas');
  var ctx = canvas.getContext('2d');
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var W = 0, H = 0, parts = [], mouse = { x: -9999, y: -9999 };
  var accent = getComputedStyle(stage).getPropertyValue('--k-accent').trim() || '#0e9594';
  var paper = getComputedStyle(stage).getPropertyValue('--k-on-color').trim() || '#ffffff';
  function targets(word) {
    var off = document.createElement('canvas');
    off.width = W; off.height = H;
    var o = off.getContext('2d');
    o.fillStyle = '#fff';
    o.font = '700 ' + Math.min(150, W / Math.max(2.2, word.length * 0.62)) + 'px Inter, sans-serif';
    o.textAlign = 'center'; o.textBaseline = 'middle';
    o.fillText(word, W / 2, H / 2 + 4);
    var data = o.getImageData(0, 0, W, H).data;
    var pts = [], step = 5;
    for (var y = 0; y < H; y += step) for (var x = 0; x < W; x += step)
      if (data[(y * W + x) * 4 + 3] > 128) pts.push({ x: x, y: y });
    if (pts.length > 1500) { pts = pts.filter(function (_, i) { return i % 2 === 0; }); }
    return pts;
  }
  function seed(word) {
    var pts = targets(word);
    while (parts.length < pts.length) parts.push({ x: Math.random() * W, y: Math.random() * H, vx: 0, vy: 0, c: Math.random() < .22 ? accent : paper });
    parts.length = pts.length;
    parts.forEach(function (p, i) { p.hx = pts[i].x; p.hy = pts[i].y; if (reduced) { p.x = p.hx; p.y = p.hy; } });
  }
  function frame() {
    ctx.clearRect(0, 0, W, H);
    parts.forEach(function (p) {
      var dx = mouse.x - p.x, dy = mouse.y - p.y;
      var d2 = dx * dx + dy * dy;
      if (d2 < 4900) { var d = Math.sqrt(d2) || 1; var f = (70 - d) / 70 * 2.6; p.vx -= dx / d * f; p.vy -= dy / d * f; }
      p.vx += (p.hx - p.x) * 0.028;
      p.vy += (p.hy - p.y) * 0.028;
      p.vx *= 0.86; p.vy *= 0.86;
      p.x += p.vx; p.y += p.vy;
      ctx.fillStyle = p.c;
      ctx.fillRect(p.x, p.y, 2.2, 2.2);
    });
    if (!reduced) requestAnimationFrame(frame);
  }
  function resize() {
    W = canvas.clientWidth; H = canvas.clientHeight;
    canvas.width = W; canvas.height = H;
    seed(stage.getAttribute('data-word') || 'KATA');
    if (reduced) frame();
  }
  stage.querySelectorAll('[data-pw-word]').forEach(function (b) {
    b.addEventListener('click', function () {
      stage.querySelectorAll('[data-pw-word]').forEach(function (x) { x.classList.remove('on'); });
      b.classList.add('on');
      stage.setAttribute('data-word', b.getAttribute('data-pw-word'));
      seed(b.getAttribute('data-pw-word'));
    });
  });
  canvas.addEventListener('pointermove', function (e) {
    var r = canvas.getBoundingClientRect();
    mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top;
  });
  canvas.addEventListener('pointerleave', function () { mouse.x = -9999; mouse.y = -9999; });
  resize();
  window.addEventListener('resize', resize);
  if (!reduced) requestAnimationFrame(frame);
});
