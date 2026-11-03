import { spawn } from 'node:child_process';
import { createServer } from 'node:net';
import { python, root } from './python.mjs';

const preferred = Number(process.env.QA_PORT || process.env.BACKEND_PORT || 8000);
if (!Number.isInteger(preferred) || preferred < 1 || preferred > 65435) {
  throw new Error('QA_PORT must be a port between 1 and 65435.');
}

function available(port) {
  return new Promise((resolve) => {
    const server = createServer();
    server.once('error', () => resolve(false));
    server.listen(port, '127.0.0.1', () => server.close(() => resolve(true)));
  });
}

let port = preferred;
while (port < preferred + 100 && !(await available(port))) port++;
if (port === preferred + 100) throw new Error('No free local port.');
console.log(`DebugLab: http://127.0.0.1:${port}`);
console.log(`QA Shop:  http://127.0.0.1:${port}/shop.html`);
console.log(`API docs: http://127.0.0.1:${port}/docs`);

const child = spawn(python, ['-m', 'uvicorn', 'app.main:app', '--app-dir', 'backend',
  '--host', '127.0.0.1', '--port', String(port)], { cwd: root, stdio: 'inherit' });
child.on('error', (error) => { console.error(error.message); process.exitCode = 1; });
child.on('exit', (code) => { process.exitCode = code ?? 0; });
for (const signal of ['SIGINT', 'SIGTERM']) process.on(signal, () => child.kill(signal));
