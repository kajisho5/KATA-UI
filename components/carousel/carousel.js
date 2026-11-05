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

  document.querySelectorAll('[data-car-track]').forEach(track => {
    if (track.dataset.kataReady) return;
    const root = track.closest('.k-car') || track.parentElement;
    const slides = [...track.children];
    if (!root || !slides.length) return;
    track.dataset.kataReady = 'true';
    identify(root, 'kata-carousel'); identify(track, 'kata-carousel-track');
    const prev = root.querySelector('[data-car-prev]');
    const next = root.querySelector('[data-car-next]');
    const dots = [...root.querySelectorAll('[data-car-dot]')];
    // A group, not a region landmark: pasted copies would repeat the same landmark name.
    if (!root.hasAttribute('role')) root.setAttribute('role', 'group');
    if (!root.hasAttribute('aria-roledescription')) root.setAttribute('aria-roledescription', 'carousel');
    if (!root.hasAttribute('aria-label') && !root.hasAttribute('aria-labelledby')) root.setAttribute('aria-label', 'Carousel');
    slides.forEach((slide, i) => {
      identify(slide, 'kata-carousel-slide');
      slide.setAttribute('role', 'group'); slide.setAttribute('aria-roledescription', 'slide');
      if (!slide.hasAttribute('aria-label')) slide.setAttribute('aria-label', (i + 1) + ' of ' + slides.length);
    });
    // The scroll container is a tab stop so keyboard users can move it directly.
    if (!track.hasAttribute('tabindex')) track.tabIndex = 0;
    if (!track.hasAttribute('aria-label')) track.setAttribute('aria-label', 'Slides');
    [prev, next].forEach(button => { if (button) button.setAttribute('aria-controls', track.id); });
    dots.forEach((dot, i) => {
      dot.setAttribute('aria-controls', track.id);
      if (!dot.hasAttribute('aria-label')) dot.setAttribute('aria-label', 'Go to slide ' + (i + 1));
    });
    const status = document.createElement('span');
    status.className = 'k-car-status'; status.setAttribute('role', 'status');
    identify(status, 'kata-carousel-status'); root.append(status);

    const rtl = () => getComputedStyle(track).direction === 'rtl';
    // Distance from the track's inline-start edge, so RTL scrolling uses the same math.
    function offset(slide) {
      const a = slide.getBoundingClientRect(), b = track.getBoundingClientRect();
      return rtl() ? b.right - a.right : a.left - b.left;
    }
    function current() {
      let best = 0, distance = Infinity;
      slides.forEach((slide, i) => { const d = Math.abs(offset(slide)); if (d < distance) { distance = d; best = i; } });
      return best;
    }
    function still() {
      const scale = parseFloat(getComputedStyle(root).getPropertyValue('--k-mscale'));
      return matchMedia('(prefers-reduced-motion: reduce)').matches || scale === 0;
    }
    function go(index) {
      const target = slides[Math.max(0, Math.min(slides.length - 1, index))];
      const delta = offset(target);
      track.scrollBy({ left: rtl() ? -delta : delta, behavior: still() ? 'auto' : 'smooth' });
    }
    let shown = -1, announced = -1, timer = 0;
    function sync() {
      const index = current();
      if (index === shown) return;
      shown = index;
      dots.forEach((dot, i) => dot.setAttribute('aria-current', i === index ? 'true' : 'false'));
    }
    // Announce once the scroll settles, so a smooth jump does not report the slides it passes.
    function settle() {
      sync();
      if (shown === announced) return;
      announced = shown;
      status.textContent = 'Slide ' + (shown + 1) + ' of ' + slides.length;
      root.dispatchEvent(new CustomEvent('kata-carousel-change', { bubbles: true, detail: { index: shown, count: slides.length } }));
    }
    const native = 'onscrollend' in track;

    if (prev) prev.addEventListener('click', () => go(current() - 1));
    if (next) next.addEventListener('click', () => go(current() + 1));
    dots.forEach((dot, i) => dot.addEventListener('click', () => go(i)));
    track.addEventListener('keydown', event => {
      if (event.target !== track || event.isComposing || event.keyCode === 229) return;
      let index = null;
      if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
        // Horizontal arrows follow the visual direction; in RTL, Left moves forward.
        index = current() + (((event.key === 'ArrowRight') !== rtl()) ? 1 : -1);
      } else if (event.key === 'Home') index = 0;
      else if (event.key === 'End') index = slides.length - 1;
      if (index === null) return;
      event.preventDefault(); go(index);
    });
    track.addEventListener('scroll', () => {
      sync();
      if (!native) { clearTimeout(timer); timer = setTimeout(settle, 150); }
    }, { passive: true });
    if (native) track.addEventListener('scrollend', settle);
    sync(); announced = shown;
  });
})();
