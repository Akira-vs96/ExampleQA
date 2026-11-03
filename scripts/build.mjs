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
console.log(`Built ${labs.length} laboratory reports and static portal in dist/.`);
