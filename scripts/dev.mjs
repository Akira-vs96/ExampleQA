import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import { createServer } from "node:net";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const backendDirectory = join(projectRoot, "backend");
const frontendDirectory = join(projectRoot, "frontend");
const windows = process.platform === "win32";

const localPython = windows
  ? join(backendDirectory, ".venv", "Scripts", "python.exe")
  : join(backendDirectory, ".venv", "bin", "python");
const python = existsSync(localPython) ? localPython : windows ? "python" : "python3";
const npm = windows ? "npm.cmd" : "npm";

function portIsAvailable(port) {
  return new Promise((resolveAvailability) => {
    const server = createServer();
    server.unref();
    server.once("error", () => resolveAvailability(false));
    server.listen({ host: "127.0.0.1", port }, () => {
      server.close(() => resolveAvailability(true));
    });
  });
}

async function findAvailablePort(preferredPort) {
  for (let port = preferredPort; port < preferredPort + 100; port += 1) {
    if (await portIsAvailable(port)) return port;
  }
  throw new Error(`${preferredPort} портынан кейін бос порт табылмады.`);
}

function preferredPort(environmentName, fallback) {
  const value = Number(process.env[environmentName] ?? fallback);
  if (!Number.isInteger(value) || value < 1 || value > 65535) {
    throw new Error(`${environmentName} дұрыс порт нөмірі болуы керек.`);
  }
  return value;
}

const backendPort = await findAvailablePort(preferredPort("BACKEND_PORT", 8000));
const frontendPort = await findAvailablePort(preferredPort("FRONTEND_PORT", 5173));

const processes = [];
let stopping = false;

function start(name, command, args, cwd, extraEnvironment = {}) {
  const child = spawn(command, args, {
    cwd,
    stdio: "inherit",
    env: {
      ...process.env,
      PYTHONUNBUFFERED: "1",
      ...extraEnvironment,
    },
    detached: !windows,
  });

  child.on("error", (error) => {
    console.error(`[${name}] Іске қосу қатесі: ${error.message}`);
    stopAll(1);
  });

  child.on("exit", (code, signal) => {
    if (stopping) return;
    const reason = signal ? `signal ${signal}` : `код ${code ?? 0}`;
    console.error(`[${name}] Процесс тоқтады (${reason}).`);
    stopAll(code ?? 1);
  });

  processes.push(child);
}

function stopProcess(child, signal = "SIGTERM") {
  if (!child.pid || child.killed) return;
  try {
    if (windows) child.kill(signal);
    else process.kill(-child.pid, signal);
  } catch (error) {
    if (error.code !== "ESRCH") console.error(error);
  }
}

function stopAll(exitCode = 0) {
  if (stopping) return;
  stopping = true;
  for (const child of processes) stopProcess(child);
  setTimeout(() => {
    for (const child of processes) stopProcess(child, "SIGKILL");
    process.exit(exitCode);
  }, 800).unref();
}

console.log("DebugLab KZ іске қосылуда:");
console.log(`  Frontend: http://localhost:${frontendPort}`);
console.log(`  Backend:  http://localhost:${backendPort}`);
console.log(`  API docs: http://localhost:${backendPort}/docs\n`);

start(
  "backend",
  python,
  ["-m", "uvicorn", "main:app", "--reload", "--host", "127.0.0.1", "--port", String(backendPort)],
  backendDirectory,
);
start(
  "frontend",
  npm,
  ["run", "dev", "--", "--host", "127.0.0.1", "--port", String(frontendPort), "--strictPort"],
  frontendDirectory,
  {
    BACKEND_PORT: String(backendPort),
    FRONTEND_PORT: String(frontendPort),
  },
);

setTimeout(() => {
  if (stopping) return;
  console.log("\nАшу үшін сілтемелер:");
  console.log(`  Сайт:    http://localhost:${frontendPort}`);
  console.log(`  API:     http://localhost:${backendPort}`);
  console.log(`  Swagger: http://localhost:${backendPort}/docs`);
  console.log("  Тоқтату: Ctrl+C\n");
}, 1_000);

process.on("SIGINT", () => stopAll(0));
process.on("SIGTERM", () => stopAll(0));
