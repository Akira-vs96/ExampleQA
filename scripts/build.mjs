import { cp, mkdir, readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { root } from './python.mjs';

const destination = join(root, 'dist');
await mkdir(destination, { recursive: true });
await cp(join(root, 'frontend'), destination, { recursive: true });
const labs = [];
for (let id = 1; id <= 15; id++) {
  const report = await readFile(join(root, `backend/lab${id}/REPORT.md`), 'utf8');
  labs.push({ id, title: report.split('\n')[0].replace(/^#+\s*/, ''), report, source: `backend/lab${id}` });
}
await writeFile(join(destination, 'labs.json'), JSON.stringify(labs, null, 2) + '\n');

const lab12Evidence = [
  'security-tests.log',
  'before_after.json',
  'zap-summary.json',
  'zap-before.json',
  'zap-after.json',
  'before-server.log',
  'before-zap.log',
  'after-server.log',
  'after-zap.log',
];
const evidenceDestination = join(destination, 'lab12-results');
await mkdir(evidenceDestination, { recursive: true });
for (const file of lab12Evidence) {
  try {
    await cp(join(root, 'backend/lab12/results', file), join(evidenceDestination, file));
  } catch (error) {
    if (error.code !== 'ENOENT') throw error;
  }
}
console.log(`Built ${labs.length} laboratory reports and Lab 12 evidence in dist/.`);
