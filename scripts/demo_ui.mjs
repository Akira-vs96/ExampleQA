import { spawnSync } from 'node:child_process';
import { mkdirSync, writeFileSync } from 'node:fs';
import { root } from './python.mjs';

const directory = `${root}/backend/lab10/results`;
mkdirSync(directory, { recursive: true });
const comparison = { recorded_at: new Date().toISOString(), runs: [] };
for (const variant of ['before', 'after']) {
  const result = spawnSync(process.execPath, ['node_modules/@playwright/test/cli.js', 'test'], {
    cwd: root, encoding: 'utf8', timeout: 90_000,
    env: { ...process.env, UI_VARIANT: variant },
  });
  writeFileSync(`${directory}/${variant}.log`, (result.stdout || '') + (result.stderr || ''));
  comparison.runs.push({ variant, exit_code: result.status, error: result.error?.message || null });
  console.log(`Chromium ${variant}: exit ${result.status}`);
}
comparison.demonstration_passed = comparison.runs[0].exit_code === 1 && comparison.runs[1].exit_code === 0;
writeFileSync(`${directory}/comparison.json`, JSON.stringify(comparison, null, 2) + '\n');
if (!comparison.demonstration_passed) console.error('Inspect backend/lab10/results/before.log and after.log');
process.exitCode = comparison.demonstration_passed ? 0 : 1;
