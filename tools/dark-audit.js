#!/usr/bin/env node
/* KATA UI dark-mode audit — run after every build, before every deploy.
 *
 * Catches the 2026-11-03 incident class: surfaces that stay light inside a
 * dark page. Checks, at desktop width, with the cast state set to dark:
 *   1. Every iframe on the landing page shares the parent's theme.
 *   2. No "light slab": no visible element painted near-white over more
 *      than 20% of the viewport, outside an intentional [data-theme="light"]
 *      stage subtree.
 *   3. A template demo opened standalone under a dark system preference
 *      renders dark (no saved state).
 *   4. The same slab check on /pricing/, /design-system/, /themes/,
 *      /components/ and one component detail page.
 *
 * Usage: node tools/dark-audit.js [baseUrl]   (default http://127.0.0.1:8901)
 * Needs playwright-core; set PW_PATH if it is not resolvable here.
 */
const pwPath = process.env.PW_PATH || '/home/hatch/workspace/tools/pshot/node_modules/playwright-core';
const { chromium } = require(pwPath);
const BASE = process.argv[2] || 'http://127.0.0.1:8901';

const SLAB_FN = () => {
  const vw = innerWidth, vh = innerHeight;
  const bad = [];
  const inLightStage = el => !!el.closest('[data-theme="light"]');
  document.querySelectorAll('body *').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width < 40 || r.height < 40) return;
    const visW = Math.max(0, Math.min(r.right, vw) - Math.max(r.left, 0));
    const visH = Math.max(0, Math.min(r.bottom, vh) - Math.max(r.top, 0));
    if (visW * visH < vw * vh * 0.2) return;
    const bg = getComputedStyle(el).backgroundColor;
    const m = bg.match(/[\d.]+/g);
    if (!m) return;
    const [rr, gg, bb, aa] = m.map(Number);
    if (aa !== undefined && aa < 0.5) return;
    if (rr > 238 && gg > 238 && bb > 238 && !inLightStage(el)) {
      bad.push(el.tagName + '.' + (el.className.baseVal !== undefined ? '' : String(el.className).slice(0, 40)) + ' ' + Math.round(r.width) + 'x' + Math.round(r.height) + ' bg=' + bg);
    }
  });
  return bad;
};

(async () => {
  const browser = await chromium.launch();
  const failures = [];
  const initDark = () => { try { localStorage.setItem('kata-fdeck', JSON.stringify({ dark: true })); } catch (e) {} };

  const page = await browser.newPage({ viewport: { width: 1280, height: 1000 } });
  await page.addInitScript(initDark);

  // 1 + 2 on the landing page (scroll through so lazy surfaces mount)
  await page.goto(BASE + '/', { waitUntil: 'networkidle' });
  const rootTheme = await page.evaluate(() => document.documentElement.getAttribute('data-theme'));
  if (rootTheme !== 'dark') failures.push('LP: root did not enter dark mode');
  for (let y = 0; y < 12; y++) {
    await page.evaluate(yy => scrollTo(0, yy * 900), y);
    await page.waitForTimeout(220);
    const slabs = await page.evaluate(SLAB_FN);
    slabs.forEach(s => failures.push(`LP scroll ${y}: light slab ${s}`));
  }
  // activate every showcase tab so lazy iframes really load, then check parity
  const tabCount = await page.locator('[data-sctab]').count();
  for (let i = 0; i < tabCount; i++) {
    await page.locator('[data-sctab]').nth(i).click();
    await page.waitForTimeout(700);
  }
  const frames = page.frames().filter(f => f !== page.mainFrame() && !f.url().endsWith('about:blank') && f.url() !== 'about:blank');
  for (const f of frames) {
    const t = await f.evaluate(() => document.documentElement.getAttribute('data-theme')).catch(() => '(unreachable)');
    if (t !== 'dark') failures.push(`LP iframe ${f.url()} theme=${t}, expected dark`);
  }

  // 4: slab check on key pages
  for (const path of ['/pricing/', '/design-system/', '/themes/', '/components/', '/components/button/']) {
    await page.goto(BASE + path, { waitUntil: 'networkidle' });
    await page.waitForTimeout(300);
    const slabs = await page.evaluate(SLAB_FN);
    slabs.forEach(s => failures.push(`${path}: light slab ${s}`));
  }

  // 3: standalone demo under system dark, no saved state
  const ctx = await browser.newContext({ colorScheme: 'dark', viewport: { width: 1100, height: 800 } });
  const dp = await ctx.newPage();
  await dp.goto(BASE + '/templates/dashboard/demo/', { waitUntil: 'networkidle' });
  const dt = await dp.evaluate(() => document.documentElement.getAttribute('data-theme'));
  if (dt !== 'dark') failures.push(`standalone demo theme=${dt}, expected dark under system-dark`);

  await browser.close();
  if (failures.length) {
    console.log('DARK AUDIT FAIL (' + failures.length + ')');
    failures.forEach(f => console.log(' - ' + f));
    process.exit(1);
  }
  console.log('DARK AUDIT PASS — no light slabs, iframes in parity, standalone demo follows system dark');
})().catch(e => { console.error(e); process.exit(1); });
