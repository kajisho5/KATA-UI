// KATA Wagara — one hundred patterns, drawn from their constructions.
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
    chidori: 'Chidori — plovers in flight. Birds that cross rough seas in pairs, drawn as one bold silhouette: a wish for safe passage.',
    kiku: 'Kiku — the chrysanthemum. Sixteen petals around eight, the imperial flower; long life, drawn at sixteen-fold symmetry.',
    sakura: 'Sakura — the cherry blossom. Five petals, each notched at the tip the way the real petal tears; spring, and its brevity.',
    ume: 'Ume — the plum blossom. Five round petals on the branch that blooms in snow; endurance before the spring.',
    fuji: 'Fuji — wisteria. Clusters hanging heavy off the vine, drawn as falling rows of fruit; longevity that droops with plenty.',
    matsuba: 'Matsuba — pine needles. Needles fall in pairs and stay joined, so the pattern wishes a bond that holds to the ground.',
    take: 'Take — bamboo. Jointed stalks that bend and do not break; the nodes are drawn true, one segment at a time.',
    icho: 'Icho — the ginkgo leaf. A fan split down the middle, older than the dinosaurs; drawn with its veins and its notch.',
    momiji: 'Momiji — the maple leaf. Five lobes pointed for autumn; the other spring, the one that burns red.',
    ogi: 'Ogi — the folding fan. Ribs from one pivot, opening wider toward the end: suehiro, a future that fans out.',
    hyotan: 'Hyotan — the gourd. Two round bellies tied at the waist; a charm against drowning and bad luck alike.',
    sekka: 'Sekka — snow flowers. Six-fold crystals, no two alike in the field; here they agree to a grid.',
    hoshi: 'Hoshi — stars. Five-pointed and small, scattered like the winter sky over a plain ground.',
    kanzemizu: 'Kanzemizu — the Kanze school water. Great slow swirls named for a Noh house; water that turns and remembers.',
    uzu: 'Uzu — the whirlpool. One line spiralling in; the sea at Naruto, turning without malice.',
    tomoe: 'Tomoe — the comma swirl. Three commas chasing inside a ring; water, war and warding, turning as one.',
    genjigumo: 'Genjigumo — Genji clouds. Long cloud bands with a curled end, named for the Tale of Genji chapter screens.',
    kasumi: 'Kasumi — mist. Flat bands drifting at offsets; the pattern for everything half-seen and better for it.',
    kumo: 'Kumo — clouds. Single arcs in rows, the scalloped edge of a cloud bank, drawn out to the horizon.',
    ame: 'Ame — rain. Slanted strokes in companies, the way rain actually arrives: together, and at an angle.',
    shibakusa: 'Shibakusa — lawn grass. Five blades to a tuft and a bead of dew; the ground, paying attention.',
    wakamatsu: 'Wakamatsu — the young pine. A fan of needles from one tie; new growth, celebrated at the new year.',
    kikusui: 'Kikusui — chrysanthemum on water. A half-bloom riding two wave lines; the crest of Kusunoki, loyalty afloat.',
    hamon: 'Hamon — ripples. Rings where a stone went in, drawn at three removes; cause and echo.',
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
    zenimon: 'Zenimon — the coin. A round coin with its square hole, tiled; prosperity you can count.',
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
    yaezakura: 'Yaezakura — the double cherry. Two rings of notched petals, the blossom at its fullest.',
    kozakura: 'Kozakura — small cherries. The sakura drawn at komon scale, a drift of little blossoms.',
    nadeshiko: 'Nadeshiko — the dianthus. Five petals frilled at the tip; the flower that names an ideal and outlives it.',
    kikyo: 'Kikyo — the bellflower. A five-pointed star that is a flower; the crest of Akechi, drawn plainly.',
    karahana: 'Karahana — the Tang flower. An imagined blossom of eight petals, older than any garden that grew it.',
    tessen: 'Tessen — clematis. Six petals with a curl at the heart, named for the wire strength of its vine.',
    budoukarakusa: 'Budou karakusa — grape arabesque. A vine curl with a bunch of grapes hanging off it; plenty, trailing.',
    hakarakusa: 'Hakarakusa — leaf arabesque. A waving stem putting out leaves in turn, the vine drawn as a border.',
    ayame: 'Ayame — the iris. One tall standard, two falls; a flower that stands like a flag by the water.',
    omodaka: 'Omodaka — the arrowhead. A spear-point leaf on a bent stem; the water plant that became a crest.',
    kobana: 'Kobana — little flowers. Four petals and a dot, at the scale where a pattern becomes a texture.',
    mokkou: 'Mokkou — the quince section. Four lobes in one outline, a crest shape tiled into a field.',
    noshi: 'Noshi — the gift band. Strips of the noshi wrapper laid diagonally, folds and all; ceremony as a pattern.',
    tabanenoshi: 'Tabane noshi — bundled bands. Ribbons in threes, tied at intervals; many gifts, one bundle.',
    sasa: 'Sasa — bamboo grass. Four pointed leaves from one node, the understory of every bamboo grove.',
    inaho: 'Inaho — the rice ear. Grains in pairs down a stem with its awns up; the harvest, standing.',
    yotsuba: 'Yotsuba — four leaves. Round petals at the cardinals; luck, before the clover claimed it.',
    tanzaku: 'Tanzaku — poem slips. Paper strips hung by a string, waiting for a verse at Tanabata.',
    botan: 'Botan — the peony. Ring inside ring of scalloped petals; the king of flowers, drawn as circles.',
    cho: 'Cho — the butterfly. Wings in pairs and a plain body; drawn symmetric, the way crests draw it.',
    tsuru: 'Tsuru — the crane. One folded silhouette, wing up; a thousand years in a dozen straight lines.',
    usagi: 'Usagi — the rabbit. Ears up, sitting still; the animal in the moon, caught on cloth.',
    tonbo: 'Tonbo — the dragonfly. Four glass wings and a ruled body; the insect that never retreats, a samurai emblem.',
    maruuroko: 'Maru uroko — round scales. The uroko tiling with circles for triangles; a softer armor.',
    temari: 'Temari — the thread ball. Great circles crossing on a sphere, with a diamond at the heart.',
    fuusha: 'Fuusha — the pinwheel. Four blades turning on a square hub; the wind, made visible and toy-sized.',
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
  function chidori(t) {
    var sx = 54, sy = 48, row = 0;
    ctx.fillStyle = t.fg;
    for (var y = sy / 2; y < H + sy; y += sy, row++) {
      for (var x = sx / 2 + (row % 2 ? sx / 2 : 0); x < W + sx; x += sx) {
        var f = (row % 2) ? -1 : 1;
        ctx.save(); ctx.translate(x, y); ctx.scale(f, 1); ctx.globalAlpha = .88;
        ctx.beginPath();
        ctx.moveTo(15, -1);
        ctx.quadraticCurveTo(8, -6, 2, -5);
        ctx.quadraticCurveTo(-6, -12, -14, -9);
        ctx.quadraticCurveTo(-8, -3, -6, 0);
        ctx.quadraticCurveTo(-11, 4, -13, 8);
        ctx.quadraticCurveTo(-5, 7, -1, 5);
        ctx.quadraticCurveTo(6, 8, 10, 3);
        ctx.quadraticCurveTo(14, 1, 15, -1);
        ctx.closePath(); ctx.fill();
        ctx.restore(); ctx.globalAlpha = 1;
      }
    }
  }
  function kiku(t) {
    var sx = 62, sy = 62, row = 0;
    for (var y = sy / 2; y < H + sy; y += sy, row++) {
      for (var x = sx / 2 + (row % 2 ? sx / 2 : 0); x < W + sx; x += sx) {
        ctx.strokeStyle = t.fg; ctx.lineWidth = 1.3;
        for (var k = 0; k < 16; k++) {
          var a = Math.PI / 8 * k;
          ctx.beginPath(); ctx.ellipse(x + 13 * Math.cos(a), y + 13 * Math.sin(a), 4.6, 9.5, a + Math.PI / 2, 0, 7); ctx.stroke();
        }
        ctx.strokeStyle = t.mid;
        for (var k2 = 0; k2 < 8; k2++) {
          var a2 = Math.PI / 4 * k2 + Math.PI / 8;
          ctx.beginPath(); ctx.ellipse(x + 6.5 * Math.cos(a2), y + 6.5 * Math.sin(a2), 2.8, 5.4, a2 + Math.PI / 2, 0, 7); ctx.stroke();
        }
        ctx.beginPath(); ctx.arc(x, y, 2.2, 0, 7); ctx.fillStyle = t.fg; ctx.fill();
      }
    }
  }
  function sakura(t) {
    var sx = 56, sy = 54, row = 0;
    for (var y = sy / 2; y < H + sy; y += sy, row++) {
      for (var x = sx / 2 + (row % 2 ? sx / 2 : 0); x < W + sx; x += sx) {
        for (var k = 0; k < 5; k++) {
          ctx.save(); ctx.translate(x, y); ctx.rotate(Math.PI * 2 / 5 * k - Math.PI / 2);
          ctx.beginPath();
          ctx.moveTo(0, -3);
          ctx.bezierCurveTo(-6.4, -6, -6.8, -12.5, -1.9, -14.6);
          ctx.lineTo(0, -12.4); ctx.lineTo(1.9, -14.6);
          ctx.bezierCurveTo(6.8, -12.5, 6.4, -6, 0, -3);
          ctx.closePath();
          ctx.fillStyle = t.soft; ctx.fill();
          ctx.strokeStyle = t.fg; ctx.lineWidth = 1.2; ctx.stroke();
          ctx.restore();
        }
        ctx.beginPath(); ctx.arc(x, y, 2.6, 0, 7); ctx.strokeStyle = t.fg; ctx.stroke();
        ctx.fillStyle = t.fg;
        for (var k2 = 0; k2 < 5; k2++) { var a = Math.PI * 2 / 5 * k2; ctx.beginPath(); ctx.arc(x + 4.6 * Math.cos(a), y + 4.6 * Math.sin(a), .95, 0, 7); ctx.fill(); }
      }
    }
  }
  function ume(t) {
    var sx = 52, sy = 50, row = 0;
    for (var y = sy / 2; y < H + sy; y += sy, row++) {
      for (var x = sx / 2 + (row % 2 ? sx / 2 : 0); x < W + sx; x += sx) {
        for (var k = 0; k < 5; k++) {
          var a = Math.PI * 2 / 5 * k - Math.PI / 2;
          ctx.beginPath(); ctx.arc(x + 8 * Math.cos(a), y + 8 * Math.sin(a), 6.2, 0, 7);
          ctx.fillStyle = t.soft; ctx.fill(); ctx.strokeStyle = t.fg; ctx.lineWidth = 1.2; ctx.stroke();
        }
        ctx.beginPath(); ctx.arc(x, y, 3, 0, 7); ctx.fillStyle = t.fg; ctx.fill();
      }
    }
  }
  function fuji(t) {
    var sx = 58, sy = 64, row = 0;
    for (var y = 16; y < H + sy; y += sy, row++) {
      for (var x = sx / 2 + (row % 2 ? sx / 2 : 0); x < W + sx; x += sx) {
        ctx.strokeStyle = t.fg; ctx.lineWidth = 1.2;
        ctx.beginPath(); ctx.moveTo(x - 12, y - 12); ctx.quadraticCurveTo(x, y - 6, x, y); ctx.stroke();
        ctx.beginPath(); ctx.ellipse(x - 13, y - 9, 3, 6.5, .7, 0, 7); ctx.stroke();
        ctx.beginPath(); ctx.ellipse(x + 1, y - 13, 3, 6.5, -.4, 0, 7); ctx.stroke();
        var rows = [[3, 0], [4, 7], [3, 13.5], [2, 19], [1, 24]];
        rows.forEach(function (rw, ri) {
          for (var i = 0; i < rw[0]; i++) {
            var gx = x + (i - (rw[0] - 1) / 2) * 6.8, gy = y + rw[1];
            ctx.beginPath(); ctx.arc(gx, gy, 3.1, 0, 7);
            ctx.fillStyle = ri % 2 ? t.mid : t.fg; ctx.fill();
          }
        });
      }
    }
  }
  function matsuba(t) {
    var sx = 50, sy = 46, row = 0;
    ctx.lineWidth = 1.4; ctx.strokeStyle = t.fg; ctx.lineCap = 'round';
    for (var y = sy - 8; y < H + sy; y += sy, row++) {
      for (var x = sx / 2 + (row % 2 ? sx / 2 : 0); x < W + sx; x += sx) {
        [-0.9, -0.45, 0, 0.45, 0.9].forEach(function (da) {
          var a = -Math.PI / 2 + da;
          ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + 21 * Math.cos(a), y + 21 * Math.sin(a)); ctx.stroke();
        });
        ctx.beginPath(); ctx.moveTo(x - 5, y + 1.5); ctx.lineTo(x + 5, y + 1.5); ctx.stroke();
      }
    }
  }
  function take(t) {
    var sx = 46;
    ctx.lineWidth = 1.3;
    for (var x = sx / 2; x < W + sx; x += sx) {
      var off = (Math.round(x / sx) % 2) * 20;
      for (var y = -20 + off; y < H + 30; y += 34) {
        ctx.beginPath();
        ctx.moveTo(x - 5, y); ctx.lineTo(x + 5, y); ctx.lineTo(x + 5, y + 27); ctx.lineTo(x - 5, y + 27); ctx.closePath();
        ctx.fillStyle = t.soft; ctx.fill(); ctx.strokeStyle = t.fg; ctx.stroke();
        ctx.beginPath(); ctx.moveTo(x - 6.5, y + 29.5); ctx.lineTo(x + 6.5, y + 29.5); ctx.stroke();
        ctx.beginPath(); ctx.ellipse(x + 11, y + 24, 3, 7.5, -.8, 0, 7); ctx.strokeStyle = t.mid; ctx.stroke();
        ctx.beginPath(); ctx.ellipse(x - 11, y + 24, 3, 7.5, .8, 0, 7); ctx.stroke();
      }
    }
  }
  function icho(t) {
    var sx = 54, sy = 56, row = 0;
    for (var y = sy / 2 + 8; y < H + sy; y += sy, row++) {
      for (var x = sx / 2 + (row % 2 ? sx / 2 : 0); x < W + sx; x += sx) {
        ctx.beginPath();
        ctx.moveTo(x, y + 16); ctx.lineTo(x, y + 2);
        ctx.strokeStyle = t.fg; ctx.lineWidth = 1.3; ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(x, y + 2);
        ctx.lineTo(x - 15, y - 10);
        ctx.arc(x, y - 10, 15, Math.PI, Math.PI * 1.42);
        ctx.lineTo(x, y - 13.5);
        ctx.lineTo(x, y - 10);
        ctx.arc(x, y - 10, 15, Math.PI * 1.58, 0);
        ctx.lineTo(x, y + 2);
        ctx.closePath();
        ctx.fillStyle = t.soft; ctx.fill(); ctx.stroke();
        [-.5, 0, .5].forEach(function (da) {
          ctx.beginPath(); ctx.moveTo(x, y + 1); ctx.lineTo(x + 13 * Math.sin(da), y - 10 - 12 * Math.cos(da) + 3); ctx.strokeStyle = t.mid; ctx.stroke();
        });
      }
    }
  }
  function momiji(t) {
    var sx = 58, sy = 56, row = 0;
    ctx.fillStyle = t.fg;
    var half = [[-90, 17.5], [-73, 6.5], [-55, 13.5], [-36, 5.5], [-14, 11], [2, 5], [26, 8], [48, 4], [75, 7]];
    for (var y = sy / 2; y < H + sy; y += sy, row++) {
      for (var x = sx / 2 + (row % 2 ? sx / 2 : 0); x < W + sx; x += sx) {
        var pts = [];
        half.forEach(function (p) { var a = p[0] * Math.PI / 180; pts.push([p[1] * Math.cos(a), p[1] * Math.sin(a)]); });
        for (var k = half.length - 2; k >= 1; k--) { var a2 = (180 - half[k][0]) * Math.PI / 180; pts.push([half[k][1] * Math.cos(a2), half[k][1] * Math.sin(a2)]); }
        ctx.save(); ctx.translate(x, y); ctx.globalAlpha = .88;
        ctx.beginPath();
        pts.forEach(function (p, i) { if (i === 0) ctx.moveTo(p[0], p[1]); else ctx.lineTo(p[0], p[1]); });
        ctx.closePath(); ctx.fill();
        ctx.beginPath(); ctx.moveTo(0, 3); ctx.lineTo(0, 15); ctx.strokeStyle = t.fg; ctx.lineWidth = 1.7; ctx.stroke();
        ctx.restore(); ctx.globalAlpha = 1;
      }
    }
  }
  function ogi(t) {
    var sx = 58, sy = 56, row = 0;
    for (var y = sy / 2 + 14; y < H + sy; y += sy, row++) {
      for (var x = sx / 2 + (row % 2 ? sx / 2 : 0); x < W + sx; x += sx) {
        ctx.strokeStyle = t.fg; ctx.lineWidth = 1.3;
        ctx.beginPath(); ctx.arc(x, y, 21, Math.PI * 1.22, Math.PI * 1.78); ctx.stroke();
        ctx.beginPath(); ctx.arc(x, y, 16.5, Math.PI * 1.22, Math.PI * 1.78); ctx.strokeStyle = t.mid; ctx.stroke();
        ctx.strokeStyle = t.fg;
        for (var k = 0; k <= 4; k++) {
          var a = Math.PI * (1.22 + .14 * k);
          ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + 21 * Math.cos(a), y + 21 * Math.sin(a)); ctx.stroke();
        }
        ctx.beginPath(); ctx.arc(x, y, 2.2, 0, 7); ctx.fillStyle = t.fg; ctx.fill();
      }
    }
  }
  function hyotan(t) {
    var sx = 56, sy = 62, row = 0;
    for (var y = sy / 2; y < H + sy; y += sy, row++) {
      for (var x = sx / 2 + (row % 2 ? sx / 2 : 0); x < W + sx; x += sx) {
        ctx.beginPath(); ctx.arc(x, y - 9, 7.5, 0, 7); ctx.fillStyle = t.soft; ctx.fill();
        ctx.beginPath(); ctx.arc(x, y + 7, 11, 0, 7); ctx.fill();
        ctx.beginPath(); ctx.arc(x, y - 9, 7.5, 0, 7); ctx.strokeStyle = t.fg; ctx.lineWidth = 1.3; ctx.stroke();
        ctx.beginPath(); ctx.arc(x, y + 7, 11, 0, 7); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(x - 5.5, y - 1.5); ctx.lineTo(x + 5.5, y - 1.5); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(x, y - 16.5); ctx.lineTo(x, y - 20); ctx.stroke();
      }
    }
  }
  function sekka(t) {
    var sx = 58, sy = 58, row = 0;
    ctx.strokeStyle = t.fg; ctx.lineWidth = 1.3;
    for (var y = sy / 2; y < H + sy; y += sy, row++) {
      for (var x = sx / 2 + (row % 2 ? sx / 2 : 0); x < W + sx; x += sx) {
        for (var k = 0; k < 6; k++) {
          var a = Math.PI / 3 * k;
          ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + 15 * Math.cos(a), y + 15 * Math.sin(a)); ctx.stroke();
          var bx = x + 9.5 * Math.cos(a), by = y + 9.5 * Math.sin(a);
          [a - .5, a + .5].forEach(function (ba) {
            ctx.beginPath(); ctx.moveTo(bx, by); ctx.lineTo(bx + 4.6 * Math.cos(ba), by + 4.6 * Math.sin(ba)); ctx.stroke();
          });
        }
        ctx.beginPath();
        for (var k2 = 0; k2 < 6; k2++) { var a2 = Math.PI / 3 * k2 + Math.PI / 6, px = x + 4.4 * Math.cos(a2), py = y + 4.4 * Math.sin(a2); if (k2 === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py); }
        ctx.closePath(); ctx.strokeStyle = t.mid; ctx.stroke(); ctx.strokeStyle = t.fg;
      }
    }
  }
  function hoshi(t) {
    var sx = 46, sy = 44, row = 0;
    ctx.fillStyle = t.fg;
    for (var y = sy / 2; y < H + sy; y += sy, row++) {
      for (var x = sx / 2 + (row % 2 ? sx / 2 : 0); x < W + sx; x += sx) {
        ctx.beginPath();
        for (var k = 0; k < 10; k++) {
          var a = Math.PI / 5 * k - Math.PI / 2, rr = k % 2 ? 3.6 : 8.6, px = x + rr * Math.cos(a), py = y + rr * Math.sin(a);
          if (k === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
        }
        ctx.closePath(); ctx.globalAlpha = .88; ctx.fill(); ctx.globalAlpha = 1;
        ctx.beginPath(); ctx.arc(x + sx / 2, y + (row % 2 ? 0 : sy / 2), 1.4, 0, 7); ctx.fillStyle = t.mid; ctx.fill(); ctx.fillStyle = t.fg;
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
  function uzu(t) {
    var sx = 62, sy = 60, row = 0;
    ctx.lineWidth = 1.7; ctx.lineCap = 'round'; ctx.strokeStyle = t.fg;
    for (var y = sy / 2; y < H + sy; y += sy, row++) {
      for (var x = sx / 2 + (row % 2 ? sx / 2 : 0); x < W + sx; x += sx) {
        ctx.beginPath();
        for (var a = 0; a <= Math.PI * 4.6; a += .22) {
          var r = .8 + a * 1.62, px = x + r * Math.cos(a + row), py = y + r * Math.sin(a + row);
          if (a === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
        }
        ctx.stroke();
      }
    }
  }
  function tomoe(t) {
    var sx = 62, sy = 62, row = 0;
    ctx.fillStyle = t.fg;
    for (var y = sy / 2; y < H + sy; y += sy, row++) {
      for (var x = sx / 2 + (row % 2 ? sx / 2 : 0); x < W + sx; x += sx) {
        ctx.beginPath(); ctx.arc(x, y, 18.5, 0, 7); ctx.strokeStyle = t.fg; ctx.lineWidth = 1.5; ctx.stroke();
        for (var k = 0; k < 3; k++) {
          var a = Math.PI * 2 / 3 * k - Math.PI / 2;
          ctx.beginPath();
          ctx.arc(x, y, 13, a + .35, a + 1.85);
          ctx.arc(x, y, 9.6, a + 1.85, a + .35, true);
          ctx.closePath(); ctx.fill();
          ctx.beginPath(); ctx.arc(x + 11.3 * Math.cos(a + .35), y + 11.3 * Math.sin(a + .35), 5.2, 0, 7); ctx.fill();
        }
      }
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
  function shibakusa(t) {
    var sx = 44, sy = 42, row = 0;
    ctx.lineWidth = 1.4; ctx.strokeStyle = t.fg; ctx.lineCap = 'round';
    for (var y = sy - 6; y < H + sy; y += sy, row++) {
      for (var x = sx / 2 + (row % 2 ? sx / 2 : 0); x < W + sx; x += sx) {
        [[-11, -15], [0, -19], [11, -15], [-6, -18], [6, -18]].forEach(function (d) {
          ctx.beginPath(); ctx.moveTo(x, y); ctx.quadraticCurveTo(x + d[0] * .4, y + d[1] * .7, x + d[0], y + d[1]); ctx.stroke();
        });
        ctx.beginPath(); ctx.arc(x + 6, y - 19, 1.7, 0, 7); ctx.fillStyle = t.fg; ctx.fill();
      }
    }
  }
  function wakamatsu(t) {
    var sx = 52, sy = 52, row = 0;
    ctx.lineWidth = 1.4; ctx.strokeStyle = t.fg; ctx.lineCap = 'round';
    for (var y = sy - 8; y < H + sy; y += sy, row++) {
      for (var x = sx / 2 + (row % 2 ? sx / 2 : 0); x < W + sx; x += sx) {
        for (var k = -3; k <= 3; k++) {
          var a = -Math.PI / 2 + k * .3;
          ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + 23 * Math.cos(a), y + 23 * Math.sin(a)); ctx.stroke();
        }
        ctx.beginPath(); ctx.moveTo(x - 4.5, y + 2); ctx.lineTo(x + 4.5, y + 2); ctx.stroke();
      }
    }
  }
  function kikusui(t) {
    var bh = 58;
    for (var r = 0; r * bh < H + bh; r++) {
      var y = r * bh + 34, off = (r % 2) * 46;
      ctx.strokeStyle = t.mid; ctx.lineWidth = 1.4;
      [0, 1].forEach(function (k) {
        ctx.beginPath();
        for (var x = 0; x <= W; x += 6) { var yy = y + 12 + k * 7 + Math.sin(x * .05 + r * 2 + k * 2) * 3; if (x === 0) ctx.moveTo(x, yy); else ctx.lineTo(x, yy); }
        ctx.stroke();
      });
      for (var x2 = 30 + off; x2 < W + 40; x2 += 92) {
        ctx.strokeStyle = t.fg; ctx.lineWidth = 1.2;
        for (var k2 = 0; k2 < 9; k2++) {
          var a = Math.PI + Math.PI / 8 * k2;
          ctx.beginPath(); ctx.ellipse(x2 + 11 * Math.cos(a), y + 11 * Math.sin(a) + 12, 3.6, 7.6, a - Math.PI / 2, 0, 7); ctx.stroke();
        }
        ctx.beginPath(); ctx.arc(x2, y + 12, 2, 0, 7); ctx.fillStyle = t.fg; ctx.fill();
      }
    }
  }
  function hamon(t) {
    var sx = 74, sy = 66, row = 0;
    ctx.lineWidth = 1.3;
    for (var y = sy / 2; y < H + sy; y += sy, row++) {
      for (var x = sx / 2 + (row % 2 ? sx / 2 : 0); x < W + sx; x += sx) {
        [16, 11, 6].forEach(function (rr, i) {
          ctx.beginPath(); ctx.arc(x, y, rr, 0, 7); ctx.strokeStyle = i ? t.mid : t.fg; ctx.stroke();
        });
        ctx.beginPath(); ctx.arc(x + sx / 2, y + sy / 2, 4.5, 0, 7); ctx.strokeStyle = t.mid; ctx.stroke();
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
  function zenimon(t) {
    var s = 48, row = 0;
    for (var y = s / 2; y < H + s; y += s, row++) {
      for (var x = s / 2 + (row % 2 ? s / 2 : 0); x < W + s; x += s) {
        ctx.beginPath(); ctx.arc(x, y, 12.5, 0, 7); ctx.strokeStyle = t.fg; ctx.lineWidth = 1.6; ctx.stroke();
        ctx.beginPath(); ctx.arc(x, y, 9.2, 0, 7); ctx.strokeStyle = t.mid; ctx.lineWidth = 1; ctx.stroke();
        ctx.beginPath(); ctx.rect(x - 3.4, y - 3.4, 6.8, 6.8); ctx.fillStyle = t.bg; ctx.fill(); ctx.strokeStyle = t.fg; ctx.stroke();
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
  function yaezakura(t) {
    var sx = 58, sy = 56, row = 0;
    function petal(x, y, rot, len, wdt) {
      ctx.save(); ctx.translate(x, y); ctx.rotate(rot);
      ctx.beginPath();
      ctx.moveTo(0, -len * .2);
      ctx.bezierCurveTo(-wdt, -len * .42, -wdt * 1.06, -len * .86, -wdt * .3, -len * .97);
      ctx.lineTo(0, -len * .82); ctx.lineTo(wdt * .3, -len * .97);
      ctx.bezierCurveTo(wdt * 1.06, -len * .86, wdt, -len * .42, 0, -len * .2);
      ctx.closePath();
      ctx.fillStyle = t.soft; ctx.fill(); ctx.strokeStyle = t.fg; ctx.lineWidth = 1.15; ctx.stroke();
      ctx.restore();
    }
    for (var y = sy / 2; y < H + sy; y += sy, row++) {
      for (var x = sx / 2 + (row % 2 ? sx / 2 : 0); x < W + sx; x += sx) {
        for (var k = 0; k < 5; k++) petal(x, y, Math.PI * 2 / 5 * k - Math.PI / 2, 17, 7);
        for (var k2 = 0; k2 < 5; k2++) petal(x, y, Math.PI * 2 / 5 * k2 - Math.PI / 2 + Math.PI / 5, 10.5, 4.6);
        ctx.beginPath(); ctx.arc(x, y, 2, 0, 7); ctx.fillStyle = t.fg; ctx.fill();
      }
    }
  }
  function kozakura(t) {
    var sx = 36, sy = 36, row = 0;
    for (var y = sy / 2; y < H + sy; y += sy, row++) {
      for (var x = sx / 2 + (row % 2 ? sx / 2 : 0); x < W + sx; x += sx) {
        for (var k = 0; k < 5; k++) {
          ctx.save(); ctx.translate(x, y); ctx.rotate(Math.PI * 2 / 5 * k - Math.PI / 2);
          ctx.beginPath();
          ctx.moveTo(0, -1.6);
          ctx.bezierCurveTo(-3.4, -3.2, -3.6, -6.8, -1, -7.8);
          ctx.lineTo(0, -6.6); ctx.lineTo(1, -7.8);
          ctx.bezierCurveTo(3.6, -6.8, 3.4, -3.2, 0, -1.6);
          ctx.closePath(); ctx.fillStyle = t.soft; ctx.fill(); ctx.strokeStyle = t.fg; ctx.lineWidth = 1; ctx.stroke();
          ctx.restore();
        }
        ctx.beginPath(); ctx.arc(x, y, 1.3, 0, 7); ctx.fillStyle = t.fg; ctx.fill();
      }
    }
  }
  function nadeshiko(t) {
    var sx = 56, sy = 54, row = 0;
    for (var y = sy / 2; y < H + sy; y += sy, row++) {
      for (var x = sx / 2 + (row % 2 ? sx / 2 : 0); x < W + sx; x += sx) {
        for (var k = 0; k < 5; k++) {
          ctx.save(); ctx.translate(x, y); ctx.rotate(Math.PI * 2 / 5 * k - Math.PI / 2);
          ctx.beginPath();
          ctx.moveTo(0, -3);
          ctx.bezierCurveTo(-5.6, -5.6, -5.4, -10, -2.7, -12.6);
          ctx.lineTo(-1.35, -14.4); ctx.lineTo(0, -13); ctx.lineTo(1.35, -14.4); ctx.lineTo(2.7, -12.6);
          ctx.bezierCurveTo(5.4, -10, 5.6, -5.6, 0, -3);
          ctx.closePath(); ctx.fillStyle = t.soft; ctx.fill(); ctx.strokeStyle = t.fg; ctx.lineWidth = 1.15; ctx.stroke();
          ctx.restore();
        }
        ctx.beginPath(); ctx.arc(x, y, 2.2, 0, 7); ctx.fillStyle = t.fg; ctx.fill();
      }
    }
  }
  function kikyo(t) {
    var sx = 54, sy = 52, row = 0;
    for (var y = sy / 2; y < H + sy; y += sy, row++) {
      for (var x = sx / 2 + (row % 2 ? sx / 2 : 0); x < W + sx; x += sx) {
        ctx.strokeStyle = t.fg; ctx.lineWidth = 1.2;
        for (var k = 0; k < 5; k++) {
          var a = Math.PI * 2 / 5 * k - Math.PI / 2;
          ctx.beginPath(); ctx.ellipse(x + 7.2 * Math.cos(a), y + 7.2 * Math.sin(a), 4.3, 8.6, a + Math.PI / 2, 0, 7);
          ctx.fillStyle = t.soft; ctx.fill(); ctx.stroke();
        }
        ctx.beginPath(); ctx.arc(x, y, 2.5, 0, 7); ctx.fillStyle = t.fg; ctx.fill();
        ctx.beginPath(); ctx.arc(x, y, 4.6, 0, 7); ctx.strokeStyle = t.mid; ctx.lineWidth = 1; ctx.stroke();
      }
    }
  }
  function karahana(t) {
    var sx = 56, sy = 56, row = 0;
    for (var y = sy / 2; y < H + sy; y += sy, row++) {
      for (var x = sx / 2 + (row % 2 ? sx / 2 : 0); x < W + sx; x += sx) {
        ctx.strokeStyle = t.fg; ctx.lineWidth = 1.2;
        for (var k = 0; k < 8; k++) {
          var a = Math.PI / 4 * k;
          ctx.beginPath(); ctx.ellipse(x + 8.8 * Math.cos(a), y + 8.8 * Math.sin(a), 3.8, 8.2, a + Math.PI / 2, 0, 7); ctx.stroke();
        }
        ctx.beginPath(); ctx.arc(x, y, 3.2, 0, 7); ctx.strokeStyle = t.mid; ctx.stroke();
        ctx.fillStyle = t.mid;
        for (var k2 = 0; k2 < 8; k2++) { var a2 = Math.PI / 4 * k2 + Math.PI / 8; ctx.beginPath(); ctx.arc(x + 16.5 * Math.cos(a2), y + 16.5 * Math.sin(a2), 1.1, 0, 7); ctx.fill(); }
      }
    }
  }
  function tessen(t) {
    var sx = 56, sy = 56, row = 0;
    ctx.strokeStyle = t.fg; ctx.lineWidth = 1.25;
    for (var y = sy / 2; y < H + sy; y += sy, row++) {
      for (var x = sx / 2 + (row % 2 ? sx / 2 : 0); x < W + sx; x += sx) {
        for (var k = 0; k < 6; k++) {
          var a = Math.PI / 3 * k;
          ctx.beginPath(); ctx.ellipse(x + 8 * Math.cos(a), y + 8 * Math.sin(a), 3.6, 8.6, a + Math.PI / 2 + .45, 0, 7); ctx.stroke();
        }
        ctx.beginPath();
        for (var a2 = 0; a2 <= Math.PI * 3.4; a2 += .3) { var r = .6 + a2 * 1.05, px = x + r * Math.cos(a2), py = y + r * Math.sin(a2); if (a2 === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py); }
        ctx.strokeStyle = t.mid; ctx.stroke();
        ctx.strokeStyle = t.fg;
      }
    }
  }
  function budoukarakusa(t) {
    var s = 58, row = 0;
    ctx.lineCap = 'round';
    for (var y = s / 2; y < H + s; y += s, row++) {
      for (var x = s / 2; x < W + s; x += s) {
        var cx = x + (row % 2 ? s / 2 : 0), cy = y;
        ctx.strokeStyle = t.fg; ctx.lineWidth = 1.5;
        ctx.beginPath();
        for (var a = 0; a <= Math.PI * 4.2; a += .3) { var r = 1 + a * 1.05, px = cx - 12 + r * Math.cos(a), py = cy - 8 + r * Math.sin(a); if (a === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py); }
        ctx.stroke();
        ctx.beginPath(); ctx.moveTo(cx + 2, cy - 14); ctx.quadraticCurveTo(cx + 8, cy - 6, cx + 8, cy - 1); ctx.stroke();
        [[8, 2], [2.5, 4.5], [13.5, 4.5], [5, 10.5], [11, 10.5], [8, 16]].forEach(function (g, gi) {
          ctx.beginPath(); ctx.arc(cx + g[0], cy + g[1], 3.3, 0, 7);
          ctx.fillStyle = gi % 2 ? t.mid : t.fg; ctx.fill();
        });
      }
    }
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
  function ayame(t) {
    var sx = 56, sy = 60, row = 0;
    for (var y = sy / 2 + 4; y < H + sy; y += sy, row++) {
      for (var x = sx / 2 + (row % 2 ? sx / 2 : 0); x < W + sx; x += sx) {
        ctx.strokeStyle = t.fg; ctx.lineWidth = 1.25;
        ctx.beginPath(); ctx.moveTo(x, y + 17); ctx.lineTo(x, y + 7); ctx.stroke();
        [[-1, 58], [1, -58]].forEach(function (sd) {
          ctx.beginPath(); ctx.ellipse(x + sd[0] * 9.5, y + 7.5, 3.6, 9.2, sd[1] * Math.PI / 180, 0, 7); ctx.fillStyle = t.soft; ctx.fill(); ctx.stroke();
        });
        [[-1, -30], [1, 30]].forEach(function (sd) {
          ctx.beginPath(); ctx.ellipse(x + sd[0] * 5.5, y - 8.5, 2.4, 7.2, sd[1] * Math.PI / 180, 0, 7); ctx.fillStyle = t.soft; ctx.fill(); ctx.stroke();
        });
        ctx.beginPath();
        ctx.moveTo(x, y + 9); ctx.quadraticCurveTo(x - 6, y - 7, x, y - 19); ctx.quadraticCurveTo(x + 6, y - 7, x, y + 9);
        ctx.closePath(); ctx.fillStyle = t.soft; ctx.fill(); ctx.stroke();
      }
    }
  }
  function omodaka(t) {
    var sx = 54, sy = 58, row = 0;
    for (var y = sy / 2 + 2; y < H + sy; y += sy, row++) {
      for (var x = sx / 2 + (row % 2 ? sx / 2 : 0); x < W + sx; x += sx) {
        ctx.beginPath();
        ctx.moveTo(x, y - 15); ctx.lineTo(x + 8.5, y + 5); ctx.lineTo(x, y + 1); ctx.lineTo(x - 8.5, y + 5); ctx.closePath();
        ctx.fillStyle = t.soft; ctx.fill(); ctx.strokeStyle = t.fg; ctx.lineWidth = 1.25; ctx.stroke();
        ctx.beginPath(); ctx.moveTo(x, y + 1); ctx.quadraticCurveTo(x + 2, y + 10, x, y + 16); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(x, y - 12); ctx.lineTo(x, y + 0); ctx.strokeStyle = t.mid; ctx.stroke();
        ctx.beginPath(); ctx.arc(x + 7, y + 13, 2.3, 0, 7); ctx.fillStyle = t.fg; ctx.fill();
      }
    }
  }
  function kobana(t) {
    var s = 31, row = 0;
    for (var y = s / 2; y < H + s; y += s, row++) {
      for (var x = s / 2 + (row % 2 ? s / 2 : 0); x < W + s; x += s) {
        for (var k = 0; k < 4; k++) {
          var a = Math.PI / 2 * k + Math.PI / 4;
          ctx.beginPath(); ctx.arc(x + 3.1 * Math.cos(a), y + 3.1 * Math.sin(a), 2.9, 0, 7);
          ctx.fillStyle = t.soft; ctx.fill(); ctx.strokeStyle = t.fg; ctx.lineWidth = .95; ctx.stroke();
        }
        ctx.beginPath(); ctx.arc(x, y, 1.25, 0, 7); ctx.fillStyle = t.fg; ctx.fill();
        ctx.beginPath(); ctx.arc(x + s / 2, y + s / 2, .95, 0, 7); ctx.fillStyle = t.mid; ctx.fill();
      }
    }
  }
  function mokkou(t) {
    var sx = 58, sy = 58, row = 0;
    for (var y = sy / 2; y < H + sy; y += sy, row++) {
      for (var x = sx / 2 + (row % 2 ? sx / 2 : 0); x < W + sx; x += sx) {
        ctx.save(); ctx.translate(x, y);
        ctx.beginPath();
        for (var k = 0; k < 4; k++) {
          ctx.arc(-7, -7, 8.5, -0.6, 2.17, true);
          ctx.rotate(Math.PI / 2);
        }
        ctx.closePath();
        ctx.fillStyle = t.soft; ctx.fill(); ctx.strokeStyle = t.fg; ctx.lineWidth = 1.3; ctx.stroke();
        ctx.restore();
        ctx.beginPath(); ctx.arc(x, y, 2, 0, 7); ctx.fillStyle = t.fg; ctx.fill();
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
  function sasa(t) {
    var sx = 56, sy = 58, row = 0;
    for (var y = sy / 2 + 12; y < H + sy; y += sy, row++) {
      for (var x = sx / 2 + (row % 2 ? sx / 2 : 0); x < W + sx; x += sx) {
        ctx.strokeStyle = t.fg; ctx.lineWidth = 1.3;
        ctx.beginPath(); ctx.moveTo(x, y + 14); ctx.lineTo(x, y); ctx.stroke();
        [[-.72, 19], [-.26, 22], [.26, 22], [.72, 19]].forEach(function (L) {
          var a = -Math.PI / 2 + L[0], len = L[1];
          var tipx = x + len * Math.cos(a), tipy = y + len * Math.sin(a);
          var mx = x + len * .5 * Math.cos(a), my = y + len * .5 * Math.sin(a);
          var px = Math.cos(a + Math.PI / 2) * 3.4, py = Math.sin(a + Math.PI / 2) * 3.4;
          ctx.beginPath();
          ctx.moveTo(x, y);
          ctx.quadraticCurveTo(mx + px, my + py, tipx, tipy);
          ctx.quadraticCurveTo(mx - px, my - py, x, y);
          ctx.closePath(); ctx.fillStyle = t.soft; ctx.fill(); ctx.stroke();
        });
      }
    }
  }
  function inaho(t) {
    var sx = 46, sy = 64, row = 0;
    ctx.lineWidth = 1.3;
    for (var y = 34; y < H + sy; y += sy, row++) {
      for (var x = sx / 2 + (row % 2 ? sx / 2 : 0); x < W + sx; x += sx) {
        ctx.strokeStyle = t.fg;
        ctx.beginPath(); ctx.moveTo(x, y + 22); ctx.lineTo(x, y - 24); ctx.stroke();
        for (var k = 0; k < 6; k++) {
          var gy = y - 20 + k * 6.4;
          [-1, 1].forEach(function (sd) {
            ctx.beginPath(); ctx.ellipse(x + sd * 3.6, gy, 2.3, 5.2, sd * .62, 0, 7);
            ctx.fillStyle = t.fg; ctx.globalAlpha = .82; ctx.fill(); ctx.globalAlpha = 1;
          });
        }
        ctx.lineWidth = .9;
        [-.3, 0, .3].forEach(function (da) {
          ctx.beginPath(); ctx.moveTo(x, y - 24); ctx.lineTo(x + da * 22, y - 34); ctx.stroke();
        });
        ctx.lineWidth = 1.3;
      }
    }
  }
  function yotsuba(t) {
    var sx = 52, sy = 52, row = 0;
    for (var y = sy / 2; y < H + sy; y += sy, row++) {
      for (var x = sx / 2 + (row % 2 ? sx / 2 : 0); x < W + sx; x += sx) {
        for (var k = 0; k < 4; k++) {
          var a = Math.PI / 2 * k - Math.PI / 2;
          ctx.beginPath(); ctx.arc(x + 6.2 * Math.cos(a), y + 6.2 * Math.sin(a), 6.9, 0, 7);
          ctx.fillStyle = t.soft; ctx.fill(); ctx.strokeStyle = t.fg; ctx.lineWidth = 1.2; ctx.stroke();
        }
        ctx.beginPath(); ctx.arc(x, y, 1.8, 0, 7); ctx.fillStyle = t.fg; ctx.fill();
      }
    }
  }
  function tanzaku(t) {
    var sx = 44;
    for (var x = sx / 2; x < W + sx; x += sx) {
      var col = Math.round(x / sx), off = (col * 37) % 23;
      for (var y = -30 + off; y < H + 40; y += 74) {
        ctx.beginPath(); ctx.roundRect(x - 8, y, 16, 47, 2);
        ctx.fillStyle = t.soft; ctx.fill(); ctx.strokeStyle = t.fg; ctx.lineWidth = 1.2; ctx.stroke();
        ctx.beginPath(); ctx.arc(x, y + 6, 1.7, 0, 7); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(x, y - 8); ctx.lineTo(x, y + 4.3); ctx.strokeStyle = t.mid; ctx.stroke();
        ctx.beginPath(); ctx.moveTo(x - 4.5, y + 14); ctx.lineTo(x + 4.5, y + 14); ctx.stroke();
      }
    }
  }
  function botan(t) {
    var sx = 60, sy = 60, row = 0;
    function ring(x, y, r, n, bump, col) {
      ctx.strokeStyle = col; ctx.lineWidth = 1.2;
      for (var k = 0; k < n; k++) {
        var a = Math.PI * 2 / n * k;
        ctx.beginPath(); ctx.arc(x + r * Math.cos(a), y + r * Math.sin(a), bump, 0, 7); ctx.stroke();
      }
    }
    for (var y = sy / 2; y < H + sy; y += sy, row++) {
      for (var x = sx / 2 + (row % 2 ? sx / 2 : 0); x < W + sx; x += sx) {
        ring(x, y, 11.5, 9, 5.4, t.fg);
        ring(x, y, 7.2, 7, 4.3, t.mid);
        ring(x, y, 3.6, 5, 2.9, t.fg);
        ctx.beginPath(); ctx.arc(x, y, 1.4, 0, 7); ctx.fillStyle = t.fg; ctx.fill();
      }
    }
  }
  function cho(t) {
    var sx = 58, sy = 54, row = 0;
    for (var y = sy / 2; y < H + sy; y += sy, row++) {
      for (var x = sx / 2 + (row % 2 ? sx / 2 : 0); x < W + sx; x += sx) {
        ctx.strokeStyle = t.fg; ctx.lineWidth = 1.2;
        [[-1, -.5], [1, .5]].forEach(function (sd) {
          ctx.beginPath(); ctx.ellipse(x + sd[0] * 8, y - 5, 6.4, 10.4, sd[1], 0, 7); ctx.fillStyle = t.soft; ctx.fill(); ctx.stroke();
          ctx.beginPath(); ctx.ellipse(x + sd[0] * 7, y + 6.5, 5.4, 7.8, -sd[1] * .8, 0, 7); ctx.fill(); ctx.stroke();
        });
        ctx.beginPath(); ctx.ellipse(x, y, 2.1, 9.5, 0, 0, 7); ctx.fillStyle = t.fg; ctx.fill();
        [-1, 1].forEach(function (sd) {
          ctx.beginPath(); ctx.moveTo(x + sd * 1.2, y - 8.5); ctx.quadraticCurveTo(x + sd * 5, y - 14, x + sd * 7.5, y - 15.5); ctx.stroke();
        });
      }
    }
  }
  function tsuru(t) {
    var sx = 62, sy = 54, row = 0;
    ctx.fillStyle = t.fg;
    var pts = [[-17, 6], [-7, -1], [-1, -15], [3, -3], [16, -10], [10, 0], [13.5, 7], [3, 4.5], [-2, 9.5], [-7, 3]];
    for (var y = sy / 2; y < H + sy; y += sy, row++) {
      for (var x = sx / 2 + (row % 2 ? sx / 2 : 0); x < W + sx; x += sx) {
        ctx.save(); ctx.translate(x, y); ctx.scale(row % 2 ? -1 : 1, 1); ctx.globalAlpha = .9;
        ctx.beginPath();
        pts.forEach(function (p, i) { if (i === 0) ctx.moveTo(p[0], p[1]); else ctx.lineTo(p[0], p[1]); });
        ctx.closePath(); ctx.fill();
        ctx.restore(); ctx.globalAlpha = 1;
      }
    }
  }
  function usagi(t) {
    var sx = 62, sy = 56, row = 0;
    ctx.fillStyle = t.fg;
    for (var y = sy / 2; y < H + sy; y += sy, row++) {
      for (var x = sx / 2 + (row % 2 ? sx / 2 : 0); x < W + sx; x += sx) {
        ctx.save(); ctx.translate(x, y); ctx.scale(row % 2 ? -1 : 1, 1); ctx.globalAlpha = .88;
        ctx.beginPath(); ctx.ellipse(-1, 5, 10.5, 7.6, 0, 0, 7); ctx.fill();
        ctx.beginPath(); ctx.arc(9.5, -2.5, 5.6, 0, 7); ctx.fill();
        ctx.beginPath(); ctx.ellipse(7.2, -12, 2.1, 8.6, .22, 0, 7); ctx.fill();
        ctx.beginPath(); ctx.ellipse(11.8, -11.4, 2.1, 8.2, .48, 0, 7); ctx.fill();
        ctx.beginPath(); ctx.arc(-11, 2.5, 2.7, 0, 7); ctx.fillStyle = t.bg; ctx.fill();
        ctx.beginPath(); ctx.arc(11.2, -3.6, 1.05, 0, 7); ctx.fill();
        ctx.restore(); ctx.globalAlpha = 1; ctx.fillStyle = t.fg;
      }
    }
  }
  function tonbo(t) {
    var sx = 58, sy = 58, row = 0;
    for (var y = sy / 2; y < H + sy; y += sy, row++) {
      for (var x = sx / 2 + (row % 2 ? sx / 2 : 0); x < W + sx; x += sx) {
        ctx.strokeStyle = t.fg; ctx.lineWidth = 1.15;
        [[-1, -.16, -8], [1, .16, -8], [-1, .3, 0], [1, -.3, 0]].forEach(function (w) {
          ctx.beginPath(); ctx.ellipse(x + w[0] * 11.5, y + w[2], 12.5, 3.4, w[1], 0, 7);
          ctx.fillStyle = t.soft; ctx.fill(); ctx.stroke();
        });
        ctx.beginPath(); ctx.ellipse(x, y + 1, 2.4, 13.5, 0, 0, 7); ctx.fillStyle = t.fg; ctx.fill();
        ctx.beginPath(); ctx.arc(x, y - 14.5, 3.3, 0, 7); ctx.fill();
        ctx.strokeStyle = t.bg;
        [-2, 3.5, 9].forEach(function (yy) { ctx.beginPath(); ctx.moveTo(x - 2.2, y + yy); ctx.lineTo(x + 2.2, y + yy); ctx.stroke(); });
      }
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
  function temari(t) {
    var sx = 56, sy = 56, row = 0;
    for (var y = sy / 2; y < H + sy; y += sy, row++) {
      for (var x = sx / 2 + (row % 2 ? sx / 2 : 0); x < W + sx; x += sx) {
        ctx.beginPath(); ctx.arc(x, y, 14.5, 0, 7); ctx.strokeStyle = t.fg; ctx.lineWidth = 1.4; ctx.stroke();
        ctx.beginPath(); ctx.ellipse(x, y, 6, 14.5, 0, 0, 7); ctx.strokeStyle = t.mid; ctx.lineWidth = 1.1; ctx.stroke();
        ctx.beginPath(); ctx.ellipse(x, y, 14.5, 6, 0, 0, 7); ctx.stroke();
        ctx.beginPath(); ctx.ellipse(x, y, 11, 11, Math.PI / 4, 0, 7); ctx.stroke();
        ctx.save(); ctx.translate(x, y); ctx.rotate(Math.PI / 4); ctx.fillStyle = t.fg; ctx.fillRect(-2.4, -2.4, 4.8, 4.8); ctx.restore();
      }
    }
  }
  function fuusha(t) {
    var sx = 52, sy = 52, row = 0;
    for (var y = sy / 2; y < H + sy; y += sy, row++) {
      for (var x = sx / 2 + (row % 2 ? sx / 2 : 0); x < W + sx; x += sx) {
        for (var k = 0; k < 4; k++) {
          ctx.save(); ctx.translate(x, y); ctx.rotate(Math.PI / 2 * k + (row % 2 ? Math.PI / 4 : 0));
          ctx.beginPath();
          ctx.moveTo(2.6, -2.6); ctx.lineTo(15.5, -2.6); ctx.lineTo(2.6, -11.5); ctx.closePath();
          ctx.fillStyle = k % 2 ? t.mid : t.fg; ctx.globalAlpha = .9; ctx.fill();
          ctx.restore();
        }
        ctx.save(); ctx.translate(x, y); ctx.rotate(Math.PI / 4); ctx.fillStyle = t.fg; ctx.fillRect(-2.5, -2.5, 5, 5); ctx.restore();
        ctx.globalAlpha = 1;
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
    ({ seigaiha: seigaiha, asanoha: asanoha, shippo: shippo, ichimatsu: ichimatsu, kikko: kikko, uroko: uroko, same: same, yagasuri: yagasuri, kanoko: kanoko, hishi: hishi, sayagata: sayagata, kagome: kagome, karakusa: karakusa, ryusui: ryusui, tatewaku: tatewaku, yukwa: yukwa, ajiro: ajiro, sankuzushi: sankuzushi, higaki: higaki, hanabishi: hanabishi, watsunagi: watsunagi, bishamon: bishamon, tatenami: tatenami, chidori: chidori, kiku: kiku, sakura: sakura, ume: ume, fuji: fuji, matsuba: matsuba, take: take, icho: icho, momiji: momiji, ogi: ogi, hyotan: hyotan, sekka: sekka, hoshi: hoshi, kanzemizu: kanzemizu, uzu: uzu, tomoe: tomoe, genjigumo: genjigumo, kasumi: kasumi, kumo: kumo, ame: ame, shibakusa: shibakusa, wakamatsu: wakamatsu, kikusui: kikusui, hamon: hamon, yanagi: yanagi, raimon: raimon, kojitsunagi: kojitsunagi, manjitsunagi: manjitsunagi, igeta: igeta, mansuji: mansuji, komochijima: komochijima, yamaji: yamaji, arare: arare, hyoretsu: hyoretsu, jujigasuri: jujigasuri, igasuri: igasuri, fundotsunagi: fundotsunagi, kusari: kusari, zenimon: zenimon, matsukawabishi: matsukawabishi, takedabishi: takedabishi, mitsubishi: mitsubishi, kenhanabishi: kenhanabishi, nijukikko: nijukikko, kikkohanabishi: kikkohanabishi, hanashippo: hanashippo, amime: amime, kakutoshi: kakutoshi, ishigaki: ishigaki, takegaki: takegaki, senbongoshi: senbongoshi, yaezakura: yaezakura, kozakura: kozakura, nadeshiko: nadeshiko, kikyo: kikyo, karahana: karahana, tessen: tessen, budoukarakusa: budoukarakusa, hakarakusa: hakarakusa, ayame: ayame, omodaka: omodaka, kobana: kobana, mokkou: mokkou, noshi: noshi, tabanenoshi: tabanenoshi, sasa: sasa, inaho: inaho, yotsuba: yotsuba, tanzaku: tanzaku, botan: botan, cho: cho, tsuru: tsuru, usagi: usagi, tonbo: tonbo, maruuroko: maruuroko, temari: temari, fuusha: fuusha })[pattern](t);
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
