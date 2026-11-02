// KATA Wagara — twenty-two patterns, drawn from their constructions.
document.querySelectorAll('[data-wag]').forEach(function (root) {
  var canvas = root.querySelector('canvas');
  var ctx = canvas.getContext('2d');
  var DPR = Math.min(3, window.devicePixelRatio || 1);
  var cap = root.querySelector('.k-wag-cap');
  function tones() {
    var cs = getComputedStyle(root);
    var V = function (n) { return cs.getPropertyValue(n).trim(); };
    return [
      { bg: V('--k-bg'), fg: V('--k-ink'), mid: V('--k-zinc-400'), soft: V('--k-zinc-200'), name: 'Paper' },
      { bg: V('--k-zinc-950'), fg: V('--k-zinc-200'), mid: V('--k-zinc-500'), soft: V('--k-zinc-800'), name: 'Ink' },
      { bg: V('--k-zinc-950'), fg: V('--k-accent'), mid: V('--k-zinc-500'), soft: V('--k-zinc-800'), name: 'Night' }
    ];
  }
  var picked = null;
  function ambientDark() {
    var host = root.closest('[data-theme]');
    if (host) return host.getAttribute('data-theme') === 'dark';
    return !!(window.matchMedia && matchMedia('(prefers-color-scheme: dark)').matches);
  }
  function effTone() { return picked !== null ? picked : (ambientDark() ? 1 : 0); }
  var CAPS = {
    seigaiha: 'Seigaiha — blue ocean waves. Concentric arcs, each row offset by half a fan; a wish for calm seas and a long life.',
    asanoha: 'Asanoha — the hemp leaf. Six-fold geometry from a hexagon\u2019s triangles; hemp grows fast and straight, so the pattern guards children.',
    shippo: 'Shippo — seven treasures. Equal circles overlapping by a quarter, each petal a treasure, the whole an unbroken wish for harmony.',
    ichimatsu: 'Ichimatsu — the checkered pattern named for the kabuki actor Sanogawa Ichimatsu. The nested band is the one the KATA mark wears.',
    kikko: 'Kikko — the tortoiseshell. Hexagons from the turtle\u2019s shell; the tortoise lives ten thousand years, so the pattern is worn for a long life.',
    uroko: 'Uroko — scales. Overlapping triangles of fish and dragon scale; what sheds its skin sheds misfortune with it.',
    same: 'Samekomon — sharkskin. Dots riding the arcs of scales, dyed so fine it counted as plain cloth under Edo sumptuary law — luxury hiding in the dots.',
    yagasuri: 'Yagasuri — the arrow feather. An arrow once shot never returns, so the pattern rides wedding kimono: go, and do not come back.',
    kanoko: 'Kanoko — the fawn\u2019s spots. Shibori dots pinched and dyed one by one, named for the dapples down a young deer\u2019s back.',
    hishi: 'Hishi — the diamond. The floating leaf of the water caltrop, squared into a lattice that crosses the whole cloth.',
    sayagata: 'Sayagata — the silk fret. A manji lattice interlocked so no line ever ends; woven into silk gauze, it wishes a long life without a break.',
    kagome: 'Kagome — the basket weave. A bamboo lattice of hexagons and triangles; the pattern of the woven basket, sung as a ward against evil.',
    karakusa: 'Karakusa — the vine arabesque. Curls that never stop growing, carried on silk and temple cloth: prosperity, spreading.',
    ryusui: 'Ryusui — flowing water. It never stagnates and never stops; the pattern is worn for a life that keeps moving, and stays clean.',
    tatewaku: 'Tatewaku — the rising pattern. Paired waves stand and swell like steam off hot water: fortune, rising.',
    yukwa: 'Yukwa — the snow ring. A snowflake rounded into a medallion; snow promises a full harvest, and melts without a trace.',
    ajiro: 'Ajiro — wickerwork. Bamboo strips woven over and under, the pattern of trays and lattice screens: patient, and exact.',
    sankuzushi: 'Sankuzushi — the counting rods, broken. Bars laid in alternating directions, named for the abacus counters they imitate.',
    higaki: 'Higaki — the cypress fence. A doubled diagonal lattice, after the woven cypress fences of old gardens: quiet, and hard to climb.',
    hanabishi: 'Hanabishi — the flower diamond. The water-caltrop diamond with a flower at its heart, a crest softened into a pattern.',
    watsunagi: 'Watsunagi — linked rings. Ring inside ring inside ring, an unbroken chain: continuity, hand to hand.',
    bishamon: 'Bishamon-kikko — the tortoiseshell of Bishamon-ten, guardian of warriors; his armor is drawn as hexagons worked with triangles.'
  };
  var pattern = 'seigaiha', W, H;
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

  function kikko(t) {
    var R = 22, dx = Math.sqrt(3) * R, dy = 1.5 * R;
    ctx.lineWidth = 1.2;
    var row = 0;
    for (var y = -R; y < H + R; y += dy, row++) {
      for (var x = -dx; x < W + dx; x += dx) {
        var cx = x + (row % 2 ? dx / 2 : 0), cy = y;
        [1, .58].forEach(function (sc, i) {
          ctx.beginPath();
          for (var k = 0; k < 6; k++) {
            var a = Math.PI / 3 * k - Math.PI / 2, px = cx + R * sc * Math.cos(a), py = cy + R * sc * Math.sin(a);
            if (k === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
          }
          ctx.closePath();
          ctx.strokeStyle = i === 0 ? t.fg : t.mid;
          ctx.stroke();
        });
      }
    }
  }
  function uroko(t) {
    var s = 30, h = s * .87;
    ctx.lineWidth = 1.2;
    var row = 0;
    for (var y = h; y < H + h; y += h, row++) {
      for (var x = -s; x < W + s; x += s) {
        ctx.beginPath();
        ctx.moveTo(x, y); ctx.lineTo(x + s / 2, y - h); ctx.lineTo(x + s, y); ctx.closePath();
        ctx.fillStyle = row % 2 ? t.bg : t.soft;
        ctx.fill();
        ctx.strokeStyle = t.fg;
        ctx.stroke();
      }
    }
  }
  function same(t) {
    var R = 18;
    ctx.fillStyle = t.fg;
    var rows = Math.ceil(H / (R * .62)) + 2;
    for (var r = rows; r >= -1; r--) {
      var y = r * R * .62 + R;
      var off = (r % 2) * R;
      for (var x = -R + off; x < W + R; x += R * 2) {
        [1, .6].forEach(function (sc) {
          var Rk = R * sc, stepA = 5.6 / Rk;
          for (var a = Math.PI; a <= Math.PI * 2 + .001; a += stepA) {
            ctx.beginPath(); ctx.arc(x + Rk * Math.cos(a), y + Rk * Math.sin(a), 1.35, 0, 7); ctx.fill();
          }
        });
        ctx.beginPath(); ctx.arc(x, y, 1.35, 0, 7); ctx.fill();
      }
    }
  }
  function yagasuri(t) {
    var w = 24, h = 46;
    var row = 0;
    for (var y = -h; y < H + h; y += h * .8, row++) {
      for (var x = 0; x < W + w; x += w) {
        var cx = x + (row % 2 ? w / 2 : 0), cy = y;
        ctx.beginPath();
        ctx.moveTo(cx, cy);
        ctx.lineTo(cx + w * .4, cy + h * .34);
        ctx.lineTo(cx + w * .13, cy + h * .34);
        ctx.lineTo(cx + w * .13, cy + h);
        ctx.lineTo(cx, cy + h * .7);
        ctx.lineTo(cx - w * .13, cy + h);
        ctx.lineTo(cx - w * .13, cy + h * .34);
        ctx.lineTo(cx - w * .4, cy + h * .34);
        ctx.closePath();
        ctx.fillStyle = row % 2 ? t.mid : t.fg;
        ctx.globalAlpha = .88;
        ctx.fill();
        ctx.globalAlpha = 1;
      }
    }
  }
  function kanoko(t) {
    var s = 23;
    var row = 0;
    for (var y = s / 2; y < H + s; y += s, row++) {
      for (var x = s / 2 + (row % 2 ? s / 2 : 0); x < W + s; x += s) {
        ctx.beginPath(); ctx.arc(x, y, 8, 0, 7); ctx.strokeStyle = t.soft; ctx.lineWidth = 3.4; ctx.stroke();
        ctx.beginPath(); ctx.arc(x, y, 4.4, 0, 7); ctx.strokeStyle = t.fg; ctx.lineWidth = 1.5; ctx.stroke();
        ctx.beginPath(); ctx.arc(x, y, 1.5, 0, 7); ctx.fillStyle = t.fg; ctx.fill();
      }
    }
  }
  function hishi(t) {
    var s = 25;
    ctx.lineWidth = 1.1; ctx.strokeStyle = t.mid;
    ctx.beginPath();
    for (var d = -H; d < W + H; d += s) { ctx.moveTo(d, 0); ctx.lineTo(d + H, H); }
    for (var d2 = 0; d2 < W + 2 * H; d2 += s) { ctx.moveTo(d2, 0); ctx.lineTo(d2 - H, H); }
    ctx.stroke();
    ctx.fillStyle = t.fg;
    for (var gy = 0; gy <= H + s; gy += s) for (var gx = 0; gx <= W + s; gx += s) {
      var px = gx + ((gy / s) % 2 ? 0 : 0), py = gy;
      ctx.save(); ctx.translate(px, py); ctx.rotate(Math.PI / 4); ctx.fillRect(-2.1, -2.1, 4.2, 4.2); ctx.restore();
    }
  }
  function sayagata(t) {
    var s = 36, u = s / 4;
    ctx.lineWidth = 2; ctx.strokeStyle = t.fg; ctx.lineCap = 'square';
    function hook(x, y) {
      ctx.beginPath();
      ctx.moveTo(x, y + 3 * u); ctx.lineTo(x + 3 * u, y + 3 * u); ctx.lineTo(x + 3 * u, y + u); ctx.lineTo(x + u, y + u); ctx.lineTo(x + u, y + 2 * u); ctx.lineTo(x + 2 * u, y + 2 * u);
      ctx.stroke();
    }
    for (var y = -s; y < H + s; y += s) {
      for (var x = -s; x < W + s; x += s) {
        hook(x, y);
        hook(x + 2 * u, y + 2 * u);
      }
    }
  }
  function kagome(t) {
    var d = 27, st = d * 1.155;
    ctx.lineWidth = 1.3; ctx.strokeStyle = t.mid;
    ctx.beginPath();
    for (var y = 0; y <= H + d; y += d) { ctx.moveTo(0, y); ctx.lineTo(W, y); }
    for (var x = -H; x < W + H; x += st) { ctx.moveTo(x, 0); ctx.lineTo(x + H * .577, H); }
    for (var x2 = 0; x2 < W + 2 * H; x2 += st) { ctx.moveTo(x2, 0); ctx.lineTo(x2 - H * .577, H); }
    ctx.stroke();
  }
  function karakusa(t) {
    var s = 56;
    ctx.lineWidth = 1.7; ctx.lineCap = 'round';
    var row = 0;
    for (var y = s / 2; y < H + s; y += s, row++) {
      for (var x = s / 2; x < W + s; x += s) {
        var cx = x + (row % 2 ? s / 2 : 0), cy = y;
        var flip = ((Math.round(cx / s) + row) % 2) ? -1 : 1;
        ctx.strokeStyle = t.fg;
        ctx.beginPath();
        for (var a = 0; a <= Math.PI * 4.4; a += .3) {
          var r = 1.5 + a * 1.28, px = cx + flip * r * Math.cos(a), py = cy + r * Math.sin(a);
          if (a === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
        }
        ctx.stroke();
        ctx.strokeStyle = t.mid;
        ctx.beginPath();
        if (flip > 0) ctx.arc(cx - s / 2, cy - s / 2, s * .4, 0, Math.PI / 2);
        else ctx.arc(cx + s / 2, cy - s / 2, s * .4, Math.PI / 2, Math.PI);
        ctx.stroke();
      }
    }
  }
  function ryusui(t) {
    ctx.lineWidth = 1.5; ctx.lineCap = 'round';
    var band = 42;
    for (var r = 0; r * band < H + band; r++) {
      var base = r * band + 12;
      [0, 1, 2].forEach(function (k) {
        ctx.beginPath();
        ctx.strokeStyle = k === 1 ? t.mid : t.fg;
        for (var x = 0; x <= W; x += 6) {
          var y = base + k * 7 + Math.sin(x * .028 + r * 1.7 + k * 2.1) * 4.5;
          if (x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
        }
        ctx.stroke();
      });
      var sx = ((r * 173) % Math.max(60, W - 40)) + 20;
      [9.5, 6].forEach(function (rr) { ctx.beginPath(); ctx.arc(sx, base + 7, rr, .2, 5.9); ctx.strokeStyle = t.fg; ctx.stroke(); });
    }
  }
  function tatewaku(t) {
    ctx.lineWidth = 1.6;
    for (var cx = -12; cx < W + 30; cx += 38) {
      [0, 1].forEach(function (k) {
        ctx.beginPath(); ctx.strokeStyle = k ? t.mid : t.fg;
        for (var y = 0; y <= H; y += 6) {
          var x = cx + k * 13 + Math.sin(y * .026 + k * Math.PI) * 6.5;
          if (y === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
        }
        ctx.stroke();
      });
    }
  }
  function yukwa(t) {
    var sx = 66, sy = 58, row = 0;
    for (var y = sy / 2; y < H + sy; y += sy, row++) {
      for (var x = sx / 2 + (row % 2 ? sx / 2 : 0); x < W + sx; x += sx) {
        ctx.lineWidth = 1.6; ctx.strokeStyle = t.fg;
        ctx.beginPath(); ctx.arc(x, y, 15.5, 0, 7); ctx.stroke();
        for (var k = 0; k < 6; k++) {
          var a = Math.PI / 3 * k + Math.PI / 6, nx = x + 15.5 * Math.cos(a), ny = y + 15.5 * Math.sin(a);
          ctx.beginPath(); ctx.arc(nx, ny, 4.6, a + Math.PI * .55, a + Math.PI * 1.45); ctx.stroke();
        }
        ctx.lineWidth = 1.1; ctx.strokeStyle = t.mid;
        ctx.beginPath(); ctx.arc(x, y, 8.6, 0, 7); ctx.stroke();
        ctx.beginPath(); ctx.arc(x, y, 1.7, 0, 7); ctx.fillStyle = t.fg; ctx.fill();
      }
    }
    ctx.fillStyle = t.mid;
    for (var y2 = sy; y2 < H; y2 += sy) for (var x2 = sx; x2 < W; x2 += sx) { ctx.beginPath(); ctx.arc(x2, y2, 1.3, 0, 7); ctx.fill(); }
  }
  function ajiro(t) {
    var w = 9, b = w * 3;
    for (var by = 0; by < H + b; by += b) for (var bx = 0; bx < W + b; bx += b) {
      var horiz = ((bx / b) + (by / b)) % 2 === 0;
      for (var k = 0; k < 3; k++) {
        ctx.fillStyle = t.soft; ctx.strokeStyle = t.mid; ctx.lineWidth = 1;
        if (horiz) { ctx.fillRect(bx + 1, by + k * w + 1, b - 2, w - 2); ctx.strokeRect(bx + 1, by + k * w + 1, b - 2, w - 2); }
        else { ctx.fillRect(bx + k * w + 1, by + 1, w - 2, b - 2); ctx.strokeRect(bx + k * w + 1, by + 1, w - 2, b - 2); }
      }
    }
  }
  function sankuzushi(t) {
    var b = 39, bw = 7, gap = 6;
    ctx.fillStyle = t.fg;
    for (var by = 0; by < H + b; by += b) for (var bx = 0; bx < W + b; bx += b) {
      var horiz = ((bx / b) + (by / b)) % 2 === 0;
      ctx.globalAlpha = .85;
      for (var k = 0; k < 3; k++) {
        if (horiz) ctx.fillRect(bx + 2, by + 3 + k * (bw + gap), b - 4, bw);
        else ctx.fillRect(bx + 3 + k * (bw + gap), by + 2, bw, b - 4);
      }
      ctx.globalAlpha = 1;
    }
  }
  function higaki(t) {
    var s = 38;
    ctx.lineWidth = 1.2; ctx.strokeStyle = t.mid;
    [-2.2, 2.2].forEach(function (o) {
      ctx.beginPath();
      for (var d = -H; d < W + H; d += s) { ctx.moveTo(d + o, 0); ctx.lineTo(d + H + o, H); }
      for (var d2 = 0; d2 < W + 2 * H; d2 += s) { ctx.moveTo(d2 + o, 0); ctx.lineTo(d2 - H + o, H); }
      ctx.stroke();
    });
  }
  function hanabishi(t) {
    var dx = 48, dy = 42, row = 0;
    for (var y = dy / 2; y < H + dy; y += dy, row++) {
      for (var x = dx / 2 + (row % 2 ? dx / 2 : 0); x < W + dx; x += dx) {
        ctx.beginPath();
        ctx.moveTo(x, y - 19); ctx.lineTo(x + 22, y); ctx.lineTo(x, y + 19); ctx.lineTo(x - 22, y); ctx.closePath();
        ctx.strokeStyle = t.fg; ctx.lineWidth = 1.4; ctx.stroke();
        ctx.strokeStyle = t.mid; ctx.lineWidth = 1.1;
        for (var k = 0; k < 4; k++) {
          var a = Math.PI / 2 * k, ex = x + 8.5 * Math.cos(a), ey = y + 8.5 * Math.sin(a);
          ctx.beginPath(); ctx.ellipse(ex, ey, k % 2 ? 3.4 : 4.6, k % 2 ? 4.6 : 3.4, 0, 0, 7); ctx.stroke();
        }
        ctx.beginPath(); ctx.arc(x, y, 1.6, 0, 7); ctx.fillStyle = t.fg; ctx.fill();
      }
    }
  }
  function watsunagi(t) {
    var R = 16, st = 27, row = 0;
    for (var y = 0; y < H + R; y += st, row++) {
      for (var x = (row % 2 ? st / 2 : 0); x < W + R; x += st) {
        ctx.beginPath(); ctx.arc(x, y, R, 0, 7); ctx.strokeStyle = t.mid; ctx.lineWidth = 1.3; ctx.stroke();
        ctx.beginPath(); ctx.arc(x, y, R - 3.4, 0, 7); ctx.strokeStyle = t.fg; ctx.stroke();
      }
    }
  }
  function bishamon(t) {
    var R = 25, dx = Math.sqrt(3) * R, dy = 1.5 * R, row = 0;
    ctx.lineWidth = 1.2;
    for (var y = -R; y < H + R; y += dy, row++) {
      for (var x = -dx; x < W + dx; x += dx) {
        var cx = x + (row % 2 ? dx / 2 : 0), cy = y, v = [];
        for (var k = 0; k < 6; k++) { var a = Math.PI / 3 * k - Math.PI / 2; v.push([cx + R * Math.cos(a), cy + R * Math.sin(a)]); }
        ctx.beginPath();
        v.forEach(function (p, i) { if (i === 0) ctx.moveTo(p[0], p[1]); else ctx.lineTo(p[0], p[1]); });
        ctx.closePath(); ctx.strokeStyle = t.fg; ctx.stroke();
        ctx.strokeStyle = t.mid;
        [0, 2, 4].forEach(function (k2) { ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(v[k2][0], v[k2][1]); ctx.stroke(); });
        ctx.fillStyle = t.mid;
        v.forEach(function (p, i) {
          if (i % 2) return;
          var a2 = Math.PI / 3 * i - Math.PI / 2, tx = cx + (R + 5) * Math.cos(a2), ty = cy + (R + 5) * Math.sin(a2);
          ctx.beginPath();
          ctx.moveTo(tx, ty);
          ctx.lineTo(tx + 5 * Math.cos(a2 + 2.2), ty + 5 * Math.sin(a2 + 2.2));
          ctx.lineTo(tx + 5 * Math.cos(a2 - 2.2), ty + 5 * Math.sin(a2 - 2.2));
          ctx.closePath(); ctx.fill();
        });
      }
    }
  }
  function draw() {
    var TONES = tones();
    var t = TONES[effTone()];
    var tb = root.querySelector('[data-wag-tone]');
    if (tb) tb.textContent = 'Tone: ' + t.name;
    W = canvas.clientWidth; H = canvas.clientHeight;
    canvas.width = W * DPR; canvas.height = H * DPR; ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    ctx.fillStyle = t.bg; ctx.fillRect(0, 0, W, H);
    ({ seigaiha: seigaiha, asanoha: asanoha, shippo: shippo, ichimatsu: ichimatsu, kikko: kikko, uroko: uroko, same: same, yagasuri: yagasuri, kanoko: kanoko, hishi: hishi, sayagata: sayagata, kagome: kagome, karakusa: karakusa, ryusui: ryusui, tatewaku: tatewaku, yukwa: yukwa, ajiro: ajiro, sankuzushi: sankuzushi, higaki: higaki, hanabishi: hanabishi, watsunagi: watsunagi, bishamon: bishamon })[pattern](t);
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
  root.querySelector('[data-wag-tone]').addEventListener('click', function () { picked = (effTone() + 1) % 3; draw(); });
  window.addEventListener('resize', draw);
  new MutationObserver(function () { if (picked === null) draw(); }).observe(document.body, { attributes: true, subtree: true, attributeFilter: ['data-theme'] });
  draw();
});
