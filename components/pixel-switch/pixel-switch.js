// KATA Pixel Switch — the knob's dot icon scatters and re-forms on every change.
(() => {
  'use strict';
  // 11 x 11 dot maps, '#' lit: [unchecked, checked]. Edit a pair or add one, then name it in data-pxs.
  const MAPS = {
    theme: [
      ['.....#.....', '.#.......#.', '...........', '....###....', '...#####...', '#..#####..#', '...#####...', '....###....', '...........', '.#.......#.', '.....#.....'],
      ['...........', '....###..#.', '...###.....', '..###....#.', '..###......', '..###......', '..####.....', '...#####.#.', '....#####..', '.....###...', '...........']],
    sound: [
      ['...........', '....#......', '...##......', '..###.#...#', '#####..#.#.', '#####...#..', '#####..#.#.', '..###.#...#', '...##......', '....#......', '...........'],
      ['...........', '....#......', '...##...#..', '..###.#..#.', '#####..#.#.', '#####..#.#.', '#####..#.#.', '..###.#..#.', '...##...#..', '....#......', '...........']],
    bell: [
      ['...........', '.#...#.....', '..#.###....', '...#.###...', '...##.##...', '...###.#...', '..#####.#..', '.#######.#.', '........#..', '....###..#.', '...........'],
      ['...........', '.....#.....', '....###....', '...#####...', '...#####...', '...#####...', '..#######..', '.#########.', '...........', '....###....', '...........']],
    power: [
      ['.....#.....', '.....#.....', '...#.#.#...', '..#..#..#..', '.##..#..##.', '.#...#...#.', '.#.......#.', '.##.....##.', '..#.....#..', '...#####...', '...........'],
      ['......#....', '.....##....', '....##.....', '...##......', '..#######..', '.....##....', '....##.....', '...##......', '..##.......', '..#........', '...........']]
  };
  const SIZE = 11, MID = 5, PERIOD = 720, STAGGER = 20;
  const cells = rows => {
    const out = [];
    rows.forEach((row, y) => { for (let x = 0; x < SIZE; x++) if (row[x] === '#') out.push([x, y]); });
    return out;
  };
  const SHAPES = {};
  Object.keys(MAPS).forEach(name => { SHAPES[name] = MAPS[name].map(cells); });
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  // Translate percentages are the dot's own size, so one unit is one cell at any part size.
  const at = p => 'translate(' + (p.x * 100) + '%, ' + (p.y * 100) + '%)';

  document.querySelectorAll('[data-pxs]').forEach(root => {
    if (root.dataset.kataReady) return;
    const input = root.querySelector('input[type="checkbox"]');
    const knob = root.querySelector('.k-pxs-knob');
    if (!input || !knob) return;
    root.dataset.kataReady = 'true';
    const pair = SHAPES[root.dataset.pxs] || SHAPES.theme;
    let box = knob.querySelector('.k-pxs-dots');
    if (!box) {
      box = document.createElement('span');
      box.className = 'k-pxs-dots';
      knob.append(box);
    }
    box.setAttribute('aria-hidden', 'true');
    box.textContent = '';
    // One dot per lit cell of the larger icon; spare dots fade out at the centre.
    const dots = Array.from({ length: Math.max(pair[0].length, pair[1].length) }, () => box.appendChild(document.createElement('span')));
    const runs = [];
    const ends = () => {
      const shape = pair[input.checked ? 1 : 0];
      return dots.map((_, i) => shape[i] ? { x: shape[i][0], y: shape[i][1], a: 1 } : { x: MID, y: MID, a: 0 });
    };
    const place = (dot, p) => { dot.style.transform = at(p); dot.style.opacity = String(p.a); };
    const still = () => {
      const scale = parseFloat(getComputedStyle(root).getPropertyValue('--k-mscale'));
      return reduce.matches || scale === 0 || typeof dots[0].animate !== 'function';
    };
    const sync = () => {
      const targets = ends();
      const scale = parseFloat(getComputedStyle(root).getPropertyValue('--k-mscale'));
      const factor = Number.isFinite(scale) ? scale : 1;
      const easing = getComputedStyle(root).getPropertyValue('--k-ease-in-out').trim() || 'ease-in-out';
      const instant = still();
      dots.forEach((dot, i) => {
        // An interrupted morph starts again from where its dot is now.
        if (runs[i]) { try { runs[i].commitStyles(); } catch (e) { /* not rendered */ } runs[i].cancel(); runs[i] = null; }
        const cs = getComputedStyle(dot);
        const from = { transform: cs.transform === 'none' ? at({ x: 0, y: 0 }) : cs.transform, opacity: cs.opacity };
        place(dot, targets[i]);
        if (instant) return;
        const turn = Math.random() * Math.PI * 2, reach = 3 + Math.random() * 3;
        const out = { x: MID + Math.cos(turn) * reach, y: MID + Math.sin(turn) * reach };
        runs[i] = dot.animate([
          { offset: 0, transform: from.transform, opacity: from.opacity, easing },
          { offset: 0.45, transform: at(out), opacity: String(parseFloat(from.opacity) * 0.6), easing },
          { offset: 1, transform: at(targets[i]), opacity: String(targets[i].a) }
        ], { duration: PERIOD * factor, delay: (i % 7) * STAGGER * factor, fill: 'backwards' });
        runs[i].onfinish = () => { runs[i] = null; };
      });
    };
    ends().forEach((p, i) => place(dots[i], p));
    input.addEventListener('change', sync);
    if (input.form) input.form.addEventListener('reset', () => setTimeout(sync));
  });
})();
