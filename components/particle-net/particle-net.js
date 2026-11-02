// KATA Particle Net — drift, connect, gather at the cursor.
document.querySelectorAll('[data-net]').forEach(function (stage) {
  var canvas = stage.querySelector('canvas');
  var ctx = canvas.getContext('2d');
  var DPR = Math.min(3, window.devicePixelRatio || 1);
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var cs = getComputedStyle(stage);
  var INK = cs.getPropertyValue('--k-zinc-400').trim() || '#a1a1aa';
  var ACCENT = cs.getPropertyValue('--k-accent').trim() || '#0e9594';
  var W, H, pts = [], mouse = { x: -9999, y: -9999 };
  function size() {
    W = stage.clientWidth; H = stage.clientHeight;
    canvas.width = W * DPR; canvas.height = H * DPR; ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    var n = Math.min(78, Math.floor(W * H / 2600));
    pts = [];
    for (var i = 0; i < n; i++) pts.push({ x: Math.random() * W, y: Math.random() * H, vx: (Math.random() - .5) * .34, vy: (Math.random() - .5) * .34 });
  }
  function draw() {
    ctx.clearRect(0, 0, W, H);
    var i, j, p, q;
    for (i = 0; i < pts.length; i++) {
      p = pts[i];
      p.x += p.vx; p.y += p.vy;
      if (p.x < 0 || p.x > W) p.vx *= -1;
      if (p.y < 0 || p.y > H) p.vy *= -1;
      var dm = Math.hypot(mouse.x - p.x, mouse.y - p.y);
      if (dm < 130 && dm > 1) { p.x += (mouse.x - p.x) * .0016; p.y += (mouse.y - p.y) * .0016; }
    }
    for (i = 0; i < pts.length; i++) for (j = i + 1; j < pts.length; j++) {
      p = pts[i]; q = pts[j];
      var d = Math.hypot(p.x - q.x, p.y - q.y);
      if (d < 108) {
        ctx.strokeStyle = INK;
        ctx.globalAlpha = (1 - d / 108) * .42;
        ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(q.x, q.y); ctx.stroke();
      }
    }
    ctx.globalAlpha = 1;
    pts.forEach(function (p, i) {
      ctx.fillStyle = i % 9 === 0 ? ACCENT : INK;
      ctx.beginPath(); ctx.arc(p.x, p.y, 2, 0, 7); ctx.fill();
    });
  }
  function frame() { draw(); if (!reduced) requestAnimationFrame(frame); }
  stage.addEventListener('pointermove', function (e) {
    var r = stage.getBoundingClientRect();
    mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top;
  });
  stage.addEventListener('pointerleave', function () { mouse.x = -9999; mouse.y = -9999; });
  size();
  window.addEventListener('resize', size);
  frame();
});
