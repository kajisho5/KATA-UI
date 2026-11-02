// KATA Gravity Playground — circles in chip clothing; grab and fling.
document.querySelectorAll('[data-grav]').forEach(function (stage) {
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var bodies = [];
  stage.querySelectorAll('.k-grav-chip').forEach(function (el, i) {
    var r = Math.max(el.offsetWidth, el.offsetHeight) / 2;
    bodies.push({ el: el, x: 30 + (i * 67) % Math.max(120, stage.clientWidth - 90), y: 16 + (i % 4) * 34, vx: 0, vy: 0, r: r, held: false });
  });
  var drag = null, last = null;
  bodies.forEach(function (b) {
    b.el.style.left = '0px'; b.el.style.top = '0px';
    b.el.addEventListener('pointerdown', function (e) {
      drag = b; last = { x: e.clientX, y: e.clientY, t: performance.now() };
      b.held = true; b.vx = 0; b.vy = 0;
      b.el.setPointerCapture(e.pointerId);
    });
    b.el.addEventListener('pointermove', function (e) {
      if (drag !== b) return;
      var now = performance.now();
      var rect = stage.getBoundingClientRect();
      b.x = e.clientX - rect.left; b.y = e.clientY - rect.top;
      var dt = Math.max(1, now - last.t);
      b.vx = (e.clientX - last.x) / dt * 16; b.vy = (e.clientY - last.y) / dt * 16;
      last = { x: e.clientX, y: e.clientY, t: now };
    });
    function release() { if (drag === b) { drag = null; b.held = false; } }
    b.el.addEventListener('pointerup', release);
    b.el.addEventListener('pointercancel', release);
  });
  function tick() {
    var W = stage.clientWidth, H = stage.clientHeight;
    bodies.forEach(function (b) {
      if (!b.held) {
        b.vy += .45;
        b.x += b.vx; b.y += b.vy;
        b.vx *= .999; b.vy *= .999;
        if (b.x < b.r) { b.x = b.r; b.vx = Math.abs(b.vx) * .5; }
        if (b.x > W - b.r) { b.x = W - b.r; b.vx = -Math.abs(b.vx) * .5; }
        if (b.y < b.el.offsetHeight / 2) { b.y = b.el.offsetHeight / 2; b.vy = Math.abs(b.vy) * .5; }
        if (b.y > H - b.el.offsetHeight / 2) { b.y = H - b.el.offsetHeight / 2; b.vy = -Math.abs(b.vy) * .42; b.vx *= .92; if (Math.abs(b.vy) < .6) b.vy = 0; }
      }
      b.el.style.transform = 'translate(' + (b.x - b.el.offsetWidth / 2) + 'px,' + (b.y - b.el.offsetHeight / 2) + 'px)';
    });
    for (var i = 0; i < bodies.length; i++) for (var j = i + 1; j < bodies.length; j++) {
      var a = bodies[i], c = bodies[j];
      var dx = c.x - a.x, dy = c.y - a.y;
      var rr = (a.el.offsetWidth + c.el.offsetWidth) / 4.4;
      var d2 = dx * dx + dy * dy;
      if (d2 > 0 && d2 < rr * rr) {
        var d = Math.sqrt(d2), push = (rr - d) / 2;
        var nx = dx / d, ny = dy / d;
        if (!a.held) { a.x -= nx * push; a.y -= ny * push; }
        if (!c.held) { c.x += nx * push; c.y += ny * push; }
      }
    }
    requestAnimationFrame(tick);
  }
  if (reduced) {
    bodies.forEach(function (b, i) { b.x = 40 + i * 62; b.y = stage.clientHeight - 24; b.el.style.transform = 'translate(' + (b.x - b.el.offsetWidth / 2) + 'px,' + (b.y - b.el.offsetHeight / 2) + 'px)'; });
  } else { requestAnimationFrame(tick); }
});
