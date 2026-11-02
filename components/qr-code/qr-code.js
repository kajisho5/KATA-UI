// KATA QR Code — a zero-dependency encoder written from ISO/IEC 18004.
// Byte mode, error-correction level M, versions 1–6 (14–106 bytes).
// The mask is chosen by the standard's four penalty rules.

// ---- Galois field GF(256), primitive polynomial 0x11d ----
var KQR_EXP = [], KQR_LOG = [];
(function () {
  var x = 1;
  for (var i = 0; i < 255; i++) { KQR_EXP.push(x); KQR_LOG[x] = i; x <<= 1; if (x & 0x100) x ^= 0x11d; }
})();
function kqrMul(a, b) { return (a && b) ? KQR_EXP[(KQR_LOG[a] + KQR_LOG[b]) % 255] : 0; }
function kqrPolyMul(p, q) {
  var r = new Array(p.length + q.length - 1).fill(0);
  for (var i = 0; i < p.length; i++) for (var j = 0; j < q.length; j++) r[i + j] ^= kqrMul(p[i], q[j]);
  return r;
}
function kqrGenPoly(n) {
  var g = [1];
  for (var i = 0; i < n; i++) g = kqrPolyMul(g, [1, KQR_EXP[i]]);
  return g;
}
function kqrRemainder(data, gen) {
  var res = new Array(gen.length - 1).fill(0);
  data.forEach(function (b) {
    var factor = b ^ res.shift();
    res.push(0);
    for (var i = 0; i < res.length; i++) res[i] ^= kqrMul(gen[i + 1], factor);
  });
  return res;
}

// version -> [blocks, data codewords per block, EC per block, alignment center, remainder bits]
var KQR_V = [null,
  [1, 16, 10, 0, 0], [1, 28, 16, 18, 7], [1, 44, 26, 22, 7],
  [2, 32, 18, 26, 7], [2, 43, 24, 30, 7], [4, 27, 16, 34, 7]];

function kqrDataCodewords(bytes, ver) {
  var info = KQR_V[ver];
  var capBits = info[0] * info[1] * 8;
  var bits = [];
  function push(val, len) { for (var i = len - 1; i >= 0; i--) bits.push((val >>> i) & 1); }
  push(0x4, 4); // byte mode
  push(bytes.length, 8);
  bytes.forEach(function (b) { push(b, 8); });
  push(0, Math.min(4, capBits - bits.length));
  while (bits.length % 8) bits.push(0);
  var out = [];
  for (var i = 0; i < bits.length; i += 8) {
    var v = 0; for (var j = 0; j < 8; j++) v = (v << 1) | bits[i + j];
    out.push(v);
  }
  var pads = [0xec, 0x11], total = info[0] * info[1];
  for (var k = 0; out.length < total; k++) out.push(pads[k % 2]);
  return out;
}

function kqrInterleave(dataCw, ver) {
  var info = KQR_V[ver], nb = info[0], per = info[1], gen = kqrGenPoly(info[2]);
  var blocks = [], ecs = [], i, j;
  for (i = 0; i < nb; i++) {
    var chunk = dataCw.slice(i * per, (i + 1) * per);
    blocks.push(chunk);
    ecs.push(kqrRemainder(chunk, gen));
  }
  var bits = [];
  function pushByte(v) { for (var k = 7; k >= 0; k--) bits.push((v >>> k) & 1); }
  for (j = 0; j < per; j++) for (i = 0; i < nb; i++) pushByte(blocks[i][j]);
  for (j = 0; j < info[2]; j++) for (i = 0; i < nb; i++) pushByte(ecs[i][j]);
  for (i = 0; i < info[4]; i++) bits.push(0);
  return bits;
}

function kqrFormatBits(mask) {
  var data = mask; // EC level M indicator bits are 00, so data = 0b00<<3 | mask
  var rem = data;
  for (var i = 0; i < 10; i++) rem = (rem << 1) ^ (((rem >>> 9) & 1) * 0x537);
  return ((data << 10) | rem) ^ 0x5412;
}

