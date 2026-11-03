import { existsSync } from 'node:fs';
import { delimiter, join, resolve } from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

export const root = fileURLToPath(new URL('../', import.meta.url));
const bin = process.platform === 'win32' ? 'Scripts/python.exe' : 'bin/python';
export const python = process.env.QA_PYTHON || [
  join(root, '.venv', bin), join(root, 'backend/.venv', bin),
].find(existsSync) || (process.platform === 'win32' ? 'python' : 'python3');

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const result = spawnSync(python, process.argv.slice(2), { cwd: root, stdio: 'inherit',
    env: { ...process.env, PYTHONPATH: [join(root, 'backend'), root, process.env.PYTHONPATH].filter(Boolean).join(delimiter) },
  });
  if (result.error) console.error(result.error.message);
  process.exitCode = result.status ?? 1;
}
