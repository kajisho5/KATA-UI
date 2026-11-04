/* Shared Foundry/theme export roles. Build injects the canonical contrast configuration. */
(function () {
  'use strict';
  const root = document.documentElement;
  if (root.dataset.kataColorReady) return;
  root.dataset.kataColorReady = 'true';
  const config = __KATA_COLOR_CONFIG__;
  const rgb = hex => hex.slice(1).match(/../g).map(c => parseInt(c, 16) / 255);
  const linear = c => c <= .04045 ? c / 12.92 : Math.pow((c + .055) / 1.055, 2.4);
  const encoded = c => c <= .0031308 ? 12.92 * c : 1.055 * Math.pow(c, 1 / 2.4) - .055;
  const hex = channels => '#' + channels.map(c => Math.round(Math.max(0, Math.min(1, c)) * 255).toString(16).padStart(2, '0')).join('');
  const luminance = value => rgb(value).reduce((sum, c, i) => sum + linear(c) * [.2126, .7152, .0722][i], 0);
  const contrast = (a, b) => (Math.max(luminance(a), luminance(b)) + .05) / (Math.min(luminance(a), luminance(b)) + .05);
  function roles(accent, mode) {
    const y = luminance(accent), inkY = luminance(config.darkText);
    const scale = Math.max(0, Math.min(inkY, (y + .05) / config.preferredMinimum - .05)) / inkY;
    const on = y < config.switchLuminance ? config.lightText : hex(rgb(config.darkText).map(c => encoded(linear(c) * scale)));
    const surface = y < config.switchLuminance ? '#000000' : '#ffffff';
    const weight = config.hoverAccentPercent / 100;
    const hover = hex(rgb(accent).map((c, i) => c * weight + rgb(surface)[i] * (1 - weight)));
    const target = mode === 'light' ? 0 : 1;
    const mixed = t => hex(rgb(accent).map(c => c + (target - c) * t));
    const passes = value => config.backgrounds[mode].every(bg => contrast(value, bg) >= config.preferredMinimum);
    let ink = accent;
    if (!passes(ink)) {
      let lo = 0, hi = 1;
      for (let i = 0; i < 24; i++) { const mid = (lo + hi) / 2; if (passes(mixed(mid))) hi = mid; else lo = mid; }
      ink = mixed(hi);
    }
    const channels = rgb(accent).map(c => Math.round(c * 255)).join(',');
    return {'--k-accent': accent, '--k-on-accent': on, '--k-accent-ink': ink, '--k-accent-contrast-surface': surface, '--k-accent-hover': hover, '--k-accent-bg': 'rgba(' + channels + ',.08)', '--k-accent-bg-strong': 'rgba(' + channels + ',.1)', '--k-accent-line': 'rgba(' + channels + ',.18)'};
  }
  function exportCSS(accent) {
    return '/* KATA theme: static WCAG color roles. Load after tokens.css. */\n' + ['light', 'dark'].map(mode => (mode === 'light' ? ':root,[data-theme="light"]' : '[data-theme="dark"]') + '{\n' + Object.entries(roles(accent, mode)).map(([name, value]) => '  ' + name + ':' + value + ';\n').join('') + '}').join('\n') + '\n';
  }
  document.addEventListener('kata:color-roles', event => {
    const detail = event.detail;
    if (!/^#[0-9a-f]{6}$/i.test(detail.accent)) return;
    if (detail.element) {
      const mode = detail.element.closest('[data-theme]')?.dataset.theme || root.dataset.theme || 'light';
      Object.entries(roles(detail.accent, mode)).forEach(([name, value]) => detail.element.style.setProperty(name, value));
    }
    if (detail.receive) detail.receive({css: exportCSS(detail.accent), light: roles(detail.accent, 'light'), dark: roles(detail.accent, 'dark')});
  });
  // Non-relative browsers still follow Foundry, while downloaded themes contain static roles.
  if (!CSS.supports('color', 'oklch(from red l c h)')) {
    const update = () => {
      const canvas = document.createElement('canvas'), ctx = canvas.getContext('2d');
      ctx.fillStyle = getComputedStyle(root).getPropertyValue('--k-accent').trim();
      const accent = ctx.fillStyle;
      if (!/^#[0-9a-f]{6}$/i.test(accent)) return;
      Object.entries(roles(accent, root.dataset.theme || 'light')).forEach(([name, value]) => {if (name !== '--k-accent' && root.style.getPropertyValue(name) !== value) root.style.setProperty(name, value);});
    };
    new MutationObserver(update).observe(root, {attributes: true, attributeFilter: ['style', 'data-theme']});
    document.addEventListener('DOMContentLoaded', update);
  }
  document.addEventListener('click', event => {
    if (!event.target.closest('[data-export-theme]')) return;
    const ctx = document.createElement('canvas').getContext('2d');
    ctx.fillStyle = getComputedStyle(root).getPropertyValue('--k-accent').trim();
    const css = exportCSS(ctx.fillStyle);
    const link = document.createElement('a'), url = URL.createObjectURL(new Blob([css], {type: 'text/css'}));
    link.href = url; link.download = 'kata-theme.css'; link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  });
})();
