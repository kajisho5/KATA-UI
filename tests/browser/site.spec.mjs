import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

const pages = [
  '/',
  '/components/',
  '/components/button/',
  '/blocks/',
  '/blocks/login/',
  '/templates/',
  '/templates/dashboard/',
  '/docs/',
  '/pricing/',
  '/themes/'
];

test('representative pages render without uncaught page errors', async ({ page }) => {
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  for (const path of pages) {
    const response = await page.goto(path);
    expect(response, path + ' response').not.toBeNull();
    expect(response.status(), path + ' status').toBeLessThan(400);
    await expect(page.locator('body')).not.toBeEmpty();
  }
  expect(errors).toEqual([]);
});

test('homepage navigation and catalog search are operable', async ({ page }) => {
  await page.goto('/');
  const search = page.locator('[data-site-search]').first();
  if (await search.count()) {
    await search.click();
    const dialog = page.locator('[data-site-dialog]');
    await expect(dialog).toBeVisible();
    const input = dialog.locator('[data-site-input]');
    await input.fill('button');
    await expect(dialog.locator('[data-site-list]')).toContainText(/button/i);
    await page.keyboard.press('Escape');
  }
  await page.setViewportSize({ width: 390, height: 844 });
  const menu = page.locator('#menubtn');
  if (await menu.count()) {
    await menu.click();
    await expect(page.locator('#drawer')).toBeVisible();
    await page.keyboard.press('Escape');
  }
});

test('primary pages have no automatically detectable serious accessibility violations', async ({ page }) => {
  for (const path of ['/', '/components/', '/components/button/', '/docs/', '/pricing/']) {
    await page.goto(path);
    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
      .analyze();
    const serious = results.violations.filter(v => ['critical', 'serious'].includes(v.impact));
    expect(serious, path + ' serious/critical axe violations').toEqual([]);
  }
});

test('primary pages do not overflow horizontally at supported viewport widths', async ({ page }) => {
  for (const width of [360, 390, 430, 768, 1024, 1440]) {
    await page.setViewportSize({ width, height: 900 });
    for (const path of ['/', '/components/', '/components/button/', '/blocks/', '/templates/', '/docs/', '/pricing/', '/themes/']) {
      await page.goto(path);
      const dimensions = await page.evaluate(() => ({
        viewport: document.documentElement.clientWidth,
        document: document.documentElement.scrollWidth
      }));
      expect(
        dimensions.document,
        path + ' horizontal overflow at ' + width + 'px'
      ).toBeLessThanOrEqual(dimensions.viewport + 1);
    }
  }
});
