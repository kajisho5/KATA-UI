// KATA Fireworks — rockets rise, burst, and rain sparks.
document.querySelectorAll('[data-fw]').forEach(function (stage) {
  var canvas = stage.querySelector('canvas');
  var ctx = canvas.getContext('2d');
  var DPR = Math.min(3, window.devicePixelRatio || 1);
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var cs = getComputedStyle(stage);
  var COLORS = ['--k-accent', '--k-on-color', '--k-yamabuki-ink', '--k-on-color'].map(function (v) { return cs.getPropertyValue(v).trim(); }).filter(Boolean);
  var W, H, rockets = [], sparks = [];
  function size() { W = canvas.clientWidth; H = canvas.clientHeight; canvas.width = W * DPR; canvas.height = H * DPR; ctx.setTransform(DPR, 0, 0, DPR, 0, 0); }
  function launch(tx, ty) {
    rockets.push({ x: tx != null ? tx : 40 + Math.random() * (W - 80), y: H, ty: ty != null ? ty : 40 + Math.random() * H * .45, vy: -(9.5 + Math.random() * 3), c: COLORS[Math.floor(Math.random() * COLORS.length)] });
  }
  function burst(r) {
    for (var i = 0; i < 96; i++) {
      var a = Math.PI * 2 * i / 96 + Math.random() * .1;
      var sp = 1.4 + Math.random() * 3.6;
      sparks.push({ x: r.x, y: r.ty, vx: Math.cos(a) * sp, vy: Math.sin(a) * sp, life: 1, c: Math.random() < .3 ? COLORS[1] : r.c });
    }
  }
  function tick() {
    ctx.fillStyle = 'rgba(9,9,11,.18)';
    ctx.fillRect(0, 0, W, H);
    rockets = rockets.filter(function (r) {
      r.y += r.vy; r.vy += .12;
      ctx.fillStyle = r.c; ctx.fillRect(r.x - 1, r.y, 2.4, 7);
      if (r.vy >= -1 || r.y <= r.ty) { burst(r); return false; }
      return true;
    });
    sparks = sparks.filter(function (s) { return s.life > 0; });
    ctx.globalCompositeOperation = 'lighter';
    sparks.forEach(function (s) {
      s.vy += .045; s.vx *= .985; s.vy *= .985;
      s.x += s.vx; s.y += s.vy; s.life -= .010;
      ctx.globalAlpha = Math.max(0, s.life);
      ctx.fillStyle = s.c;
      ctx.fillRect(s.x, s.y, 3, 3);
    });
    ctx.globalCompositeOperation = 'source-over';
    ctx.globalAlpha = 1;
    requestAnimationFrame(tick);
  }
  canvas.addEventListener('pointerdown', function (e) {
    var r = canvas.getBoundingClientRect();
    launch(e.clientX - r.left, e.clientY - r.top);
  });
  size();
  window.addEventListener('resize', size);
  if (!reduced) {
    launch(); setTimeout(launch, 500);
    setInterval(function () { if (rockets.length < 3 && Math.random() > .35) launch(); }, 1100);
    requestAnimationFrame(tick);
  } else {
    ctx.fillStyle = '#09090b'; ctx.fillRect(0, 0, W, H);
  }
});
