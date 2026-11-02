// KATA Kaleidoscope — one stroke, ten reflections.
document.querySelectorAll('[data-kal]').forEach(function (stage) {
  var canvas = stage.querySelector('canvas');
  var ctx = canvas.getContext('2d');
  var DPR = Math.min(3, window.devicePixelRatio || 1);
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var SEG = 10, W, H, cx, cy, drawing = false, prev = null, auto = !reduced, t = 0;
  var paper = getComputedStyle(stage).getPropertyValue('--k-on-color').trim() || '#ffffff';
  var accent = getComputedStyle(stage).getPropertyValue('--k-accent').trim() || '#0e9594';
  function size() {
    W = canvas.clientWidth; H = canvas.clientHeight;
    canvas.width = W * DPR; canvas.height = H * DPR; ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    cx = W / 2; cy = H / 2;
    ctx.fillStyle = '#09090b'; ctx.fillRect(0, 0, W, H);
  }
  function stroke(a, b, color) {
    ctx.strokeStyle = color; ctx.lineWidth = 2.4; ctx.lineCap = 'round';
    for (var i = 0; i < SEG; i++) {
      var ang = (Math.PI * 2 / SEG) * i;
      var flip = i % 2 === 1;
      [false, true].forEach(function (mirror) {
        var s = (flip ? -1 : 1) * (mirror ? -1 : 1);
        ctx.beginPath();
        ctx.moveTo(cx + rot(a, ang, s).x, cy + rot(a, ang, s).y);
        ctx.lineTo(cx + rot(b, ang, s).x, cy + rot(b, ang, s).y);
        ctx.stroke();
      });
    }
  }
  function rot(p, ang, sx) {
    var dx = (p.x - cx) * sx, dy = p.y - cy;
    return { x: dx * Math.cos(ang) - dy * Math.sin(ang), y: dx * Math.sin(ang) + dy * Math.cos(ang) };
  }
  function autoPen() {
    if (!auto) return;
    t += .016;
    var p = { x: cx + Math.sin(t * 1.9) * W * .3, y: cy + Math.sin(t * 2.7) * H * .32 };
    if (prev) stroke(prev, p, Math.floor(t * 2) % 2 ? paper : accent);
    prev = p;
    requestAnimationFrame(autoPen);
  }
  function pos(e) { var r = canvas.getBoundingClientRect(); return { x: e.clientX - r.left, y: e.clientY - r.top }; }
  canvas.addEventListener('pointerdown', function (e) { auto = false; drawing = true; prev = pos(e); canvas.setPointerCapture(e.pointerId); });
  canvas.addEventListener('pointermove', function (e) { if (!drawing) return; var p = pos(e); stroke(prev, p, paper); prev = p; });
  canvas.addEventListener('pointerup', function () { drawing = false; });
  stage.querySelector('[data-kal-clear]').addEventListener('click', function () { ctx.fillStyle = '#09090b'; ctx.fillRect(0, 0, W, H); });
  size();
  window.addEventListener('resize', size);
  if (!reduced) requestAnimationFrame(autoPen);
});
