// KATA Kata Rain — columns of falling glyphs, taupe sky optional.
document.querySelectorAll('[data-rain]').forEach(function (stage) {
  var canvas = stage.querySelector('canvas');
  var ctx = canvas.getContext('2d');
  var DPR = Math.min(3, window.devicePixelRatio || 1);
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var GLYPHS = 'アカサタナハマヤラワイキシチニヒミリヲ0123456789';
  var W, H, cols, drops;
  var accent = getComputedStyle(stage).getPropertyValue('--k-accent').trim() || '#0e9594';
  function size() {
    W = canvas.clientWidth; H = canvas.clientHeight;
    canvas.width = W * DPR; canvas.height = H * DPR; ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    cols = Math.floor(W / 17);
    drops = [];
    for (var i = 0; i < cols; i++) drops.push({ y: Math.random() * -40, speed: .5 + Math.random() * 1.1 });
    ctx.fillStyle = '#09090b';
    ctx.fillRect(0, 0, W, H);
  }
  function draw() {
    ctx.fillStyle = 'rgba(9,9,11,.16)';
    ctx.fillRect(0, 0, W, H);
    ctx.font = '15px monospace';
    for (var i = 0; i < cols; i++) {
      var d = drops[i];
      var ch = GLYPHS[Math.floor(Math.random() * GLYPHS.length)];
      ctx.fillStyle = accent;
      ctx.fillText(ch, i * 17 + 2, d.y * 17);
      ctx.fillStyle = 'rgba(212,212,216,.5)';
      ctx.fillText(GLYPHS[Math.floor(Math.random() * GLYPHS.length)], i * 17 + 2, (d.y - 1) * 17);
      d.y += d.speed;
      if (d.y * 17 > H && Math.random() > .978) { d.y = Math.random() * -12; d.speed = .5 + Math.random() * 1.1; }
    }
  }
  size();
  window.addEventListener('resize', size);
  if (reduced) { for (var k = 0; k < 26; k++) draw(); }
  else { setInterval(draw, 52); }
});
