(() => {
  'use strict';
  let serial = 0;
  function identify(element, prefix) {
    if (!element.id) {
      let candidate;
      do { candidate = prefix + '-' + (++serial); } while (document.getElementById(candidate));
      element.id = candidate;
    }
    return element.id;
  }
  const INTERVAL = 3000;
  const reduced = () => matchMedia('(prefers-reduced-motion: reduce)').matches;

  document.querySelectorAll('[data-rank]').forEach(list => {
    if (list.dataset.kataReady) return;
    const panel = list.closest('.k-glass') || list.parentElement;
    const button = panel.querySelector('[data-rank-btn]');
    list.dataset.kataReady = 'true';
    identify(list, 'kata-rank');
    if (button) { button.type = 'button'; button.setAttribute('aria-controls', list.id); }
    const status = document.createElement('span');
    status.className = 'k-rank-status'; status.setAttribute('role', 'status');
    identify(status, 'kata-rank-status'); list.after(status);

    function sort(announce) {
      const items = [...list.children];
      const first = new Map(items.map(item => [item, item.getBoundingClientRect().top]));
      items.forEach(item => { item.dataset.score = Math.max(40, Math.min(99, +item.dataset.score + Math.round((Math.random() - 0.5) * 36))); });
      items.sort((a, b) => +b.dataset.score - +a.dataset.score).forEach(item => list.append(item));
      const scale = parseFloat(getComputedStyle(list).getPropertyValue('--k-mscale'));
      const duration = 560 * (Number.isFinite(scale) ? scale : 1);
      const ease = getComputedStyle(list).getPropertyValue('--k-ease-in-out').trim() || 'ease';
      [...list.children].forEach((item, index) => {
        item.querySelector('.no').textContent = index + 1;
        item.querySelector('.val').textContent = item.dataset.score;
        const dy = first.get(item) - item.getBoundingClientRect().top;
        // FLIP: rows travel from their old position; zero duration or reduced motion just lands them.
        if (dy && duration > 0 && !reduced()) item.animate([{ transform: `translateY(${dy}px)` }, { transform: 'none' }], { duration, easing: ease });
      });
      const top = list.firstElementChild;
      const name = top ? [...top.childNodes].filter(node => node.nodeType === 3).map(node => node.textContent).join('').trim() : '';
      if (announce) status.textContent = 'Re-ranked. First: ' + name + '.';
      list.dispatchEvent(new CustomEvent('kata-reorder-change', { bubbles: true, detail: { order: [...list.children].map(item => [...item.childNodes].filter(node => node.nodeType === 3).map(node => node.textContent).join('').trim()), source: announce ? 'button' : 'auto' } }));
    }
    if (button) button.addEventListener('click', () => sort(true));
    const pause = panel.querySelector('[data-rank-pause]');

    // Autoplay pauses while a pointer or keyboard focus is inside, and never starts with reduced motion.
    let timer = 0, hovered = false, focused = false;
    const stop = () => { clearInterval(timer); timer = 0; };
    const resume = () => { stop(); if (!hovered && !focused && !reduced() && list.dataset.rankAutoplay !== 'off') timer = setInterval(() => sort(false), INTERVAL); };
    panel.addEventListener('pointerenter', () => { hovered = true; stop(); });
    panel.addEventListener('pointerleave', () => { hovered = false; resume(); });
    panel.addEventListener('focusin', () => { focused = true; stop(); });
    panel.addEventListener('focusout', event => { if (event.relatedTarget && panel.contains(event.relatedTarget)) return; focused = false; resume(); });
    if (pause) {
      pause.type = 'button'; pause.setAttribute('aria-controls', list.id);
      pause.setAttribute('aria-pressed', list.dataset.rankAutoplay === 'off' ? 'true' : 'false');
      pause.addEventListener('click', () => {
        const off = list.dataset.rankAutoplay !== 'off';
        list.dataset.rankAutoplay = off ? 'off' : 'on';
        pause.setAttribute('aria-pressed', off ? 'true' : 'false');
        resume();
      });
    }
    resume();
  });
})();
