// KATA Wagara — classical patterns that tile, drawn from their constructions.
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
    bishamon: 'Bishamon-kikko — the tortoiseshell of Bishamon-ten, guardian of warriors; his armor is drawn as hexagons worked with triangles.',
    tatenami: 'Tatenami — standing waves. Bold arcs rearing in rows, crests flecked with foam; the sea with its back up.',
    kanzemizu: 'Kanzemizu — the Kanze school water. Great slow swirls named for a Noh house; water that turns and remembers.',
    genjigumo: 'Genjigumo — Genji clouds. Long cloud bands with a curled end, named for the Tale of Genji chapter screens.',
    kasumi: 'Kasumi — mist. Flat bands drifting at offsets; the pattern for everything half-seen and better for it.',
    kumo: 'Kumo — clouds. Single arcs in rows, the scalloped edge of a cloud bank, drawn out to the horizon.',
    ame: 'Ame — rain. Slanted strokes in companies, the way rain actually arrives: together, and at an angle.',
    yanagi: 'Yanagi — the willow. Strands hung from the top of the cloth, leafed and swaying; what bends in the wind, survives it.',
    raimon: 'Raimon — the thunder pattern. One squared spiral, struck like a bolt and repeated; an old pattern with a loud name.',
    kojitsunagi: 'Kojitsunagi — the character 工， linked. Bars turned alternately so the letters hold each other up.',
    manjitsunagi: 'Manjitsunagi — linked manji. Four bent arms to a cell, chained without a break; an auspicious sign far older than its misuse.',
    igeta: 'Igeta — the well curb. Doubled lines crossing like the frame of a well; the mark of things drawn from deep water.',
    mansuji: 'Mansuji — ten thousand lines. Pinstripes beyond counting, the proudest of the Edo komon; luxury you need a loupe to see.',
    komochijima: 'Komochijima — the stripe with a child. A wide band carrying a thin stripe inside it, parent and child in one cloth.',
    yamaji: 'Yamaji — the mountain road. A zigzag that climbs and descends in rows, woven the way a path switchbacks.',
    arare: 'Arare — hail. Dots of no fixed size, scattered the way hail actually falls; a komon classic.',
    hyoretsu: 'Hyoretsu — cracked ice. A jittered lattice of fractures, the pattern of a pond the morning after it freezes.',
    jujigasuri: 'Jujigasuri — the cross kasuri. Plus signs woven into the cloth, one thread-count at a time.',
    igasuri: 'Igasuri — the well kasuri. Small # marks in offset rows; the kasuri weaver counting in wells.',
    fundotsunagi: 'Fundotsunagi — linked scale-weights. The fundo weight of the money-changer, chained lobe to lobe.',
    kusari: 'Kusari — the chain. Oval links turned alternately, each holding the next; drawn double, like the real links.',
    matsukawabishi: 'Matsukawabishi — pine-bark diamonds. Tall diamonds stacked like the plates of pine bark.',
    takedabishi: 'Takedabishi — the Takeda diamonds. Four diamonds in a square, the crest of the Takeda house.',
    mitsubishi: 'Mitsubishi — three diamonds. One above two, the arrangement that became a company mark the world knows.',
    kenhanabishi: 'Kenhanabishi — the sword flower-diamond. A hanabishi with blades at its diagonals; a crest, sharpened.',
    nijukikko: 'Nijukikko — the double tortoiseshell. Kikko drawn at three removes, shell inside shell inside shell.',
    kikkohanabishi: 'Kikkohanabishi — the tortoiseshell flower-diamond. A hanabishi blooming inside every hexagon.',
    hanashippo: 'Hanashippo — the flower shippo. Seven treasures with a four-petal flower struck at every crossing.',
    amime: 'Amime — the net. A diamond mesh with a knotted ring at every crossing, cast for fish and for fences.',
    kakutoshi: 'Kakutoshi — passing squares. Tiny squares in strict rows, the quietest of the komon family.',
    ishigaki: 'Ishigaki — the stone wall. Rounded blocks laid in offset courses, the pattern of castle foundations.',
    takegaki: 'Takegaki — the bamboo fence. Slats in pairs with tied crossbars, the garden fence drawn flat.',
    senbongoshi: 'Senbongoshi — the thousand-bar lattice. Thin slats ruled by heavier frames, a window drawn as a pattern.',
    hakarakusa: 'Hakarakusa — leaf arabesque. A waving stem putting out leaves in turn, the vine drawn as a border.',
    noshi: 'Noshi — the gift band. Strips of the noshi wrapper laid diagonally, folds and all; ceremony as a pattern.',
    tabanenoshi: 'Tabane noshi — bundled bands. Ribbons in threes, tied at intervals; many gifts, one bundle.',
    maruuroko: 'Maru uroko — round scales. The uroko tiling with circles for triangles; a softer armor.',
    dandigai: 'Dandigai ichimatsu — the staggered check. Ichimatsu with each row slipped half a stone, so the field never sits still.',
    ishidatami: 'Ishidatami — stone paving. Big checks with a dressed edge inside each stone; the floor of a castle approach.',
    koshi: 'Koshi — the lattice. One line each way, nothing hidden; the grid every other pattern is measured against.',
    nanamegoshi: 'Naname goshi — the diagonal lattice. The koshi turned forty-five degrees; diamonds where the squares were.',
    yotsumeami: 'Yotsume ami — four-eye weave. Basket squares drawn over and under in turn, the weave you can read.',
    goma: 'Goma — sesame. The smallest dots in the komon book, sown evenly; a texture before it is a pattern.',
    chidorigoshi: 'Chidorigoshi — the plover check, the world’s houndstooth. Checks broken by teeth at every corner.',
    sensuji: 'Sensuji — a thousand stripes. Lines in companies of six with a rest between; mansuji’s quieter brother.',
    koshijima: 'Koshijima — the check stripe. Warp bands crossing weft bands, darker where they meet, the way dyed cloth deepens.',
    dandan: 'Dandan — step by step. Bands laid in a slow staircase of offsets; a pattern that climbs without rising.',
    hishigasane: 'Hishigasane — layered diamonds. Outlines overlapping point to point, a chain of lozenges running off both edges.',
    irekobishi: 'Ireko bishi — nested diamonds. Three outlines to a stone, diamond inside diamond inside diamond.',
    suimon: 'Suimon — water crests. Wave lines in close ranks, phase shifting row by row; a river drawn in section.',
    kikkogasuri: 'Kikko gasuri — the tortoiseshell kasuri. Bold hexagons woven as marks, one to a count of threads.',
    takeami: 'Takeami — bamboo weave. Plain weave drawn honestly: over, under, over, under, in rounded strips.',
    sankakugoshi: 'Sankaku goshi — the triangle lattice. Three directions of line, nothing else; the truss of the pattern world.',
    kasaneshikaku: 'Kasane shikaku — layered squares. A square and its forty-five-degree twin on every point; eight-point stars where they marry.',
    uzutsunagi: 'Uzu tsunagi — linked whirlpools. Spirals chained by an arc to the next; the whirlpool made sociable.',
    mizutama: 'Mizutama — water drops. Dots in two sizes, the polka dot before it was polka; rain, counted.',
    futojima: 'Futojima — the bold stripe. A wide band and two hairlines for company; stripes with their shoulders back.',
    nanameichimatsu: 'Naname ichimatsu — the check on the diagonal. Ichimatsu rotated until the squares stand on their points.',
    midareishigaki: 'Midare ishigaki — the rough stone wall. Courses of uneven blocks, laid the way field stone actually falls.',
    kasanesankaku: 'Kasane sankaku — layered triangles. Points up and points down in one lattice; hexagrams wherever they marry.',
    mikazuki: 'Mikazuki — crescent moons. Rows of crescents alternating their horns; the moon at three days, tiled.',
    kakutsunagi: 'Kaku tsunagi — linked squares. Plain squares chained by diamonds at the corners; right angles, holding hands.',
    ayaori: 'Ayaori — the twill weave. Diagonal steps at thread scale; the weave of every pair of jeans, drawn as a pattern.',
    sorobandama: 'Soroban dama — abacus beads. Bicones on their rods in counted rows; arithmetic as ornament.',
    kikkokuzushi: 'Kikko kuzushi — the broken tortoiseshell. Kikko with its columns slipped, the shell after an earthquake, still standing.',
    wagasane: 'Wagasane — layered rings. Rings overlapping in ranks like mail; circles that behave like scales.',
    yokojima: 'Yokojima — the horizontal stripe. Laid bands with a ruled double line; the stripe at rest.',
    sakurakumiko: 'Sakura kumiko — the kumiko lattice. Joinery hexagons with a six-point star fitted inside, the woodworker’s geometry.',
    chigaitatewaku: 'Chigai tatewaku — unmatched standing waves. Wide pairs and narrow pairs alternating up the cloth.',
    chigaibishi: 'Chigai bishi — unmatched diamonds. Big stones and small stones dealt alternately across the field.',
    kasanegoshi: 'Kasane goshi — the doubled lattice. Two grids overlaid half a cell apart; a mesh with pinned crossings.',
    nanameyagasuri: 'Naname yagasuri — the arrows on the diagonal. Yagasuri flying at an angle, the wind it was shot into drawn in.',
    tsurugoshi: 'Tsuru goshi — the vine lattice. A grid that grew instead of being ruled; lines waving where they cross.',
    kasumigasane: 'Kasumi gasane — layered mist. The mist bands doubled and slipped, weather in pairs.',
    kumogasane: 'Kumo gasane — layered clouds. Scallop banks filled in turn, a cloud deck seen from above it.',
    futogoshi: 'Futo goshi — the bold lattice. Koshi with its shoulders up: thick bars and a punched knot at every crossing.',
    ichimatsujima: 'Ichimatsu jima — the check stripe. Ichimatsu confined to bands, plain cloth between; checks reporting for duty in columns.',
    irekoasanoha: 'Ireko asanoha — the nested hemp star. Asanoha with a half-scale copy of itself fitted inside every star.',
    irekoshippo: 'Ireko shippo — the nested seven treasures. Shippo with a ring struck at every crossing and a bead at every quarter point.',
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
  function tatenami(t) {
    var R = 44;
    ctx.lineWidth = 2.4;
    var row = 0;
    for (var y = R * .4; y < H + R; y += R * .78, row++) {
      for (var x = -R + (row % 2 ? R : 0); x < W + R; x += R * 2) {
        [1, .68, .38].forEach(function (sc, i) {
          ctx.beginPath(); ctx.arc(x, y, R * sc, Math.PI * 1.08, Math.PI * 1.92);
          ctx.strokeStyle = i ? t.mid : t.fg; ctx.stroke();
        });
        ctx.beginPath(); ctx.arc(x + R * .8, y - R * .52, 3.4, 0, 7); ctx.fillStyle = t.fg; ctx.fill();
      }
    }
  }
  function kanzemizu(t) {
    var s = 96;
    ctx.lineWidth = 2.1; ctx.lineCap = 'round';
    var row = 0;
    for (var y = s / 2; y < H + s; y += s * .82, row++) {
      for (var x = s / 2 + (row % 2 ? s / 2 : 0); x < W + s; x += s) {
        ctx.strokeStyle = t.fg;
        ctx.beginPath();
        for (var a = 0; a <= Math.PI * 3.7; a += .25) {
          var r = 1 + a * 2.5, px = x + r * Math.cos(a), py = y + r * Math.sin(a);
          if (a === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
        }
        ctx.stroke();
      }
      ctx.strokeStyle = t.mid; ctx.lineWidth = 1.4;
      ctx.beginPath();
      for (var x2 = 0; x2 <= W; x2 += 6) { var y2 = y + s * .42 + Math.sin(x2 * .03 + row * 2) * 4; if (x2 === 0) ctx.moveTo(x2, y2); else ctx.lineTo(x2, y2); }
      ctx.stroke(); ctx.lineWidth = 2.1;
    }
  }
  function genjigumo(t) {
    var bh = 46;
    ctx.lineWidth = 1.4;
    for (var r = 0; r * bh < H + bh; r++) {
      var y = r * bh + 26, off = (r % 2) * 52;
      for (var x = -60 + off; x < W + 60; x += 118) {
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(x + 96, y);
        ctx.arc(x + 84, y, 12, 0, Math.PI, true);
        ctx.arc(x + 58, y, 14, 0, Math.PI, true);
        ctx.arc(x + 30, y, 15, 0, Math.PI, true);
        ctx.arc(x + 10, y, 10, 0, Math.PI, true);
        ctx.closePath();
        ctx.fillStyle = t.soft; ctx.fill();
        ctx.strokeStyle = t.fg; ctx.stroke();
        ctx.beginPath();
        for (var a = 0; a <= Math.PI * 2.6; a += .3) { var rr = 1 + a * 1.5, px = x + 97 + rr * Math.cos(a), py = y - 2 + rr * Math.sin(a); if (a === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py); }
        ctx.strokeStyle = t.mid; ctx.stroke();
      }
    }
  }
  function kasumi(t) {
    var bh = 34;
    ctx.fillStyle = t.mid;
    for (var r = 0; r * bh < H + bh; r++) {
      var y = r * bh + 10, off = (r % 2) * 64;
      for (var x = -70 + off; x < W + 70; x += 128) {
        ctx.globalAlpha = .5;
        ctx.beginPath(); ctx.roundRect(x, y, 92, 9, 4.5); ctx.fill();
        ctx.globalAlpha = 1;
      }
    }
  }
  function kumo(t) {
    var R = 17;
    ctx.lineWidth = 1.4;
    var row = 0;
    for (var y = R; y < H + R * 2; y += R * 1.15, row++) {
      for (var x = -R + (row % 2 ? R : 0); x < W + R; x += R * 2) {
        ctx.beginPath(); ctx.arc(x, y, R, Math.PI, 0); ctx.strokeStyle = t.fg; ctx.stroke();
        ctx.beginPath(); ctx.arc(x, y, R * .58, Math.PI, 0); ctx.strokeStyle = t.mid; ctx.stroke();
      }
    }
  }
  function ame(t) {
    ctx.lineWidth = 1.2; ctx.strokeStyle = t.mid; ctx.lineCap = 'round';
    for (var gy = 8; gy < H + 40; gy += 44) {
      for (var gx = 0; gx < W + 40; gx += 46) {
        for (var k = 0; k < 4; k++) {
          var x = gx + k * 7;
          ctx.beginPath(); ctx.moveTo(x, gy); ctx.lineTo(x - 7, gy + 27); ctx.stroke();
        }
      }
    }
  }
  function yanagi(t) {
    ctx.lineWidth = 1.3; ctx.lineCap = 'round';
    for (var gx = 10; gx < W + 30; gx += 42) {
      for (var k = 0; k < 4; k++) {
        var x0 = gx + k * 8;
        ctx.strokeStyle = t.fg;
        ctx.beginPath();
        for (var y = -4; y <= H + 4; y += 6) { var xx = x0 + Math.sin(y * .045 + gx * 1.3 + k * 1.7) * 3.2; if (y === -4) ctx.moveTo(xx, y); else ctx.lineTo(xx, y); }
        ctx.stroke();
        ctx.strokeStyle = t.mid;
        for (var y2 = 10 + (k % 2) * 6; y2 < H; y2 += 13) {
          var xx2 = x0 + Math.sin(y2 * .045 + gx * 1.3 + k * 1.7) * 3.2;
          ctx.beginPath(); ctx.moveTo(xx2, y2); ctx.lineTo(xx2 + (k % 2 ? 4.8 : -4.8), y2 + 4.6); ctx.stroke();
        }
      }
    }
  }
  function raimon(t) {
    var s = 36;
    ctx.lineWidth = 2.6; ctx.strokeStyle = t.fg; ctx.lineJoin = 'miter';
    for (var y = 0; y < H + s; y += s) for (var x = 0; x < W + s; x += s) {
      ctx.beginPath();
      ctx.moveTo(x + 3, y + 33); ctx.lineTo(x + 33, y + 33); ctx.lineTo(x + 33, y + 3); ctx.lineTo(x + 11, y + 3); ctx.lineTo(x + 11, y + 25); ctx.lineTo(x + 25, y + 25); ctx.lineTo(x + 25, y + 11); ctx.lineTo(x + 17, y + 11);
      ctx.stroke();
    }
  }
  function kojitsunagi(t) {
    var s = 34;
    ctx.lineWidth = 4.4; ctx.strokeStyle = t.fg; ctx.lineCap = 'square';
    var row = 0;
    for (var y = s / 2; y < H + s; y += s, row++) {
      for (var x = s / 2; x < W + s; x += s) {
        var rot = ((Math.round(x / s) + row) % 2) * Math.PI / 2;
        ctx.save(); ctx.translate(x, y); ctx.rotate(rot);
        ctx.beginPath();
        ctx.moveTo(-13, -11); ctx.lineTo(13, -11);
        ctx.moveTo(-13, 11); ctx.lineTo(13, 11);
        ctx.moveTo(0, -11); ctx.lineTo(0, 11);
        ctx.stroke(); ctx.restore();
      }
    }
  }
  function manjitsunagi(t) {
    var s = 35;
    ctx.lineWidth = 2.4; ctx.strokeStyle = t.fg; ctx.lineCap = 'square';
    for (var y = s / 2; y < H + s; y += s) for (var x = s / 2; x < W + s; x += s) {
      for (var k = 0; k < 4; k++) {
        ctx.save(); ctx.translate(x, y); ctx.rotate(Math.PI / 2 * k);
        ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(11.5, 0); ctx.lineTo(11.5, 8.5); ctx.stroke();
        ctx.restore();
      }
    }
  }
  function igeta(t) {
    ctx.strokeStyle = t.fg; ctx.lineWidth = 3;
    ctx.beginPath();
    for (var x = 23; x < W + 46; x += 46) { ctx.moveTo(x - 5, 0); ctx.lineTo(x - 5, H); ctx.moveTo(x + 5, 0); ctx.lineTo(x + 5, H); }
    for (var y = 23; y < H + 46; y += 46) { ctx.moveTo(0, y - 5); ctx.lineTo(W, y - 5); ctx.moveTo(0, y + 5); ctx.lineTo(W, y + 5); }
    ctx.stroke();
  }
  function mansuji(t) {
    ctx.lineWidth = 1;
    for (var x = 0; x < W; x += 5) {
      ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H);
      ctx.strokeStyle = x % 25 === 0 ? t.fg : t.mid; ctx.stroke();
    }
  }
  function komochijima(t) {
    for (var x = 0; x < W + 38; x += 38) {
      ctx.fillStyle = t.soft; ctx.fillRect(x, 0, 17, H);
      ctx.fillStyle = t.fg; ctx.fillRect(x + 7, 0, 3, H);
      ctx.fillStyle = t.mid; ctx.fillRect(x + 26, 0, 1.4, H);
    }
  }
  function yamaji(t) {
    ctx.lineWidth = 2; ctx.lineJoin = 'miter';
    var row = 0;
    for (var y = 10; y < H + 18; y += 18, row++) {
      ctx.beginPath(); ctx.strokeStyle = row % 2 ? t.mid : t.fg;
      for (var x = 0; x <= W + 16; x += 16) {
        var yy = y + (((x / 16) + row) % 2 ? -6.5 : 6.5);
        if (x === 0) ctx.moveTo(x, yy); else ctx.lineTo(x, yy);
      }
      ctx.stroke();
    }
  }
  function arare(t) {
    function R(n) { var v = Math.sin(n * 127.1) * 43758.5453; return v - Math.floor(v); }
    for (var i = 0; i < 215; i++) {
      var x = R(i * 2 + 1) * W, y = R(i * 2 + 2) * H, r = .8 + R(i * 3 + 5) * 2.7;
      ctx.beginPath(); ctx.arc(x, y, r, 0, 7);
      ctx.fillStyle = R(i * 5) > .35 ? t.fg : t.mid;
      ctx.globalAlpha = .55 + R(i * 7) * .45;
      ctx.fill(); ctx.globalAlpha = 1;
    }
  }
  function hyoretsu(t) {
    function R(n) { var v = Math.sin(n * 91.7) * 24634.63; return v - Math.floor(v); }
    ctx.lineWidth = 1.1; ctx.strokeStyle = t.mid;
    for (var gx = 0; gx <= W + 26; gx += 26) {
      ctx.beginPath();
      for (var y = 0; y <= H; y += 30) { var x = gx + (R(gx * 3 + y) - .5) * 11; if (y === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y); }
      ctx.stroke();
    }
    for (var gy = 0; gy <= H + 26; gy += 26) {
      ctx.beginPath();
      for (var x2 = 0; x2 <= W; x2 += 30) { var y2 = gy + (R(gy * 5 + x2) - .5) * 11; if (x2 === 0) ctx.moveTo(x2, y2); else ctx.lineTo(x2, y2); }
      ctx.stroke();
    }
  }
  function jujigasuri(t) {
    var s = 34, row = 0;
    ctx.fillStyle = t.fg;
    for (var y = s / 2; y < H + s; y += s, row++) {
      for (var x = s / 2 + (row % 2 ? s / 2 : 0); x < W + s; x += s) {
        ctx.globalAlpha = .9;
        ctx.fillRect(x - 2.2, y - 9.5, 4.4, 19);
        ctx.fillRect(x - 9.5, y - 2.2, 19, 4.4);
        ctx.globalAlpha = 1;
      }
    }
  }
  function igasuri(t) {
    var s = 38, row = 0;
    ctx.lineWidth = 1.8; ctx.strokeStyle = t.fg;
    for (var y = s / 2; y < H + s; y += s, row++) {
      for (var x = s / 2 + (row % 2 ? s / 2 : 0); x < W + s; x += s) {
        ctx.beginPath();
        ctx.moveTo(x - 5, y - 10); ctx.lineTo(x - 5, y + 10);
        ctx.moveTo(x + 5, y - 10); ctx.lineTo(x + 5, y + 10);
        ctx.moveTo(x - 10, y - 5); ctx.lineTo(x + 10, y - 5);
        ctx.moveTo(x - 10, y + 5); ctx.lineTo(x + 10, y + 5);
        ctx.stroke();
      }
    }
  }
  function fundotsunagi(t) {
    var s = 27, row = 0;
    ctx.lineWidth = 1.5; ctx.strokeStyle = t.fg;
    for (var y = s / 2; y < H + s; y += s, row++) {
      for (var x = s / 2 + (row % 2 ? s / 2 : 0); x < W + s; x += s) {
        ctx.save(); ctx.translate(x, y); ctx.rotate(((Math.round(x / s) + row) % 2) * Math.PI / 2);
        ctx.beginPath();
        ctx.moveTo(0, -13);
        ctx.bezierCurveTo(8, -13, 8, -3, 0, 0);
        ctx.bezierCurveTo(8, 3, 8, 13, 0, 13);
        ctx.bezierCurveTo(-8, 13, -8, 3, 0, 0);
        ctx.bezierCurveTo(-8, -3, -8, -13, 0, -13);
        ctx.closePath(); ctx.stroke(); ctx.restore();
      }
    }
  }
  function kusari(t) {
    var s = 27, row = 0;
    for (var y = s / 2; y < H + s; y += s, row++) {
      for (var x = s / 2; x < W + s; x += s) {
        var rot = ((Math.round(x / s) + row) % 2) * Math.PI / 2;
        ctx.beginPath(); ctx.ellipse(x, y, 12, 7.5, rot, 0, 7); ctx.strokeStyle = t.fg; ctx.lineWidth = 1.6; ctx.stroke();
        ctx.beginPath(); ctx.ellipse(x, y, 8.4, 4.4, rot, 0, 7); ctx.strokeStyle = t.mid; ctx.lineWidth = 1.1; ctx.stroke();
      }
    }
  }
  function matsukawabishi(t) {
    var sx = 42;
    ctx.lineWidth = 1.3;
    for (var x = sx / 2; x < W + sx; x += sx) {
      var off = (Math.round(x / sx) % 2) * 8;
      for (var y = -6 + off; y < H + 16; y += 15.5) {
        ctx.beginPath();
        ctx.moveTo(x, y - 13.5); ctx.lineTo(x + 8.5, y); ctx.lineTo(x, y + 13.5); ctx.lineTo(x - 8.5, y); ctx.closePath();
        ctx.fillStyle = t.soft; ctx.fill(); ctx.strokeStyle = t.fg; ctx.stroke();
      }
    }
  }
  function takedabishi(t) {
    var s = 54, row = 0;
    ctx.fillStyle = t.fg;
    for (var y = s / 2; y < H + s; y += s, row++) {
      for (var x = s / 2 + (row % 2 ? s / 2 : 0); x < W + s; x += s) {
        [[-9.8, -9.8], [9.8, -9.8], [-9.8, 9.8], [9.8, 9.8]].forEach(function (o) {
          ctx.beginPath();
          ctx.moveTo(x + o[0], y + o[1] - 9.8); ctx.lineTo(x + o[0] + 9.8, y + o[1]); ctx.lineTo(x + o[0], y + o[1] + 9.8); ctx.lineTo(x + o[0] - 9.8, y + o[1]);
          ctx.closePath(); ctx.globalAlpha = .88; ctx.fill(); ctx.globalAlpha = 1;
        });
        ctx.beginPath(); ctx.arc(x, y, 1.8, 0, 7); ctx.fill();
      }
    }
  }
  function mitsubishi(t) {
    var s = 54, row = 0;
    ctx.fillStyle = t.fg;
    for (var y = s / 2; y < H + s; y += s, row++) {
      for (var x = s / 2 + (row % 2 ? s / 2 : 0); x < W + s; x += s) {
        [[0, -11.5], [-11.5, 9], [11.5, 9]].forEach(function (o) {
          ctx.beginPath();
          ctx.moveTo(x + o[0], y + o[1] - 10.5); ctx.lineTo(x + o[0] + 10.5, y + o[1]); ctx.lineTo(x + o[0], y + o[1] + 10.5); ctx.lineTo(x + o[0] - 10.5, y + o[1]);
          ctx.closePath(); ctx.globalAlpha = .88; ctx.fill(); ctx.globalAlpha = 1;
        });
      }
    }
  }
  function kenhanabishi(t) {
    var s = 58, row = 0;
    for (var y = s / 2; y < H + s; y += s, row++) {
      for (var x = s / 2 + (row % 2 ? s / 2 : 0); x < W + s; x += s) {
        ctx.beginPath();
        ctx.moveTo(x, y - 20); ctx.lineTo(x + 23, y); ctx.lineTo(x, y + 20); ctx.lineTo(x - 23, y); ctx.closePath();
        ctx.strokeStyle = t.fg; ctx.lineWidth = 1.4; ctx.stroke();
        ctx.strokeStyle = t.mid; ctx.lineWidth = 1.1;
        for (var k = 0; k < 4; k++) {
          var a = Math.PI / 2 * k;
          ctx.beginPath(); ctx.ellipse(x + 10 * Math.cos(a), y + 10 * Math.sin(a), k % 2 ? 3 : 7.5, k % 2 ? 7.5 : 3, 0, 0, 7); ctx.stroke();
          ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + 19 * Math.cos(a + Math.PI / 4), y + 19 * Math.sin(a + Math.PI / 4)); ctx.stroke();
        }
        ctx.save(); ctx.translate(x, y); ctx.rotate(Math.PI / 4); ctx.fillStyle = t.fg; ctx.fillRect(-2.6, -2.6, 5.2, 5.2); ctx.restore();
      }
    }
  }
  function nijukikko(t) {
    var R = 23, dx = Math.sqrt(3) * R, dy = 1.5 * R, row = 0;
    ctx.lineWidth = 1.15;
    for (var y = -R; y < H + R; y += dy, row++) {
      for (var x = -dx; x < W + dx; x += dx) {
        var cx = x + (row % 2 ? dx / 2 : 0), cy = y;
        [1, .79, .55].forEach(function (sc, i) {
          ctx.beginPath();
          for (var k = 0; k < 6; k++) { var a = Math.PI / 3 * k - Math.PI / 2, px = cx + R * sc * Math.cos(a), py = cy + R * sc * Math.sin(a); if (k === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py); }
          ctx.closePath(); ctx.strokeStyle = i === 1 ? t.mid : t.fg; ctx.stroke();
        });
      }
    }
  }
  function kikkohanabishi(t) {
    var R = 24, dx = Math.sqrt(3) * R, dy = 1.5 * R, row = 0;
    for (var y = -R; y < H + R; y += dy, row++) {
      for (var x = -dx; x < W + dx; x += dx) {
        var cx = x + (row % 2 ? dx / 2 : 0), cy = y;
        ctx.beginPath();
        for (var k = 0; k < 6; k++) { var a = Math.PI / 3 * k - Math.PI / 2, px = cx + R * Math.cos(a), py = cy + R * Math.sin(a); if (k === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py); }
        ctx.closePath(); ctx.strokeStyle = t.fg; ctx.lineWidth = 1.3; ctx.stroke();
        ctx.strokeStyle = t.mid; ctx.lineWidth = 1.05;
        for (var k2 = 0; k2 < 4; k2++) {
          var a2 = Math.PI / 2 * k2, ex = cx + 6.4 * Math.cos(a2), ey = cy + 6.4 * Math.sin(a2);
          ctx.beginPath(); ctx.ellipse(ex, ey, k2 % 2 ? 2.8 : 4, k2 % 2 ? 4 : 2.8, 0, 0, 7); ctx.stroke();
        }
        ctx.beginPath(); ctx.arc(cx, cy, 1.5, 0, 7); ctx.fillStyle = t.fg; ctx.fill();
      }
    }
  }
  function hanashippo(t) {
    var R = 20;
    ctx.lineWidth = 1.2; ctx.strokeStyle = t.mid;
    for (var y = 0; y < H + R; y += R) for (var x = 0; x < W + R; x += R) { ctx.beginPath(); ctx.arc(x, y, R, 0, 7); ctx.stroke(); }
    for (var y2 = 0; y2 < H + R; y2 += R) for (var x2 = 0; x2 < W + R; x2 += R) {
      for (var k = 0; k < 4; k++) {
        var a = Math.PI / 2 * k + Math.PI / 4;
        ctx.beginPath(); ctx.arc(x2 + 4.4 * Math.cos(a), y2 + 4.4 * Math.sin(a), 3.2, 0, 7); ctx.fillStyle = t.mid; ctx.fill();
      }
      ctx.beginPath(); ctx.arc(x2, y2, 1.4, 0, 7); ctx.fillStyle = t.fg; ctx.fill();
    }
  }
  function amime(t) {
    var st = 29.7;
    ctx.lineWidth = 1.15; ctx.strokeStyle = t.mid;
    ctx.beginPath();
    for (var d = -H; d < W + H; d += st) { ctx.moveTo(d, 0); ctx.lineTo(d + H, H); }
    for (var d2 = 0; d2 < W + 2 * H; d2 += st) { ctx.moveTo(d2, 0); ctx.lineTo(d2 - H, H); }
    ctx.stroke();
    ctx.strokeStyle = t.fg; ctx.lineWidth = 1.2;
    for (var gy = 0; gy <= H + st; gy += st / 2) for (var gx = 0; gx <= W + st; gx += st / 2) {
      var ix = Math.round(gx / (st / 2)), iy = Math.round(gy / (st / 2));
      if ((ix + iy) % 2) continue;
      ctx.beginPath(); ctx.arc(gx, gy, 2.7, 0, 7); ctx.stroke();
    }
  }
  function kakutoshi(t) {
    var s = 13.5, row = 0;
    ctx.fillStyle = t.fg;
    for (var y = s / 2; y < H + s; y += s, row++) {
      for (var x = s / 2 + (row % 2 ? s / 2 : 0); x < W + s; x += s) ctx.fillRect(x - 2.3, y - 2.3, 4.6, 4.6);
    }
  }
  function ishigaki(t) {
    var bw = 47, bh = 22, row = 0;
    ctx.lineWidth = 1.2;
    for (var y = 0; y < H + bh; y += bh, row++) {
      for (var x = -bw + (row % 2 ? bw / 2 : 0); x < W + bw; x += bw) {
        ctx.beginPath(); ctx.roundRect(x + 1.6, y + 1.6, bw - 3.2, bh - 3.2, 6);
        ctx.fillStyle = t.soft; ctx.fill(); ctx.strokeStyle = t.fg; ctx.stroke();
      }
    }
  }
  function takegaki(t) {
    ctx.lineWidth = 1.5; ctx.strokeStyle = t.fg;
    ctx.beginPath();
    for (var x = 4; x < W + 13; x += 13) { ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.moveTo(x + 6, 0); ctx.lineTo(x + 6, H); }
    ctx.stroke();
    for (var ty = 20; ty < H; ty += 76) {
      ctx.fillStyle = t.soft; ctx.fillRect(0, ty, W, 9);
      ctx.strokeStyle = t.fg; ctx.lineWidth = 1.2; ctx.strokeRect(-2, ty, W + 4, 9);
      ctx.fillStyle = t.fg;
      for (var kx = 10; kx < W; kx += 26) { ctx.beginPath(); ctx.arc(kx, ty + 4.5, 1.7, 0, 7); ctx.fill(); }
      ctx.lineWidth = 1.5;
    }
  }
  function senbongoshi(t) {
    ctx.lineWidth = 1; ctx.strokeStyle = t.mid;
    ctx.beginPath();
    for (var x = 0; x < W; x += 7) { ctx.moveTo(x, 0); ctx.lineTo(x, H); }
    ctx.stroke();
    ctx.fillStyle = t.fg;
    for (var x2 = 0; x2 < W + 49; x2 += 49) ctx.fillRect(x2 - 1.3, 0, 2.6, H);
    for (var y = 0; y < H + 49; y += 49) ctx.fillRect(0, y - 1.3, W, 2.6);
  }
  function hakarakusa(t) {
    var bh = 46;
    ctx.lineWidth = 1.5; ctx.lineCap = 'round';
    for (var r = 0; r * bh < H + bh; r++) {
      var base = r * bh + 24;
      ctx.strokeStyle = t.fg;
      ctx.beginPath();
      for (var x = 0; x <= W; x += 6) { var y = base + Math.sin(x * .05 + r * 2.2) * 5; if (x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y); }
      ctx.stroke();
      for (var x2 = 16 + (r % 2) * 22; x2 < W; x2 += 44) {
        var y2 = base + Math.sin(x2 * .05 + r * 2.2) * 5, up = ((x2 / 44 + r) % 2) === 0;
        ctx.beginPath(); ctx.ellipse(x2, y2 + (up ? -8 : 8), 3.8, 8, up ? -.5 : .5 + Math.PI, 0, 7);
        ctx.fillStyle = t.soft; ctx.fill(); ctx.strokeStyle = t.fg; ctx.stroke();
      }
    }
  }
  function noshi(t) {
    ctx.save();
    ctx.translate(W / 2, H / 2); ctx.rotate(-.42); ctx.translate(-W / 2, -H / 2);
    for (var y = -60; y < H + 120; y += 36) {
      ctx.beginPath(); ctx.rect(-60, y, W + 120, 15);
      ctx.fillStyle = t.soft; ctx.fill(); ctx.strokeStyle = t.fg; ctx.lineWidth = 1.2; ctx.stroke();
      ctx.beginPath(); ctx.moveTo(-60, y + 5); ctx.lineTo(W + 60, y + 5); ctx.moveTo(-60, y + 10); ctx.lineTo(W + 60, y + 10);
      ctx.strokeStyle = t.mid; ctx.stroke();
      ctx.beginPath(); ctx.moveTo(-46, y); ctx.lineTo(-32, y + 15); ctx.lineTo(-46, y + 15); ctx.closePath();
      ctx.fillStyle = t.fg; ctx.globalAlpha = .75; ctx.fill(); ctx.globalAlpha = 1;
    }
    ctx.restore();
  }
  function tabanenoshi(t) {
    var sx = 56;
    ctx.lineWidth = 1.4; ctx.lineCap = 'round';
    for (var x = sx / 2; x < W + sx; x += sx) {
      var col = Math.round(x / sx);
      [-4.5, 0, 4.5].forEach(function (o) {
        ctx.beginPath(); ctx.strokeStyle = t.fg;
        for (var y = 0; y <= H; y += 6) { var xx = x + o + Math.sin(y * .05 + col * 2 + o) * 1.6; if (y === 0) ctx.moveTo(xx, y); else ctx.lineTo(xx, y); }
        ctx.stroke();
      });
      var ky = 30 + (col % 2) * 52;
      ctx.fillStyle = t.fg; ctx.fillRect(x - 8, ky, 16, 6.5);
      ctx.fillStyle = t.mid; ctx.fillRect(x - 8, ky + 34, 16, 6.5);
    }
  }
  function maruuroko(t) {
    var R = 15;
    ctx.lineWidth = 1.25;
    var row = 0;
    for (var y = 6; y < H + R; y += R * .88, row++) {
      for (var x = -R + (row % 2 ? R : 0); x < W + R; x += R * 2) {
        ctx.beginPath(); ctx.arc(x, y, R, 0, 7);
        ctx.fillStyle = row % 2 ? t.bg : t.soft; ctx.fill();
        ctx.strokeStyle = t.fg; ctx.stroke();
      }
    }
  }
  function dandigai(t) {
    var w = 37, h = 24, row = 0;
    ctx.fillStyle = t.fg;
    for (var y = 0; y < H + h; y += h, row++) {
      for (var x = -w + (row % 2 ? w / 2 : 0); x < W + w; x += w) {
        if ((Math.round(x / w) + row) % 2) continue;
        ctx.globalAlpha = .92; ctx.fillRect(x + .75, y + .75, w - 1.5, h - 1.5); ctx.globalAlpha = 1;
      }
    }
  }
  function ishidatami(t) {
    var s = 36, row = 0;
    ctx.lineWidth = 1.2;
    for (var y = 0; y < H + s; y += s, row++) {
      for (var x = 0; x < W + s; x += s) {
        var dark = (Math.round(x / s) + row) % 2;
        ctx.fillStyle = dark ? t.fg : t.bg;
        ctx.globalAlpha = dark ? .92 : 1;
        ctx.fillRect(x, y, s, s); ctx.globalAlpha = 1;
        ctx.strokeStyle = dark ? t.bg : t.fg;
        ctx.strokeRect(x + 5, y + 5, s - 10, s - 10);
      }
    }
  }
  function koshi(t) {
    ctx.strokeStyle = t.fg; ctx.lineWidth = 1.5;
    ctx.beginPath();
    for (var x = 0; x <= W; x += 24) { ctx.moveTo(x, 0); ctx.lineTo(x, H); }
    for (var y = 0; y <= H; y += 24) { ctx.moveTo(0, y); ctx.lineTo(W, y); }
    ctx.stroke();
  }
  function nanamegoshi(t) {
    var st = 34;
    ctx.lineWidth = 1.3; ctx.strokeStyle = t.fg;
    ctx.beginPath();
    for (var d = -H; d < W + H; d += st) { ctx.moveTo(d, 0); ctx.lineTo(d + H, H); }
    for (var d2 = 0; d2 < W + 2 * H; d2 += st) { ctx.moveTo(d2, 0); ctx.lineTo(d2 - H, H); }
    ctx.stroke();
  }
  function yotsumeami(t) {
    var s = 31, row = 0;
    ctx.lineWidth = 1.3;
    for (var y = 0; y < H + s; y += s, row++) {
      for (var x = 0; x < W + s; x += s) {
        var alt = (Math.round(x / s) + row) % 2;
        ctx.fillStyle = t.soft; ctx.fillRect(x + 1, y + 1, s - 2, s - 2);
        ctx.strokeStyle = t.fg;
        ctx.strokeRect(x + 1, y + 1, s - 2, s - 2);
        ctx.strokeStyle = t.mid;
        if (alt) { ctx.strokeRect(x + 7, y - 3, s - 14, s + 6); } else { ctx.strokeRect(x - 3, y + 7, s + 6, s - 14); }
      }
    }
  }
  function goma(t) {
    ctx.fillStyle = t.fg;
    var row = 0;
    for (var y = 5; y < H + 8; y += 9, row++) {
      for (var x = 5 + (row % 2 ? 4.5 : 0); x < W + 8; x += 9) {
        ctx.beginPath(); ctx.arc(x, y, 1.35, 0, 7); ctx.globalAlpha = .8; ctx.fill(); ctx.globalAlpha = 1;
      }
    }
  }
  function chidorigoshi(t) {
    var s = 18, row = 0;
    ctx.fillStyle = t.fg;
    for (var y = 0; y < H + s * 2; y += s * 2, row++) {
      for (var x = 0; x < W + s * 2; x += s * 2) {
        var cx = x + (row % 2 ? s : 0);
        ctx.globalAlpha = .92;
        ctx.fillRect(cx, y, s, s);
        ctx.beginPath();
        ctx.moveTo(cx + s, y + s * .45); ctx.lineTo(cx + s * 1.55, y + s); ctx.lineTo(cx + s, y + s * 1.55); ctx.lineTo(cx + s * .45, y + s);
        ctx.closePath(); ctx.fill();
        ctx.globalAlpha = 1;
      }
    }
  }
  function sensuji(t) {
    ctx.lineWidth = 1;
    for (var gx = 0; gx < W + 34; gx += 34) {
      for (var k = 0; k < 6; k++) {
        var x = gx + k * 3.4;
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H);
        ctx.strokeStyle = k === 0 ? t.fg : t.mid; ctx.stroke();
      }
    }
  }
  function koshijima(t) {
    ctx.globalAlpha = .55;
    ctx.fillStyle = t.mid;
    for (var x = 0; x < W + 32; x += 32) ctx.fillRect(x, 0, 15, H);
    for (var y = 0; y < H + 32; y += 32) ctx.fillRect(0, y, W, 15);
    ctx.globalAlpha = 1;
  }
  function dandan(t) {
    var bh = 21;
    for (var r = 0; r * bh < H + bh; r++) {
      var off = (r * 23) % 69;
      for (var x = -69 + off; x < W + 69; x += 69) {
        ctx.fillStyle = r % 2 ? t.soft : t.mid;
        ctx.globalAlpha = r % 2 ? 1 : .6;
        ctx.fillRect(x, r * bh + 1.5, 66, bh - 3);
        ctx.globalAlpha = 1;
      }
    }
  }
  function hishigasane(t) {
    var row = 0;
    ctx.lineWidth = 1.3; ctx.strokeStyle = t.fg;
    for (var y = 14; y < H + 28; y += 27, row++) {
      for (var x = -18 + (row % 2 ? 15 : 0); x < W + 30; x += 30) {
        ctx.beginPath();
        ctx.moveTo(x, y - 13); ctx.lineTo(x + 17, y); ctx.lineTo(x, y + 13); ctx.lineTo(x - 17, y); ctx.closePath();
        ctx.stroke();
      }
    }
  }
  function irekobishi(t) {
    var sx = 34, sy = 30, row = 0;
    ctx.lineWidth = 1.15;
    for (var y = sy / 2; y < H + sy; y += sy, row++) {
      for (var x = sx / 2 + (row % 2 ? sx / 2 : 0); x < W + sx; x += sx) {
        [1, .66, .36].forEach(function (sc, i) {
          ctx.beginPath();
          ctx.moveTo(x, y - 13 * sc); ctx.lineTo(x + 15 * sc, y); ctx.lineTo(x, y + 13 * sc); ctx.lineTo(x - 15 * sc, y); ctx.closePath();
          ctx.strokeStyle = i === 1 ? t.mid : t.fg; ctx.stroke();
        });
      }
    }
  }
  function suimon(t) {
    ctx.lineCap = 'round';
    for (var r = 0; r * 16 < H + 16; r++) {
      var base = r * 16 + 8;
      ctx.beginPath(); ctx.strokeStyle = r % 2 ? t.mid : t.fg; ctx.lineWidth = r % 2 ? 1.2 : 1.7;
      for (var x = 0; x <= W; x += 6) { var y = base + Math.sin(x * .028 + r * 1.3) * 4.6; if (x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y); }
      ctx.stroke();
    }
  }
  function kikkogasuri(t) {
    var s = 32, row = 0;
    ctx.lineWidth = 2.6; ctx.strokeStyle = t.fg;
    for (var y = s / 2; y < H + s; y += s, row++) {
      for (var x = s / 2 + (row % 2 ? s / 2 : 0); x < W + s; x += s) {
        ctx.beginPath();
        for (var k = 0; k < 6; k++) { var a = Math.PI / 3 * k - Math.PI / 2, px = x + 10.5 * Math.cos(a), py = y + 10.5 * Math.sin(a); if (k === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py); }
        ctx.closePath(); ctx.stroke();
      }
    }
  }
  function takeami(t) {
    var s = 25, row = 0;
    ctx.lineWidth = 1.15;
    for (var y = 0; y < H + s; y += s, row++) {
      for (var x = 0; x < W + s; x += s) {
        var horiz = (Math.round(x / s) + row) % 2 === 0;
        ctx.beginPath();
        if (horiz) ctx.roundRect(x + 1, y + s / 2 - 6.5, s - 2, 13, 6);
        else ctx.roundRect(x + s / 2 - 6.5, y + 1, 13, s - 2, 6);
        ctx.fillStyle = t.soft; ctx.fill(); ctx.strokeStyle = t.fg; ctx.stroke();
      }
    }
  }
  function sankakugoshi(t) {
    var h = 22, st = h * 1.732;
    ctx.lineWidth = 1.25; ctx.strokeStyle = t.fg;
    ctx.beginPath();
    for (var y = 0; y <= H; y += h) { ctx.moveTo(0, y); ctx.lineTo(W, y); }
    for (var d = -H; d < W + H; d += st) { ctx.moveTo(d, 0); ctx.lineTo(d + H * .577, H); }
    for (var d2 = 0; d2 < W + 2 * H; d2 += st) { ctx.moveTo(d2, 0); ctx.lineTo(d2 - H * .577, H); }
    ctx.stroke();
  }
  function kasaneshikaku(t) {
    var s = 32, row = 0;
    ctx.lineWidth = 1.2;
    for (var y = s / 2; y < H + s; y += s, row++) {
      for (var x = s / 2 + (row % 2 ? s / 2 : 0); x < W + s; x += s) {
        ctx.strokeStyle = t.fg;
        ctx.strokeRect(x - 11, y - 11, 22, 22);
        ctx.save(); ctx.translate(x, y); ctx.rotate(Math.PI / 4); ctx.strokeStyle = t.mid; ctx.strokeRect(-11, -11, 22, 22); ctx.restore();
      }
    }
  }
  function uzutsunagi(t) {
    var sx = 37, sy = 40, row = 0;
    ctx.lineWidth = 1.6; ctx.lineCap = 'round'; ctx.strokeStyle = t.fg;
    for (var y = sy / 2; y < H + sy; y += sy, row++) {
      for (var x = sx / 2 + (row % 2 ? sx / 2 : 0); x < W + sx; x += sx) {
        ctx.beginPath();
        for (var a = 0; a <= Math.PI * 4.4; a += .24) {
          var r = .7 + a * 1.28, px = x + r * Math.cos(a), py = y + r * Math.sin(a);
          if (a === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
        }
        ctx.stroke();
        ctx.beginPath(); ctx.arc(x + sx / 2, y - 6, sx / 2 - 4, Math.PI * 1.15, Math.PI * 1.85); ctx.strokeStyle = t.mid; ctx.stroke();
        ctx.strokeStyle = t.fg;
      }
    }
  }
  function mizutama(t) {
    var s = 31, row = 0;
    ctx.fillStyle = t.fg;
    for (var y = s / 2; y < H + s; y += s, row++) {
      for (var x = s / 2 + (row % 2 ? s / 2 : 0); x < W + s; x += s) {
        ctx.beginPath(); ctx.arc(x, y, 5.2, 0, 7); ctx.globalAlpha = .88; ctx.fill(); ctx.globalAlpha = 1;
        ctx.beginPath(); ctx.arc(x + s / 2, y + (row % 2 ? 0 : s / 2), 2.1, 0, 7); ctx.fillStyle = t.mid; ctx.fill(); ctx.fillStyle = t.fg;
      }
    }
  }
  function futojima(t) {
    for (var x = 0; x < W + 36; x += 36) {
      ctx.fillStyle = t.fg; ctx.globalAlpha = .92; ctx.fillRect(x, 0, 17, H); ctx.globalAlpha = 1;
      ctx.fillStyle = t.mid; ctx.fillRect(x + 22, 0, 1.6, H); ctx.fillRect(x + 26.5, 0, 1.6, H);
    }
  }
  function nanameichimatsu(t) {
    ctx.save();
    ctx.translate(W / 2, H / 2); ctx.rotate(Math.PI / 4); ctx.translate(-W / 2, -H / 2);
    var s = 23;
    ctx.fillStyle = t.fg;
    for (var y = -W; y < H + W; y += s) {
      for (var x = -W; x < W * 2; x += s) {
        if ((Math.round(x / s) + Math.round(y / s)) % 2) continue;
        ctx.globalAlpha = .92; ctx.fillRect(x, y, s, s); ctx.globalAlpha = 1;
      }
    }
    ctx.restore();
  }
  function midareishigaki(t) {
    function R(n) { var v = Math.sin(n * 47.3) * 12345.67; return v - Math.floor(v); }
    var bh = 22, row = 0;
    ctx.lineWidth = 1.2;
    for (var y = 0; y < H + bh; y += bh, row++) {
      var x = -8 - R(row * 3) * 20;
      var k = 0;
      while (x < W + 10) {
        var wdt = 30 + R(row * 31 + k * 7) * 30;
        ctx.beginPath(); ctx.roundRect(x + 1.6, y + 1.6, wdt - 3.2, bh - 3.2, 6);
        ctx.fillStyle = t.soft; ctx.fill(); ctx.strokeStyle = t.fg; ctx.stroke();
        x += wdt; k++;
      }
    }
  }
  function kasanesankaku(t) {
    var s = 31, hh = s * .866;
    ctx.lineWidth = 1.25; ctx.strokeStyle = t.fg;
    var row = 0;
    for (var y = 4; y < H + hh; y += hh, row++) {
      for (var x = -s + (row % 2 ? s / 2 : 0); x < W + s; x += s) {
        ctx.beginPath();
        ctx.moveTo(x, y + hh); ctx.lineTo(x + s / 2, y); ctx.lineTo(x + s, y + hh); ctx.closePath(); ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(x + s / 2, y); ctx.lineTo(x + s, y + hh); ctx.lineTo(x, y + hh); ctx.closePath();
        ctx.strokeStyle = t.mid; ctx.stroke(); ctx.strokeStyle = t.fg;
      }
    }
  }
  function mikazuki(t) {
    var sx = 40, sy = 38, row = 0;
    ctx.fillStyle = t.fg;
    for (var y = sy / 2; y < H + sy; y += sy, row++) {
      for (var x = sx / 2 + (row % 2 ? sx / 2 : 0); x < W + sx; x += sx) {
        var dir = row % 2 ? -1 : 1;
        ctx.beginPath();
        ctx.arc(x, y, 11.5, 0, 7);
        ctx.fill();
        ctx.beginPath();
        ctx.arc(x + dir * 5, y - 2.5, 9.4, 0, 7);
        ctx.fillStyle = t.bg; ctx.fill(); ctx.fillStyle = t.fg;
      }
    }
  }
  function kakutsunagi(t) {
    var s = 30, row = 0;
    ctx.lineWidth = 1.5; ctx.strokeStyle = t.fg;
    for (var y = s / 2; y < H + s; y += s, row++) {
      for (var x = s / 2 + (row % 2 ? s / 2 : 0); x < W + s; x += s) {
        ctx.strokeRect(x - 10, y - 10, 20, 20);
        ctx.save(); ctx.translate(x + s / 2, y + s / 2); ctx.rotate(Math.PI / 4); ctx.strokeStyle = t.mid; ctx.strokeRect(-6, -6, 12, 12); ctx.restore();
        ctx.strokeStyle = t.fg;
      }
    }
  }
  function ayaori(t) {
    var s = 6;
    ctx.fillStyle = t.fg;
    for (var y = 0; y < H; y += s) {
      for (var x = 0; x < W; x += s) {
        var m = ((Math.round(x / s) - Math.round(y / s)) % 4 + 4) % 4;
        if (m < 2) { ctx.globalAlpha = .75; ctx.fillRect(x, y, s, s); ctx.globalAlpha = 1; }
      }
    }
  }
  function sorobandama(t) {
    ctx.lineWidth = 1.3;
    for (var y = 18; y < H + 30; y += 31) {
      ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.strokeStyle = t.mid; ctx.stroke();
      for (var x = 14; x < W + 26; x += 27) {
        ctx.beginPath();
        ctx.moveTo(x - 10.5, y); ctx.lineTo(x - 4, y - 6.5); ctx.lineTo(x + 4, y - 6.5); ctx.lineTo(x + 10.5, y); ctx.lineTo(x + 4, y + 6.5); ctx.lineTo(x - 4, y + 6.5); ctx.closePath();
        ctx.fillStyle = t.soft; ctx.fill(); ctx.strokeStyle = t.fg; ctx.stroke();
      }
    }
  }
  function kikkokuzushi(t) {
    var R = 22, dx = Math.sqrt(3) * R, dy = 1.5 * R, row = 0;
    ctx.lineWidth = 1.25; ctx.strokeStyle = t.fg;
    for (var y = -R; y < H + R * 2; y += dy, row++) {
      for (var x = -dx; x < W + dx; x += dx) {
        var cx = x + (row % 2 ? dx / 2 : 0);
        var cy = y + ((Math.round(x / dx) % 2) ? R * .38 : 0);
        ctx.beginPath();
        for (var k = 0; k < 6; k++) { var a = Math.PI / 3 * k - Math.PI / 2, px = cx + R * Math.cos(a), py = cy + R * Math.sin(a); if (k === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py); }
        ctx.closePath(); ctx.stroke();
      }
    }
  }
  function wagasane(t) {
    var row = 0;
    ctx.lineWidth = 1.3;
    for (var y = 16; y < H + 28; y += 27, row++) {
      for (var x = -12 + (row % 2 ? 12 : 0); x < W + 24; x += 24) {
        ctx.beginPath(); ctx.arc(x, y, 15, 0, 7); ctx.strokeStyle = t.fg; ctx.stroke();
        ctx.beginPath(); ctx.arc(x, y, 10.5, 0, 7); ctx.strokeStyle = t.mid; ctx.stroke();
      }
    }
  }
  function yokojima(t) {
    for (var y = 0; y < H + 30; y += 30) {
      ctx.fillStyle = t.soft; ctx.fillRect(0, y, W, 15);
      ctx.fillStyle = t.mid; ctx.fillRect(0, y + 19, W, 1.6); ctx.fillRect(0, y + 23.5, W, 1.6);
    }
  }
  function sakurakumiko(t) {
    var R = 23, dx = Math.sqrt(3) * R, dy = 1.5 * R, row = 0;
    ctx.lineWidth = 1.15;
    for (var y = -R; y < H + R; y += dy, row++) {
      for (var x = -dx; x < W + dx; x += dx) {
        var cx = x + (row % 2 ? dx / 2 : 0), cy = y;
        var v = [];
        for (var k = 0; k < 6; k++) { var a = Math.PI / 3 * k - Math.PI / 2; v.push([cx + R * Math.cos(a), cy + R * Math.sin(a)]); }
        ctx.strokeStyle = t.fg;
        ctx.beginPath();
        v.forEach(function (p, i) { if (i === 0) ctx.moveTo(p[0], p[1]); else ctx.lineTo(p[0], p[1]); });
        ctx.closePath(); ctx.stroke();
        ctx.strokeStyle = t.mid;
        for (var k2 = 0; k2 < 3; k2++) {
          ctx.beginPath(); ctx.moveTo(v[k2 * 2][0], v[k2 * 2][1]); ctx.lineTo(v[k2 * 2 + 3 > 5 ? k2 * 2 - 3 : k2 * 2 + 3][0], v[k2 * 2 + 3 > 5 ? k2 * 2 - 3 : k2 * 2 + 3][1]); ctx.stroke();
        }
        ctx.beginPath();
        for (var k3 = 0; k3 < 6; k3++) { var a3 = Math.PI / 3 * k3, px = cx + R * .42 * Math.cos(a3), py = cy + R * .42 * Math.sin(a3); if (k3 === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py); }
        ctx.closePath(); ctx.strokeStyle = t.fg; ctx.stroke();
      }
    }
  }
  function chigaitatewaku(t) {
    ctx.lineWidth = 1.6;
    var xs = [0];
    var widths = [15, 27];
    var acc = 0, wi = 0;
    while (acc < W + 40) { acc += widths[wi % 2]; xs.push(acc); wi++; }
    xs.forEach(function (cx, i) {
      [0, 1].forEach(function (k) {
        ctx.beginPath(); ctx.strokeStyle = k ? t.mid : t.fg;
        for (var y = 0; y <= H; y += 6) {
          var x = cx + 6 + k * (widths[i % 2] * .42) + Math.sin(y * .026 + k * Math.PI + i) * 5.4;
          if (y === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
        }
        ctx.stroke();
      });
    });
  }
  function chigaibishi(t) {
    var s = 31, row = 0;
    ctx.fillStyle = t.fg;
    for (var y = s / 2; y < H + s; y += s, row++) {
      for (var x = s / 2; x < W + s; x += s) {
        var big = (Math.round(x / s) + row) % 2 === 0, r = big ? 12.5 : 6.5;
        ctx.beginPath();
        ctx.moveTo(x, y - r); ctx.lineTo(x + r, y); ctx.lineTo(x, y + r); ctx.lineTo(x - r, y); ctx.closePath();
        ctx.globalAlpha = big ? .92 : .6; ctx.fill(); ctx.globalAlpha = 1;
      }
    }
  }
  function kasanegoshi(t) {
    ctx.lineWidth = 1;
    [0, 9].forEach(function (off, oi) {
      ctx.strokeStyle = oi ? t.mid : t.fg;
      ctx.beginPath();
      for (var x = off; x <= W + 18; x += 18) { ctx.moveTo(x, 0); ctx.lineTo(x, H); }
      for (var y = off; y <= H + 18; y += 18) { ctx.moveTo(0, y); ctx.lineTo(W, y); }
      ctx.stroke();
    });
    ctx.fillStyle = t.fg;
    for (var gy = 0; gy <= H; gy += 18) for (var gx = 0; gx <= W; gx += 18) { ctx.beginPath(); ctx.arc(gx, gy, 1.3, 0, 7); ctx.fill(); }
  }
  function nanameyagasuri(t) {
    ctx.save();
    ctx.translate(W / 2, H / 2); ctx.rotate(-Math.PI / 5); ctx.translate(-W / 2, -H / 2);
    var w = 24, h = 46, row = 0;
    for (var y = -H; y < H * 2 + h; y += h * .8, row++) {
      for (var x = -W * .5; x < W * 1.5 + w; x += w) {
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
        ctx.globalAlpha = .88; ctx.fill(); ctx.globalAlpha = 1;
      }
    }
    ctx.restore();
  }
  function tsurugoshi(t) {
    ctx.lineWidth = 1.35; ctx.strokeStyle = t.fg;
    for (var gx = 0; gx <= W + 26; gx += 26) {
      ctx.beginPath();
      for (var y = 0; y <= H; y += 6) { var x = gx + Math.sin(y * .05 + gx) * 3; if (y === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y); }
      ctx.stroke();
    }
    ctx.strokeStyle = t.mid;
    for (var gy = 0; gy <= H + 26; gy += 26) {
      ctx.beginPath();
      for (var x2 = 0; x2 <= W; x2 += 6) { var y2 = gy + Math.sin(x2 * .05 + gy * 1.7) * 3; if (x2 === 0) ctx.moveTo(x2, y2); else ctx.lineTo(x2, y2); }
      ctx.stroke();
    }
  }
  function kasumigasane(t) {
    var bh = 46;
    ctx.fillStyle = t.mid;
    for (var r = 0; r * bh < H + bh; r++) {
      var off = (r % 2) * 64;
      for (var x = -70 + off; x < W + 70; x += 128) {
        ctx.globalAlpha = .5;
        ctx.beginPath(); ctx.roundRect(x, r * bh + 8, 92, 8.5, 4.25); ctx.fill();
        ctx.beginPath(); ctx.roundRect(x + 14, r * bh + 21, 92, 8.5, 4.25); ctx.fill();
        ctx.globalAlpha = 1;
      }
    }
  }
  function kumogasane(t) {
    var R = 17, row = 0;
    ctx.lineWidth = 1.35;
    for (var y = R + 4; y < H + R * 2; y += R * 1.12, row++) {
      for (var x = -R + (row % 2 ? R : 0); x < W + R; x += R * 2) {
        ctx.beginPath();
        ctx.arc(x, y, R, Math.PI, 0);
        ctx.lineTo(x + R, y + 5); ctx.lineTo(x - R, y + 5); ctx.closePath();
        ctx.fillStyle = row % 2 ? t.bg : t.soft; ctx.fill();
        ctx.strokeStyle = t.fg; ctx.stroke();
        ctx.beginPath(); ctx.arc(x, y, R * .58, Math.PI, 0); ctx.strokeStyle = t.mid; ctx.stroke();
      }
    }
  }
  function futogoshi(t) {
    ctx.fillStyle = t.fg;
    for (var x = 0; x < W + 36; x += 36) ctx.fillRect(x - 2.6, 0, 5.2, H);
    for (var y = 0; y < H + 36; y += 36) ctx.fillRect(0, y - 2.6, W, 5.2);
    ctx.fillStyle = t.bg;
    for (var gy = 0; gy <= H; gy += 36) for (var gx = 0; gx <= W; gx += 36) ctx.fillRect(gx - 1.4, gy - 1.4, 2.8, 2.8);
  }
  function ichimatsujima(t) {
    var bw = 54, s = 13.5;
    ctx.fillStyle = t.fg;
    for (var bx = 0; bx < W + bw; bx += bw) {
      for (var y = 0; y < H + s; y += s) {
        for (var x = bx; x < bx + bw; x += s) {
          if ((Math.round(x / s) + Math.round(y / s)) % 2) continue;
          ctx.globalAlpha = .92; ctx.fillRect(x, y, s, s); ctx.globalAlpha = 1;
        }
      }
      ctx.fillStyle = t.mid; ctx.fillRect(bx + bw - 1, 0, 2, H); ctx.fillStyle = t.fg;
    }
  }
  function irekoasanoha(t) {
    var R = 25, dx = Math.sqrt(3) * R, dy = 1.5 * R, row = 0;
    ctx.lineWidth = 1.05;
    function leaf(cx, cy, r, inner) {
      var v = [];
      for (var k = 0; k < 6; k++) { var a = Math.PI / 3 * k - Math.PI / 2; v.push([cx + r * Math.cos(a), cy + r * Math.sin(a)]); }
      for (var k2 = 0; k2 < 6; k2++) {
        var A = v[k2], B = v[(k2 + 1) % 6];
        var mx = (A[0] + B[0] + cx) / 3, my = (A[1] + B[1] + cy) / 3;
        ctx.strokeStyle = t.mid;
        ctx.beginPath(); ctx.moveTo(A[0], A[1]); ctx.lineTo(B[0], B[1]); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(A[0], A[1]); ctx.stroke();
        ctx.strokeStyle = t.fg;
        ctx.beginPath(); ctx.moveTo(mx, my); ctx.lineTo(A[0], A[1]); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(mx, my); ctx.lineTo(B[0], B[1]); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(mx, my); ctx.lineTo(cx, cy); ctx.stroke();
      }
      if (inner) leaf(cx, cy, r * .52, false);
    }
    for (var y = -R; y < H + R; y += dy, row++) {
      for (var x = -dx; x < W + dx; x += dx) leaf(x + (row % 2 ? dx / 2 : 0), y, R, true);
    }
  }
  function irekoshippo(t) {
    var R = 20;
    ctx.lineWidth = 1.2; ctx.strokeStyle = t.mid;
    for (var y = 0; y < H + R; y += R) for (var x = 0; x < W + R; x += R) { ctx.beginPath(); ctx.arc(x, y, R, 0, 7); ctx.stroke(); }
    ctx.strokeStyle = t.fg; ctx.lineWidth = 1.1;
    for (var y2 = 0; y2 < H + R; y2 += R) for (var x2 = 0; x2 < W + R; x2 += R) {
      ctx.beginPath(); ctx.arc(x2, y2, 5.2, 0, 7); ctx.stroke();
      ctx.beginPath(); ctx.arc(x2, y2, 1.5, 0, 7); ctx.fillStyle = t.fg; ctx.fill();
    }
    ctx.strokeStyle = t.mid;
    for (var y3 = R / 2; y3 < H + R; y3 += R) for (var x3 = R / 2; x3 < W + R; x3 += R) {
      ctx.beginPath(); ctx.arc(x3, y3, 2.8, 0, 7); ctx.stroke();
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
    ({ seigaiha: seigaiha, asanoha: asanoha, shippo: shippo, ichimatsu: ichimatsu, kikko: kikko, uroko: uroko, same: same, yagasuri: yagasuri, kanoko: kanoko, hishi: hishi, sayagata: sayagata, kagome: kagome, karakusa: karakusa, ryusui: ryusui, tatewaku: tatewaku, yukwa: yukwa, ajiro: ajiro, sankuzushi: sankuzushi, higaki: higaki, hanabishi: hanabishi, watsunagi: watsunagi, bishamon: bishamon, tatenami: tatenami, kanzemizu: kanzemizu, genjigumo: genjigumo, kasumi: kasumi, kumo: kumo, ame: ame, yanagi: yanagi, raimon: raimon, kojitsunagi: kojitsunagi, manjitsunagi: manjitsunagi, igeta: igeta, mansuji: mansuji, komochijima: komochijima, yamaji: yamaji, arare: arare, hyoretsu: hyoretsu, jujigasuri: jujigasuri, igasuri: igasuri, fundotsunagi: fundotsunagi, kusari: kusari, matsukawabishi: matsukawabishi, takedabishi: takedabishi, mitsubishi: mitsubishi, kenhanabishi: kenhanabishi, nijukikko: nijukikko, kikkohanabishi: kikkohanabishi, hanashippo: hanashippo, amime: amime, kakutoshi: kakutoshi, ishigaki: ishigaki, takegaki: takegaki, senbongoshi: senbongoshi, hakarakusa: hakarakusa, noshi: noshi, tabanenoshi: tabanenoshi, maruuroko: maruuroko, dandigai: dandigai, ishidatami: ishidatami, koshi: koshi, nanamegoshi: nanamegoshi, yotsumeami: yotsumeami, goma: goma, chidorigoshi: chidorigoshi, sensuji: sensuji, koshijima: koshijima, dandan: dandan, hishigasane: hishigasane, irekobishi: irekobishi, suimon: suimon, kikkogasuri: kikkogasuri, takeami: takeami, sankakugoshi: sankakugoshi, kasaneshikaku: kasaneshikaku, uzutsunagi: uzutsunagi, mizutama: mizutama, futojima: futojima, nanameichimatsu: nanameichimatsu, midareishigaki: midareishigaki, kasanesankaku: kasanesankaku, mikazuki: mikazuki, kakutsunagi: kakutsunagi, ayaori: ayaori, sorobandama: sorobandama, kikkokuzushi: kikkokuzushi, wagasane: wagasane, yokojima: yokojima, sakurakumiko: sakurakumiko, chigaitatewaku: chigaitatewaku, chigaibishi: chigaibishi, kasanegoshi: kasanegoshi, nanameyagasuri: nanameyagasuri, tsurugoshi: tsurugoshi, kasumigasane: kasumigasane, kumogasane: kumogasane, futogoshi: futogoshi, ichimatsujima: ichimatsujima, irekoasanoha: irekoasanoha, irekoshippo: irekoshippo })[pattern](t);
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
  var search = root.querySelector('.k-wag-search'), count = root.querySelector('.k-wag-count'), none = root.querySelector('.k-wag-none');
  var pbtns = Array.prototype.slice.call(root.querySelectorAll('[data-wag-p]'));
  function applyFilter() {
    var q = (search.value || '').trim().toLowerCase(), shown = 0;
    pbtns.forEach(function (b) {
      var slug = b.getAttribute('data-wag-p');
      var hay = (slug + ' ' + b.textContent + ' ' + (CAPS[slug] || '')).toLowerCase();
      var hit = !q || q.split(/\s+/).every(function (w) { return hay.indexOf(w) !== -1; });
      b.hidden = !hit;
      if (hit) shown++;
    });
    count.textContent = q ? shown + ' / ' + pbtns.length : pbtns.length + ' patterns';
    if (none) none.hidden = shown !== 0;
  }
  if (search) { search.addEventListener('input', applyFilter); applyFilter(); }
  window.addEventListener('resize', draw);
  new MutationObserver(function () { if (picked === null) draw(); }).observe(document.body, { attributes: true, subtree: true, attributeFilter: ['data-theme'] });
  draw();
});
