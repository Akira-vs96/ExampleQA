import { defineConfig, devices } from '@playwright/test';
import { python, root } from './scripts/python.mjs';

export default defineConfig({
  testDir: './backend/lab10/tests',
  fullyParallel: false,
  workers: 1,
  retries: 0,
  forbidOnly: Boolean(process.env.CI),
  timeout: 20_000,
  reporter: [
    ['list'],
    ['json', { outputFile: `backend/lab10/results/${process.env.UI_VARIANT === 'before' ? 'before' : 'after'}.json` }],
    ['html', { outputFolder: 'backend/lab10/results/html', open: 'never' }],
  ],
  use: { baseURL: 'http://127.0.0.1:8765', screenshot: 'only-on-failure', trace: 'retain-on-failure' },
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }],
  webServer: {
    command: `"${python}" -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8765 --no-server-header`,
    url: 'http://127.0.0.1:8765/api/health',
    cwd: root,
    env: { QA_DATABASE: `${root}/backend/.data/playwright.sqlite3` },
    reuseExistingServer: false,
    timeout: 20_000,
  },
});
