import { test, expect } from '@playwright/test';
import { mkdirSync, readFileSync } from 'node:fs';

test.afterEach(async ({ page }, testInfo) => {
  const variant = process.env.UI_VARIANT || 'after';
  const safeTitle = testInfo.title.replace(/[^a-z0-9]+/gi, '-').replace(/^-|-$/g, '').toLowerCase();
  const outputDir = 'backend/lab10/results/task-screens';
  mkdirSync(outputDir, { recursive: true });
  await page.screenshot({
    path: `${outputDir}/${variant}-${safeTitle}.png`,
    fullPage: true,
  });
});

test.beforeEach(async ({ page }) => {
  if (process.env.UI_VARIANT === 'before') {
    await page.route('**/styles.css', async (route) => {
      const response = await route.fetch();
      await route.fulfill({ response, body: await response.text() + readFileSync('backend/lab10/before/layout.css', 'utf8') });
    });
  }
  await page.goto('/shop.html');
});

async function registerAndLogin(page) {
  const username = `qa_${Date.now()}_${Math.random().toString(36).slice(2, 7)}`;
  await page.getByLabel('Логин', { exact: true }).fill(username);
  await page.getByLabel('Пароль', { exact: true }).fill('Test_password_2026');
  await page.getByRole('button', { name: 'Тіркелу', exact: true }).click();
  await expect(page.locator('#status')).toContainText('Тіркелу сәтті');
  await page.getByRole('button', { name: 'Кіру', exact: true }).click();
  await expect(page.locator('#status')).toContainText('Қош келдіңіз');
}

test('registration and login', async ({ page }) => {
  await registerAndLogin(page);
  await expect(page.locator('#status')).toContainText('Қош келдіңіз');
});

test('invalid password does not authenticate', async ({ page }) => {
  await page.getByLabel('Логин', { exact: true }).fill('unknown_user');
  await page.getByLabel('Пароль', { exact: true }).fill('wrong_password');
  await page.getByRole('button', { name: 'Кіру', exact: true }).click();
  await expect(page.locator('#status')).toContainText('Логин немесе пароль қате');
});

test('form validation blocks short passwords', async ({ page }) => {
  await page.getByLabel('Логин', { exact: true }).fill('qa_user');
  await page.getByLabel('Пароль', { exact: true }).fill('123');
  await page.getByRole('button', { name: 'Тіркелу', exact: true }).click();
  expect(await page.getByLabel('Пароль', { exact: true }).evaluate((element) => element.validity.tooShort)).toBe(true);
  await expect(page.locator('#status')).toBeEmpty();
});

test('search is case insensitive', async ({ page }) => {
  await page.getByLabel('Тауарды іздеу').fill('KEYBOARD');
  await page.getByRole('button', { name: 'Іздеу', exact: true }).click();
  await expect(page.locator('#products li')).toHaveCount(1);
  await expect(page.locator('#products')).toContainText('Keyboard');
});

test('empty search returns the catalogue', async ({ page }) => {
  await expect(page.locator('#products li')).toHaveCount(3);
});

test('invalid input is rendered safely', async ({ page }) => {
  await page.getByLabel('Тауарды іздеу').fill('<img src=x onerror=alert(1)>');
  await page.getByRole('button', { name: 'Іздеу', exact: true }).click();
  await expect(page.locator('#products')).toHaveText('Тауар табылмады.');
  await expect(page.locator('#products img')).toHaveCount(0);
});

test('navigation returns to laboratory portal', async ({ page }) => {
  await page.getByRole('link', { name: '← Зертханалар' }).click();
  await expect(page).toHaveTitle(/DebugLab KZ/);
});

test('portal opens all fifteen reports and filters works', async ({ page }) => {
  await page.goto('/index.html');
  await expect(page.locator('[data-kind="lab"]')).toHaveCount(15);
  await page.getByRole('button', { name: 'Зертханалық 15', exact: true }).click();
  await expect(page.locator('[data-kind="sro"]:visible')).toHaveCount(0);
  await page.getByRole('button', { name: 'Есепті оқу →', exact: true }).first().click();
  await expect(page.getByRole('dialog')).toBeVisible();
  await expect(page.locator('#report-content')).toContainText('## 20');
  const downloadPromise = page.waitForEvent('download');
  await page.locator('#download-report').click();
  expect((await downloadPromise).suggestedFilename()).toBe('lab1-report.md');
  await page.getByRole('button', { name: 'Есепті жабу' }).click();
  await expect(page.getByRole('dialog')).not.toBeVisible();
});

test('quote uses discount before delivery', async ({ page }) => {
  await registerAndLogin(page);
  await page.getByRole('button', { name: 'Есептеу', exact: true }).click();
  await expect(page.locator('#quote-result')).toHaveText('Барлығы: 9000.00 ₸ · жеткізу: 1000.00 ₸');
});

test('logout revokes access', async ({ page }) => {
  await registerAndLogin(page);
  await page.getByRole('button', { name: 'Шығу', exact: true }).click();
  await expect(page.locator('#status')).toHaveText('Жүйеден шықтыңыз.');
  await page.getByRole('button', { name: 'Есептеу', exact: true }).click();
  await expect(page.locator('#status')).toHaveText('Алдымен жүйеге кіріңіз.');
});

for (const width of [375, 768, 1440]) {
  test(`responsive layout at ${width}px`, async ({ page }) => {
    await expect(page.locator('#products li')).toHaveCount(3);
    await page.setViewportSize({ width, height: 900 });
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
    await page.screenshot({ path: `backend/lab10/results/${process.env.UI_VARIANT || 'after'}-${width}.png`, fullPage: true });
    expect(overflow).toBe(false);
  });
}