function kqrMatrix(text) {
  var bytes = Array.prototype.slice.call(new TextEncoder().encode(text));
  var ver = 0;
  for (var v = 1; v <= 6; v++) {
    if (bytes.length <= Math.floor((KQR_V[v][0] * KQR_V[v][1] * 8 - 12) / 8)) { ver = v; break; }
  }
  if (!ver) return null;
  var size = 17 + 4 * ver;
  var bits = kqrInterleave(kqrDataCodewords(bytes, ver), ver);
  var mod = [], fn = [], x, y;
  for (y = 0; y < size; y++) { mod.push(new Array(size).fill(0)); fn.push(new Array(size).fill(false)); }
  function setF(xx, yy, dark) { if (0 <= xx && xx < size && 0 <= yy && yy < size) { mod[yy][xx] = dark ? 1 : 0; fn[yy][xx] = true; } }
  function drawFinder(cx, cy) {
    for (var dy = -4; dy <= 4; dy++) for (var dx = -4; dx <= 4; dx++) {
      var dist = Math.max(Math.abs(dx), Math.abs(dy));
      setF(cx + dx, cy + dy, dist !== 2 && dist !== 4);
    }
  }
  for (var i = 0; i < size; i++) { setF(6, i, i % 2 === 0); setF(i, 6, i % 2 === 0); }
  drawFinder(3, 3); drawFinder(size - 4, 3); drawFinder(3, size - 4);
  var align = KQR_V[ver][3];
  if (align) {
    for (var dy2 = -2; dy2 <= 2; dy2++) for (var dx2 = -2; dx2 <= 2; dx2++)
      setF(align + dx2, align + dy2, Math.max(Math.abs(dx2), Math.abs(dy2)) !== 1);
  }
  setF(8, size - 8, 1); // dark module
  // reserve the format-information cells before data placement —
  // they are function modules even though their values wait for the mask
  (function reserveFormat() {
    for (var i = 0; i <= 5; i++) { setF(8, i, 0); setF(i, 8, 0); }
    setF(8, 7, 0); setF(8, 8, 0); setF(7, 8, 0);
    for (var i = 0; i < 8; i++) setF(size - 1 - i, 8, 0);
    for (var i = 8; i < 15; i++) setF(8, size - 15 + i, 0);
  })();
  // reserve format cells (values drawn after masking)
  function drawFormat(mask) {
    var bitsF = kqrFormatBits(mask);
    function bit(i) { return ((bitsF >>> i) & 1) === 1; }
    for (var i = 0; i <= 5; i++) setF(8, i, bit(i));
    setF(8, 7, bit(6)); setF(8, 8, bit(7)); setF(7, 8, bit(8));
    for (var i = 9; i < 15; i++) setF(14 - i, 8, bit(i));
    for (var i = 0; i < 8; i++) setF(size - 1 - i, 8, bit(i));
    for (var i = 8; i < 15; i++) setF(8, size - 15 + i, bit(i));
    setF(8, size - 8, 1);
  }
  // place data bits (zigzag), skipping function modules
  var bi = 0;
  for (var right = size - 1; right >= 1; right -= 2) {
    if (right === 6) right = 5;
    for (var vert = 0; vert < size; vert++) {
      for (var j = 0; j < 2; j++) {
        var xx = right - j;
        var upward = ((right + 1) & 2) === 0;
        var yy = upward ? size - 1 - vert : vert;
        if (!fn[yy][xx]) { mod[yy][xx] = bi < bits.length ? bits[bi] : 0; bi++; }
      }
    }
  }
  function maskBit(mask, xx, yy) {
    switch (mask) {
      case 0: return (xx + yy) % 2 === 0;
      case 1: return yy % 2 === 0;
      case 2: return xx % 3 === 0;
      case 3: return (xx + yy) % 3 === 0;
      case 4: return (Math.floor(yy / 2) + Math.floor(xx / 3)) % 2 === 0;
      case 5: return (xx * yy) % 2 + (xx * yy) % 3 === 0;
      case 6: return ((xx * yy) % 2 + (xx * yy) % 3) % 2 === 0;
      case 7: return ((xx + yy) % 2 + (xx * yy) % 3) % 2 === 0;
    }
    return false;
  }
  function penalties(m) {
    var score = 0, xx, yy, run, c;
    // rule 1: runs
    for (yy = 0; yy < size; yy++) {
      run = 1;
      for (xx = 1; xx < size; xx++) { if (m[yy][xx] === m[yy][xx - 1]) { run++; } else { if (run >= 5) score += run - 2; run = 1; } }
      if (run >= 5) score += run - 2;
    }
    for (xx = 0; xx < size; xx++) {
      run = 1;
      for (yy = 1; yy < size; yy++) { if (m[yy][xx] === m[yy - 1][xx]) { run++; } else { if (run >= 5) score += run - 2; run = 1; } }
      if (run >= 5) score += run - 2;
    }
    // rule 2: 2x2 blocks
    for (yy = 0; yy < size - 1; yy++) for (xx = 0; xx < size - 1; xx++) {
      c = m[yy][xx];
      if (c === m[yy][xx + 1] && c === m[yy + 1][xx] && c === m[yy + 1][xx + 1]) score += 3;
    }
    // rule 3: finder-like patterns
    function checkLine(line) {
      var s = 0;
      for (var i = 0; i + 11 <= line.length; i++) {
        var w = line.slice(i, i + 11).join('');
        if (w === '10111010000' || w === '00001011101') s += 40;
      }
      return s;
    }
    for (yy = 0; yy < size; yy++) score += checkLine(m[yy]);
    for (xx = 0; xx < size; xx++) score += checkLine(m.map(function (row) { return row[xx]; }));
    // rule 4: balance
    var dark = 0;
    m.forEach(function (row) { row.forEach(function (v) { dark += v; }); });
    var k = Math.ceil(Math.abs(dark * 20 - size * size * 10) / (size * size)) - 1;
    if (k > 0) score += k * 10;
    return score;
  }
  var best = null, bestScore = Infinity, bestMask = 0;
  for (var mask = 0; mask < 8; mask++) {
    var trial = mod.map(function (row, yy) {
      return row.map(function (v, xx) { return (!fn[yy][xx] && maskBit(mask, xx, yy)) ? v ^ 1 : v; });
    });
    // format cells in the trial: temporarily draw, score, keep matrix pure
    var saved = [];
    for (y = 0; y < size; y++) for (x = 0; x < size; x++) if (fn[y][x] && ((x === 8) || (y === 8))) saved.push([x, y, trial[y][x]]);
    // draw format on the trial via a shim: reuse setF against trial
    (function () {
      var bitsF = kqrFormatBits(mask);
      function bit(i2) { return ((bitsF >>> i2) & 1) === 1 ? 1 : 0; }
      function s2(xx, yy, val) { if (0 <= xx && xx < size && 0 <= yy && yy < size) trial[yy][xx] = val; }
      for (var i = 0; i <= 5; i++) s2(8, i, bit(i));
      s2(8, 7, bit(6)); s2(8, 8, bit(7)); s2(7, 8, bit(8));
      for (var i = 9; i < 15; i++) s2(14 - i, 8, bit(i));
      for (var i = 0; i < 8; i++) s2(size - 1 - i, 8, bit(i));
      for (var i = 8; i < 15; i++) s2(8, size - 15 + i, bit(i));
      s2(8, size - 8, 1);
    })();
    var sc = penalties(trial);
    if (sc < bestScore) { bestScore = sc; best = trial; bestMask = mask; }
  }
  return { size: size, version: ver, mask: bestMask, modules: best };
}

function kqrSVG(text, label) {
  var r = kqrMatrix(text);
  if (!r) return null;
  var n = r.size, d = '';
  for (var y = 0; y < n; y++) for (var x = 0; x < n; x++)
    if (r.modules[y][x]) d += 'M' + (x + 4) + ' ' + (y + 4) + 'h1v1h-1z';
  return '<svg viewBox="0 0 ' + (n + 8) + ' ' + (n + 8) + '" role="img" aria-label="' +
    (label || ('QR code: ' + text)) + '"><rect width="' + (n + 8) + '" height="' + (n + 8) + '" fill="#fff"/>' +
    '<path d="' + d + '" fill="#18181b"/></svg>';
}

document.querySelectorAll('[data-qr]').forEach(function (el) {
  var svg = kqrSVG(el.getAttribute('data-qr'), el.getAttribute('data-qr-label'));
  if (svg) { el.innerHTML = svg; }
  else { el.innerHTML = '<span class="qr-fallback">This text is too long for a version 6 code (106 bytes at level M).</span>'; }
});
