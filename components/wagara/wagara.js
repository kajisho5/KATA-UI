// KATA Wagara — the four patterns, drawn from their constructions.
document.querySelectorAll('[data-wag]').forEach(function (root) {
  var canvas = root.querySelector('canvas');
  var ctx = canvas.getContext('2d');
  var DPR = Math.min(3, window.devicePixelRatio || 1);
  var cap = root.querySelector('.k-wag-cap');
  var cs = getComputedStyle(root);
  var V = function (n) { return cs.getPropertyValue(n).trim(); };
  var TONES = [
    { bg: V('--k-bg'), fg: V('--k-ink'), mid: V('--k-zinc-400'), soft: V('--k-zinc-200'), name: 'Paper' },
    { bg: V('--k-zinc-950'), fg: V('--k-zinc-200'), mid: V('--k-zinc-500'), soft: V('--k-zinc-800'), name: 'Ink' },
    { bg: V('--k-zinc-950'), fg: V('--k-accent'), mid: V('--k-zinc-500'), soft: V('--k-zinc-800'), name: 'Night' }
  ];
  var CAPS = {
    seigaiha: 'Seigaiha — blue ocean waves. Concentric arcs, each row offset by half a fan; a wish for calm seas and a long life.',
    asanoha: 'Asanoha — the hemp leaf. Six-fold geometry from a hexagon\u2019s triangles; hemp grows fast and straight, so the pattern guards children.',
    shippo: 'Shippo — seven treasures. Equal circles overlapping by a quarter, each petal a treasure, the whole an unbroken wish for harmony.',
    ichimatsu: 'Ichimatsu — the checkered pattern named for the kabuki actor Sanogawa Ichimatsu. The nested band is the one the KATA mark wears.'
  };
  var pattern = 'seigaiha', tone = 0, W, H;
  function seigaiha(t) {
    var s = 30;
    var rows = Math.ceil(H / (s * .5)) + 2;
    for (var r = rows; r >= -1; r--) {
      var y = r * s * .5 + s * .5;
      var off = (r % 2) * s;
      for (var x = -s + off; x < W + s; x += s * 2) {
        for (var k = 4; k >= 1; k--) {
          ctx.beginPath();
          ctx.arc(x, y, s * k / 4, Math.PI, 0);
          ctx.closePath();
          ctx.fillStyle = k % 2 ? t.bg : t.soft;
          if (k === 4) ctx.fillStyle = t.bg;
          ctx.fill();
          ctx.strokeStyle = k % 2 ? t.fg : t.mid;
          ctx.lineWidth = 1.2;
          ctx.stroke();
        }
      }
    }
  }
  function asanoha(t) {
    var R = 25, dx = Math.sqrt(3) * R, dy = 1.5 * R;
    ctx.lineWidth = 1.1;
    var row = 0;
    for (var y = -R; y < H + R; y += dy, row++) {
      for (var x = -dx; x < W + dx; x += dx) {
        var cx = x + (row % 2 ? dx / 2 : 0), cy = y;
        var v = [];
        for (var k = 0; k < 6; k++) { var a = Math.PI / 3 * k - Math.PI / 2; v.push([cx + R * Math.cos(a), cy + R * Math.sin(a)]); }
        for (var k2 = 0; k2 < 6; k2++) {
          var A = v[k2], B = v[(k2 + 1) % 6];
          var mx = (A[0] + B[0] + cx) / 3, my = (A[1] + B[1] + cy) / 3;
          ctx.strokeStyle = t.mid;
          ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(A[0], A[1]); ctx.stroke();
          ctx.beginPath(); ctx.moveTo(A[0], A[1]); ctx.lineTo(B[0], B[1]); ctx.stroke();
          ctx.strokeStyle = t.fg;
          [[A, B], [B, [cx, cy]], [[cx, cy], A]].forEach(function (pr) {
            ctx.beginPath(); ctx.moveTo(mx, my); ctx.lineTo(pr[0][0], pr[0][1]); ctx.stroke();
          });
          var mAB = [(A[0] + B[0]) / 2, (A[1] + B[1]) / 2], mBc = [(B[0] + cx) / 2, (B[1] + cy) / 2], mCa = [(cx + A[0]) / 2, (cy + A[1]) / 2];
          ctx.beginPath(); ctx.moveTo(mAB[0], mAB[1]); ctx.lineTo(mBc[0], mBc[1]); ctx.lineTo(mCa[0], mCa[1]); ctx.closePath(); ctx.stroke();
        }
      }
    }
  }
  function shippo(t) {
    var R = 21;
    ctx.lineWidth = 1.2; ctx.strokeStyle = t.mid;
    for (var y = 0; y < H + R; y += R) for (var x = 0; x < W + R; x += R) {
      ctx.beginPath(); ctx.arc(x, y, R, 0, 7); ctx.stroke();
    }
    ctx.fillStyle = t.fg;
    for (var y2 = 0; y2 < H + R; y2 += R) for (var x2 = 0; x2 < W + R; x2 += R) {
      ctx.beginPath(); ctx.arc(x2, y2, 1.6, 0, 7); ctx.fill();
    }
  }
  function ichimatsu(t) {
    var s = 27;
    for (var y = 0; y < H - 40; y += s) for (var x = 0; x < W; x += s) {
      if (((x / s) + (y / s)) % 2 === 0) { ctx.fillStyle = t.fg; ctx.globalAlpha = .85; ctx.fillRect(x, y, s, s); }
    }
    ctx.globalAlpha = 1;
    var s2 = 6.75, y0 = H - 40;
    ctx.fillStyle = t.soft; ctx.fillRect(0, y0, W, 40);
    for (var yy = y0; yy < H; yy += s2) for (var xx = 0; xx < W; xx += s2) {
      if (((xx / s2) + ((yy - y0) / s2)) % 2 === 0) { ctx.fillStyle = t.fg; ctx.fillRect(xx, yy, s2, s2); }
    }
  }
  function draw() {
    var t = TONES[tone];
    W = canvas.clientWidth; H = canvas.clientHeight;
    canvas.width = W * DPR; canvas.height = H * DPR; ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    ctx.fillStyle = t.bg; ctx.fillRect(0, 0, W, H);
    ({ seigaiha: seigaiha, asanoha: asanoha, shippo: shippo, ichimatsu: ichimatsu })[pattern](t);
    cap.textContent = CAPS[pattern];
  }
  root.querySelectorAll('[data-wag-p]').forEach(function (b) {
    b.addEventListener('click', function () {
      root.querySelectorAll('[data-wag-p]').forEach(function (x) { x.classList.remove('on'); });
      b.classList.add('on');
      pattern = b.getAttribute('data-wag-p');
      draw();
    });
  });
  root.querySelector('[data-wag-tone]').addEventListener('click', function () { tone = (tone + 1) % TONES.length; this.textContent = 'Tone: ' + TONES[tone].name; draw(); });
  window.addEventListener('resize', draw);
  draw();
});
