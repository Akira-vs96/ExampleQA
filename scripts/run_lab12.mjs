import { spawn } from 'node:child_process';
import { mkdir, writeFile } from 'node:fs/promises';
import { delimiter, join } from 'node:path';
import { python, root } from './python.mjs';

const args = ['-m', 'pytest', '-q', 'backend/lab12'];
const resultsDir = join(root, 'backend/lab12/results');
const chunks = [];
const child = spawn(python, args, {
  cwd: root,
  env: {
    ...process.env,
    PYTHONPATH: [join(root, 'backend'), root, process.env.PYTHONPATH]
      .filter(Boolean)
      .join(delimiter),
  },
  stdio: ['inherit', 'pipe', 'pipe'],
});

child.stdout.on('data', (chunk) => {
  chunks.push(chunk);
  process.stdout.write(chunk);
});
child.stderr.on('data', (chunk) => {
  chunks.push(chunk);
  process.stderr.write(chunk);
});

const exitCode = await new Promise((resolve) => {
  child.once('error', (error) => {
    const message = Buffer.from(`${error.message}\n`);
    chunks.push(message);
    process.stderr.write(message);
    resolve(1);
  });
  child.once('close', (code) => resolve(code ?? 1));
});

await mkdir(resultsDir, { recursive: true });
const log = [
  '$ npm run lab12',
  '$ python -m pytest -q backend/lab12',
  '',
  Buffer.concat(chunks).toString('utf8'),
].join('\n');
await writeFile(join(resultsDir, 'security-tests.log'), log, 'utf8');
process.exitCode = exitCode;
