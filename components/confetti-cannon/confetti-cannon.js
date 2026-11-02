// KATA Confetti Cannon — canvas pieces, token colors, real gravity.
document.querySelectorAll('[data-conf]').forEach(function (stage) {
  var canvas = stage.querySelector('canvas');
  var ctx = canvas.getContext('2d');
  var DPR = Math.min(3, window.devicePixelRatio || 1);
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var cs = getComputedStyle(stage);
  var COLORS = ['--k-accent', '--k-on-color', '--k-zinc-400', '--k-yamabuki-ink'].map(function (v) { return cs.getPropertyValue(v).trim(); }).filter(Boolean);
  var pieces = [], raf = null, W = 0, H = 0;
  function size() { W = stage.clientWidth; H = stage.clientHeight; canvas.width = W * DPR; canvas.height = H * DPR; ctx.setTransform(DPR, 0, 0, DPR, 0, 0); }
  function burst() {
    if (reduced) return;
    size();
    [0, W].forEach(function (ox, side) {
      var dir = side === 0 ? 1 : -1;
      for (var i = 0; i < 70; i++) {
        var a = (-58 - Math.random() * 38) * Math.PI / 180;
        var sp = 9 + Math.random() * 9;
        pieces.push({ x: ox, y: H + 4, vx: Math.cos(a) * sp * dir, vy: Math.sin(a) * sp, w: 5 + Math.random() * 5, h: 3 + Math.random() * 5, rot: Math.random() * Math.PI, vr: (Math.random() - .5) * .3, c: COLORS[i % COLORS.length], life: 1 });
      }
    });
    if (!raf) tick();
  }
  function tick() {
    ctx.clearRect(0, 0, W, H);
    pieces = pieces.filter(function (p) { return p.life > 0 && p.y < H + 30; });
    pieces.forEach(function (p) {
      p.vy += .22; p.vx *= .99; p.vy *= .995;
      p.x += p.vx; p.y += p.vy; p.rot += p.vr;
      if (p.y > H - 90) p.life -= .02;
      ctx.save();
      ctx.globalAlpha = Math.max(0, Math.min(1, p.life));
      ctx.translate(p.x, p.y); ctx.rotate(p.rot);
      ctx.fillStyle = p.c;
      ctx.fillRect(-p.w / 2, -p.h / 2, p.w, p.h * (0.4 + Math.abs(Math.sin(p.rot * 2)) * .6));
      ctx.restore();
    });
    raf = pieces.length ? requestAnimationFrame(tick) : null;
    if (!raf) ctx.clearRect(0, 0, W, H);
  }
  stage.querySelector('[data-conf-fire]').addEventListener('click', burst);
  size();
  if ('IntersectionObserver' in window && !reduced) {
    var io = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { setTimeout(burst, 350); io.disconnect(); } }, { threshold: .5 });
    io.observe(stage);
  }
});
