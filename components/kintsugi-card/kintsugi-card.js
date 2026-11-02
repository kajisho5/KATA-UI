// KATA Kintsugi Card — the veins draw themselves, gold over glow.
document.querySelectorAll('[data-kin]').forEach(function (card) {
  var canvas = card.querySelector('canvas');
  var ctx = canvas.getContext('2d');
  var DPR = Math.min(3, window.devicePixelRatio || 1);
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var cs = getComputedStyle(card);
  var GOLD = cs.getPropertyValue('--k-yamabuki').trim();
  var GLOW = cs.getPropertyValue('--k-yamabuki').trim();
  var CRACKS = [
    [[.06, .1], [.2, .3], [.3, .34], [.44, .52], [.52, .6]],
    [[.44, .52], [.5, .72], [.47, .95]],
    [[.3, .34], [.34, .12], [.42, .02]],
    [[.52, .6], [.68, .66], [.84, .6], [.97, .72]],
    [[.68, .66], [.74, .86], [.72, 1.02]]
  ];
  var W, H;
  function size() { W = card.clientWidth; H = card.clientHeight; canvas.width = W * DPR; canvas.height = H * DPR; ctx.setTransform(DPR, 0, 0, DPR, 0, 0); }
  function draw(t) {
    ctx.clearRect(0, 0, W, H);
    CRACKS.forEach(function (line) {
      var total = line.length - 1;
      var upto = t * total;
      [5.5, 1.8].forEach(function (wdt, pass) {
        ctx.beginPath();
        ctx.strokeStyle = pass === 0 ? GLOW : GOLD;
        ctx.globalAlpha = pass === 0 ? .5 : 1;
        ctx.lineWidth = wdt;
        ctx.lineJoin = 'round';
        for (var i = 0; i < Math.floor(upto); i++) {
          var a = line[i], b = line[i + 1];
          if (i === 0) ctx.moveTo(a[0] * W, a[1] * H);
          ctx.lineTo(b[0] * W, b[1] * H);
        }
        var f = upto - Math.floor(upto);
        if (f > 0 && Math.floor(upto) < total) {
          var a2 = line[Math.floor(upto)], b2 = line[Math.floor(upto) + 1];
          if (Math.floor(upto) === 0) ctx.moveTo(a2[0] * W, a2[1] * H);
          ctx.lineTo((a2[0] + (b2[0] - a2[0]) * f) * W, (a2[1] + (b2[1] - a2[1]) * f) * H);
        }
        ctx.stroke();
      });
    });
    ctx.globalAlpha = 1;
  }
  var start = null;
  function mend(ts) {
    if (!start) start = ts;
    var t = Math.min(1, (ts - start) / 1100);
    draw(t);
    if (t < 1) requestAnimationFrame(mend);
  }
  function run() { size(); if (reduced) { draw(1); } else { start = null; requestAnimationFrame(mend); } }
  card.addEventListener('pointerenter', run);
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { run(); io.disconnect(); } }, { threshold: .4 });
    io.observe(card);
  } else { run(); }
  size(); draw(reduced ? 1 : 0);
});
