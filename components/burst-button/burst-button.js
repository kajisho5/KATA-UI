// KATA Burst Button — sparks from the point of the click.
document.querySelectorAll('[data-burst]').forEach(function (wrap) {
  var canvas = wrap.querySelector('canvas');
  var btn = wrap.querySelector('.k-burst-btn');
  var ctx = canvas.getContext('2d');
  var DPR = Math.min(3, window.devicePixelRatio || 1);
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var cs = getComputedStyle(wrap);
  var COLORS = ['--k-accent', '--k-ink', '--k-zinc-400'].map(function (v) { return cs.getPropertyValue(v).trim(); }).filter(Boolean);
  var parts = [], raf = null, W = 0, H = 0;
  function size() { W = wrap.offsetWidth + 180; H = wrap.offsetHeight + 140; canvas.width = W * DPR; canvas.height = H * DPR; ctx.setTransform(DPR, 0, 0, DPR, 0, 0); }
  function fire(cx, cy) {
    if (reduced) return;
    size();
    var r = wrap.getBoundingClientRect();
    var ox = cx != null ? cx - r.left + 90 : W / 2;
    var oy = cy != null ? cy - r.top + 70 : H / 2;
    for (var i = 0; i < 30; i++) {
      var a = Math.PI * 2 * Math.random();
      var sp = 1.4 + Math.random() * 4.4;
      parts.push({ x: ox, y: oy, vx: Math.cos(a) * sp, vy: Math.sin(a) * sp - .8, life: 1, c: COLORS[i % COLORS.length], s: 2 + Math.random() * 2.6 });
    }
    if (!raf) tick();
  }
  function tick() {
    ctx.clearRect(0, 0, W, H);
    parts = parts.filter(function (p) { return p.life > 0; });
    parts.forEach(function (p) {
      p.vy += .11; p.vx *= .985; p.vy *= .985;
      p.x += p.vx; p.y += p.vy; p.life -= .02;
      ctx.globalAlpha = Math.max(0, p.life);
      ctx.fillStyle = p.c;
      ctx.beginPath(); ctx.arc(p.x, p.y, p.s, 0, 7); ctx.fill();
    });
    ctx.globalAlpha = 1;
    raf = parts.length ? requestAnimationFrame(tick) : null;
  }
  btn.addEventListener('click', function (e) { fire(e.clientX, e.clientY); });
  if ('IntersectionObserver' in window && !reduced) {
    var io = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { setTimeout(function () { fire(); }, 450); io.disconnect(); } }, { threshold: .6 });
    io.observe(wrap);
  }
  size();
});
