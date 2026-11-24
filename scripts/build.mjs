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

const lab13Evidence = [
  'before-pricing.py',
  'after-pricing.py',
  'test_regression.py',
  'before.txt',
  'after.txt',
  'before.xml',
  'after.xml',
  'comparison.json',
  'stability.json',
  'repeat-1.txt',
  'repeat-2.txt',
  'repeat-3.txt',
];
const lab13Destination = join(destination, 'lab13-results');
await mkdir(lab13Destination, { recursive: true });
for (const file of lab13Evidence) {
  const source = file === 'before-pricing.py'
    ? join(root, 'backend/lab6/before/pricing.py')
    : file === 'after-pricing.py'
      ? join(root, 'backend/qa_shop/pricing.py')
      : file === 'test_regression.py'
        ? join(root, 'backend/lab13/tests/test_regression.py')
        : join(root, 'backend/lab13/results', file);
  try {
    await cp(source, join(lab13Destination, file));
  } catch (error) {
    if (error.code !== 'ENOENT') throw error;
  }
}
console.log('Built Lab 13 source code and regression evidence in dist/lab13-results/.');

const lab14Evidence = {
  'before-pricing.py': 'backend/lab6/before/pricing.py',
  'after-pricing.py': 'backend/qa_shop/pricing.py',
  'test_regression.py': 'backend/lab13/tests/test_regression.py',
  'workflow.yml': '.github/workflows/labs.yml',
  'requirements-dev.txt': 'requirements-dev.txt',
  'before.txt': 'backend/lab14/results/before.txt',
  'after.txt': 'backend/lab14/results/after.txt',
  'before.xml': 'backend/lab14/results/before.xml',
  'after.xml': 'backend/lab14/results/after.xml',
  'comparison.json': 'backend/lab14/results/comparison.json',
  'pipeline-demo.log': 'backend/lab15/results/pipeline-demo.log',
};

const lab15Evidence = {
  'before-pricing.py': 'backend/lab6/before/pricing.py',
  'after-pricing.py': 'backend/qa_shop/pricing.py',
  'before-security.py': 'backend/lab12/before/security.py',
  'after-security.py': 'backend/qa_shop/store.py',
  'safe-ui.js': 'frontend/shop.js',
  'test-regression.py': 'backend/lab13/tests/test_regression.py',
  'test-security.py': 'backend/lab12/tests/test_security.py',
  'workflow.yml': '.github/workflows/labs.yml',
  'summary.md': 'backend/lab15/results/SUMMARY.md',
  'summary.json': 'backend/lab15/results/summary.json',
  'checks.json': 'backend/lab15/results/checks.json',
  'full-checks.json': 'backend/lab15/results/full-checks.json',
  'pytest.xml': 'backend/lab15/results/pytest.xml',
  'coverage.json': 'backend/lab15/results/coverage.json',
  'coverage.xml': 'backend/lab15/results/coverage.xml',
  'before-after.log': 'backend/lab15/results/before-after.log',
  'pipeline-demo.log': 'backend/lab15/results/pipeline-demo.log',
  'tests.log': 'backend/lab15/results/tests.log',
  'build.log': 'backend/lab15/results/build.log',
  'analysis.log': 'backend/lab15/results/analysis.log',
  'cases.log': 'backend/lab15/results/cases.log',
  'debugger.log': 'backend/lab15/results/debugger.log',
  'stability.log': 'backend/lab15/results/stability.log',
  'browser.log': 'backend/lab15/results/browser.log',
  'load.log': 'backend/lab15/results/load.log',
  'security-demo.log': 'backend/lab15/results/security-demo.log',
  'zap.log': 'backend/lab15/results/zap.log',
  'lab8.log': 'backend/lab15/results/lab8.log',
  'zap-summary.json': 'backend/lab12/results/zap-summary.json',
  'performance.svg': 'backend/lab11/results/performance.svg',
};

for (const [lab, files] of Object.entries({ 14: lab14Evidence, 15: lab15Evidence })) {
  const labDestination = join(destination, `lab${lab}-results`);
  await mkdir(labDestination, { recursive: true });
  for (const [filename, sourcePath] of Object.entries(files)) {
    await cp(join(root, sourcePath), join(labDestination, filename));
  }
}
console.log('Built Lab 14 CI/CD and Lab 15 quality evidence in dist/.');
