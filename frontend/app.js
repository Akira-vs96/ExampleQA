const filters = document.querySelectorAll('.filter');
const grid = document.querySelector('#work-grid');
const dialog = document.querySelector('#report-dialog');
let downloadUrl;
const lab12Evidence = document.querySelector('#lab12-evidence');
const evidenceStatus = document.querySelector('#lab12-evidence-status');
const evidenceComparison = document.querySelector('#lab12-comparison');
const evidenceFindings = document.querySelector('#lab12-findings');
const evidenceArtifacts = document.querySelector('#lab12-artifacts');
const lab13Evidence = document.querySelector('#lab13-evidence');
const lab13EvidenceStatus = document.querySelector('#lab13-evidence-status');
const lab13Comparison = document.querySelector('#lab13-comparison');
const lab13CodeArtifacts = document.querySelector('#lab13-code-artifacts');
const lab13ResultArtifacts = document.querySelector('#lab13-result-artifacts');
const lab14Evidence = document.querySelector('#lab14-evidence');
const lab14EvidenceStatus = document.querySelector('#lab14-evidence-status');
const lab14Comparison = document.querySelector('#lab14-comparison');
const lab14CodeArtifacts = document.querySelector('#lab14-code-artifacts');
const lab14ResultArtifacts = document.querySelector('#lab14-result-artifacts');
const lab15Evidence = document.querySelector('#lab15-evidence');
const lab15EvidenceStatus = document.querySelector('#lab15-evidence-status');
const lab15Summary = document.querySelector('#lab15-summary');
const lab15CodeArtifacts = document.querySelector('#lab15-code-artifacts');
const lab15ResultArtifacts = document.querySelector('#lab15-result-artifacts');

const lab12Files = [
  ['security-tests.log', 'pytest · журнал запуска npm run lab12'],
  ['before_after.json', 'SQL injection және XSS · before / after нәтижесі'],
  ['zap-summary.json', 'ZAP · қысқаша қорытынды'],
  ['zap-before.json', 'ZAP · осал нұсқаның толық есебі'],
  ['zap-after.json', 'ZAP · түзетілген нұсқаның толық есебі'],
  ['before-server.log', 'Осал нұсқа · сервер журналы'],
  ['before-zap.log', 'Осал нұсқа · ZAP журналы'],
  ['after-server.log', 'Түзетілген нұсқа · сервер журналы'],
  ['after-zap.log', 'Түзетілген нұсқа · ZAP журналы'],
];

function evidenceUrl(filename) {
  return new URL(`lab12-results/${encodeURIComponent(filename)}`, document.baseURI).href;
}

function labEvidenceUrl(labId, filename) {
  return new URL(`lab${labId}-results/${encodeURIComponent(filename)}`, document.baseURI).href;
}

async function readEvidence(filename) {
  const response = await fetch(evidenceUrl(filename));
  if (!response.ok) throw new Error(`${filename}: файл табылмады`);
  return response.text();
}

function evidenceNode(tag, value, className) {
  const node = document.createElement(tag);
  node.textContent = value;
  if (className) node.className = className;
  return node;
}

function formatZapCount(scan) {
  const counts = scan.alerts.reduce((result, alert) => {
    const risk = alert.risk || 'Other';
    result[risk] = (result[risk] || 0) + 1;
    return result;
  }, {});
  return `Барлығы: ${scan.alert_count}; High: ${counts.High || 0}; Medium: ${counts.Medium || 0}; Low: ${counts.Low || 0}`;
}

function renderArtifactFiles() {
  if (evidenceArtifacts.dataset.rendered === 'true') return;
  lab12Files.forEach(([filename, label]) => {
    const details = document.createElement('details');
    const summary = evidenceNode('summary', label);
    const link = document.createElement('a');
    link.href = evidenceUrl(filename);
    link.download = filename;
    link.textContent = `Ашу / жүктеу: ${filename}`;
    const preview = evidenceNode('pre', 'Файл ашылғанда мазмұны көрсетіледі.');
    preview.dataset.loaded = 'false';
    details.addEventListener('toggle', async () => {
      if (!details.open || preview.dataset.loaded === 'true') return;
      try {
        preview.textContent = await readEvidence(filename);
      } catch (error) {
        preview.textContent = error.message;
        preview.classList.add('evidence-error');
      }
      preview.dataset.loaded = 'true';
    });
    details.append(summary, link, preview);
    evidenceArtifacts.append(details);
  });
  evidenceArtifacts.dataset.rendered = 'true';
}

async function loadLab12Evidence() {
  if (lab12Evidence.dataset.loaded === 'true' || lab12Evidence.dataset.loaded === 'loading') return;
  lab12Evidence.dataset.loaded = 'loading';
  evidenceStatus.classList.remove('evidence-error');
  renderArtifactFiles();
  try {
    const [comparisonText, zapSummaryText, beforeText, afterText, testLog] = await Promise.all([
      readEvidence('before_after.json'),
      readEvidence('zap-summary.json'),
      readEvidence('zap-before.json'),
      readEvidence('zap-after.json'),
      readEvidence('security-tests.log'),
    ]);
    const comparison = JSON.parse(comparisonText);
    const zapSummary = JSON.parse(zapSummaryText);
    const beforeScan = JSON.parse(beforeText);
    const afterScan = JSON.parse(afterText);
    const testResult = testLog.match(/\d+ passed(?:, [^\n]+)?/);
    if (testResult) evidenceStatus.textContent = `Автотесттер: ${testResult[0]}. ZAP нұсқасы ${zapSummary.runs[0]?.version || '—'}; сканерлеу уақыты ${zapSummary.recorded_at || '—'}.`;
    else evidenceStatus.textContent = `ZAP нұсқасы ${zapSummary.runs[0]?.version || '—'}; сканерлеу уақыты ${zapSummary.recorded_at || '—'}.`;

    const beforeCard = evidenceNode('article', '', 'evidence-card');
    beforeCard.append(evidenceNode('h4', 'Before · осал нұсқа'));
    beforeCard.append(evidenceNode('p', `SQL injection: ${comparison.sql_injection_before}`));
    beforeCard.append(evidenceNode('p', `XSS: ${comparison.xss_before}`));
    beforeCard.append(evidenceNode('p', `ZAP: ${formatZapCount(beforeScan)}`));

    const afterCard = evidenceNode('article', '', 'evidence-card');
    afterCard.append(evidenceNode('h4', 'After · түзетілген нұсқа'));
    afterCard.append(evidenceNode('p', `SQL injection: ${comparison.sql_injection_after}`));
    afterCard.append(evidenceNode('p', `XSS: ${comparison.xss_after}`));
    afterCard.append(evidenceNode('p', `ZAP: ${formatZapCount(afterScan)}`));
    evidenceComparison.replaceChildren(beforeCard, afterCard);

    const findings = evidenceNode('section', '', 'evidence-findings');
    findings.append(evidenceNode('h4', 'ZAP тапқан мәселелер · before'));
    const list = document.createElement('ul');
    beforeScan.alerts.forEach((alert) => {
      list.append(evidenceNode('li', `${alert.risk}: ${alert.name} (${alert.url})`));
    });
    if (!beforeScan.alerts.length) list.append(evidenceNode('li', 'Ескерту табылмады.'));
    findings.append(list);
    const afterNote = evidenceNode('p', afterScan.alerts.length ? `After сканында ${afterScan.alerts.length} ескерту қалды.` : 'After сканында ескерту табылмады.');
    findings.append(afterNote);
    evidenceFindings.replaceChildren(findings);
    lab12Evidence.dataset.loaded = 'true';
  } catch (error) {
    evidenceStatus.textContent = `Дәлел файлдарын жүктеу мүмкін болмады: ${error.message}`;
    evidenceStatus.classList.add('evidence-error');
    lab12Evidence.dataset.loaded = 'false';
  }
}

const lab13CodeFiles = [
  ['before-pricing.py', '1 · Қате код — бастапқы pricing.py'],
  ['after-pricing.py', '2 · Түзетілген код — production pricing.py'],
  ['test_regression.py', 'Regression тестілер — 10 автоматтандырылған сценарий'],
];

const lab13ResultFiles = [
  ['before.txt', 'Before · қате нұсқадағы pytest нәтижесі'],
  ['after.txt', 'After · түзетілген нұсқадағы pytest нәтижесі'],
  ['comparison.json', 'Before / after салыстыруы · exit code және командалар'],
  ['before.xml', 'Before · JUnit XML есебі'],
  ['after.xml', 'After · JUnit XML есебі'],
  ['stability.json', 'Flaky test тексерісі · үш қайталау'],
  ['repeat-1.txt', 'Тұрақтылық тексерісі · іске қосу 1'],
  ['repeat-2.txt', 'Тұрақтылық тексерісі · іске қосу 2'],
  ['repeat-3.txt', 'Тұрақтылық тексерісі · іске қосу 3'],
];

function renderEvidenceArtifacts(container, labId, files) {
  if (container.dataset.rendered === 'true') return;
  files.forEach(([filename, label]) => {
    const details = document.createElement('details');
    const summary = evidenceNode('summary', label);
    const link = document.createElement('a');
    link.href = labEvidenceUrl(labId, filename);
    link.download = filename;
    link.textContent = `Ашу / жүктеу: ${filename}`;
    const preview = evidenceNode('pre', 'Файл ашылғанда мазмұны көрсетіледі.');
    preview.dataset.loaded = 'false';
    details.addEventListener('toggle', async () => {
      if (!details.open || preview.dataset.loaded === 'true') return;
      try {
        preview.textContent = await readEvidenceUrl(labEvidenceUrl(labId, filename));
      } catch (error) {
        preview.textContent = error.message;
        preview.classList.add('evidence-error');
      }
      preview.dataset.loaded = 'true';
    });
    details.append(summary, link, preview);
    container.append(details);
  });
  container.dataset.rendered = 'true';
}

async function readEvidenceUrl(url) {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`Evidence file табылмады (${response.status})`);
  return response.text();
}

async function loadLab13Evidence() {
  if (lab13Evidence.dataset.loaded === 'true' || lab13Evidence.dataset.loaded === 'loading') return;
  lab13Evidence.dataset.loaded = 'loading';
  lab13EvidenceStatus.classList.remove('evidence-error');
  renderEvidenceArtifacts(lab13CodeArtifacts, 13, lab13CodeFiles);
  renderEvidenceArtifacts(lab13ResultArtifacts, 13, lab13ResultFiles);
  try {
    const [comparisonText, beforeText, afterText, stabilityText] = await Promise.all([
      readEvidenceUrl(labEvidenceUrl(13, 'comparison.json')),
      readEvidenceUrl(labEvidenceUrl(13, 'before.txt')),
      readEvidenceUrl(labEvidenceUrl(13, 'after.txt')),
      readEvidenceUrl(labEvidenceUrl(13, 'stability.json')),
    ]);
    const comparison = JSON.parse(comparisonText);
    const stability = JSON.parse(stabilityText);
    const beforeSummary = beforeText.match(/\d+ failed, \d+ passed/)?.[0] || 'Нәтиже оқылмады';
    const afterSummary = afterText.match(/\d+ passed(?:, \d+ warning)?/)?.[0] || 'Нәтиже оқылмады';
    const runs = Object.fromEntries(comparison.runs.map((run) => [run.variant, run]));
    lab13EvidenceStatus.textContent = comparison.demonstration_passed
      ? `Кезекпен орындалды: before — ${beforeSummary} (exit ${runs.before?.exit_code}); after — ${afterSummary} (exit ${runs.after?.exit_code}). Flaky check: ${stability.runs.length} қайталау, ${stability.all_passed ? 'бәрі өтті' : 'сәтсіздік бар'}.`
      : 'Before / after демонстрациясының күтілген нәтижесі алынбады. Толық логтарды төменнен ашыңыз.';

    const beforeCard = evidenceNode('article', '', 'evidence-card');
    beforeCard.append(evidenceNode('h4', 'Before · қате нұсқа'));
    beforeCard.append(evidenceNode('p', `Нәтиже: ${beforeSummary}`));
    beforeCard.append(evidenceNode('p', `Күтілетін мінез-құлыққа сай өтпеген regression тесттері: ${beforeText.match(/\d+ failed/)?.[0] || '—'}.`));
    beforeCard.append(evidenceNode('p', 'Broken functions: line_total, discounted_total, shipping_cost, order_total, transition_order.'));

    const afterCard = evidenceNode('article', '', 'evidence-card');
    afterCard.append(evidenceNode('h4', 'After · түзетілген нұсқа'));
    afterCard.append(evidenceNode('p', `Нәтиже: ${afterSummary}`));
    afterCard.append(evidenceNode('p', 'Сол 10 regression тесттің барлығы өтті; іске қосу коды 0.'));
    afterCard.append(evidenceNode('p', 'Үш қайталама іске қосуда flaky failure байқалмады.'));
    lab13Comparison.replaceChildren(beforeCard, afterCard);
    lab13Evidence.dataset.loaded = 'true';
  } catch (error) {
    lab13EvidenceStatus.textContent = `Дәлел файлдарын жүктеу мүмкін болмады: ${error.message}`;
    lab13EvidenceStatus.classList.add('evidence-error');
    lab13Evidence.dataset.loaded = 'false';
  }
}

const lab14CodeFiles = [
  ['before-pricing.py', 'Before · қате pricing.py'],
  ['after-pricing.py', 'After · түзетілген pricing.py'],
  ['test_regression.py', '10 regression-тесттің source коды'],
  ['workflow.yml', 'GitHub Actions · build / test / analysis workflow'],
  ['requirements-dev.txt', 'CI үшін Python dependency-лері'],
];

const lab14ResultFiles = [
  ['before.txt', 'Before · қате нұсқадағы тест нәтижесі'],
  ['after.txt', 'After · түзетілген нұсқадағы тест нәтижесі'],
  ['comparison.json', 'Exit code және before / after реттілігі'],
  ['before.xml', 'Before · JUnit report'],
  ['after.xml', 'After · JUnit report'],
  ['pipeline-demo.log', 'Continuous Testing pipeline журналы'],
];

async function loadLab14Evidence() {
  if (lab14Evidence.dataset.loaded === 'true' || lab14Evidence.dataset.loaded === 'loading') return;
  lab14Evidence.dataset.loaded = 'loading';
  lab14EvidenceStatus.classList.remove('evidence-error');
  renderEvidenceArtifacts(lab14CodeArtifacts, 14, lab14CodeFiles);
  renderEvidenceArtifacts(lab14ResultArtifacts, 14, lab14ResultFiles);
  try {
    const [comparisonText, beforeText, afterText] = await Promise.all([
      readEvidenceUrl(labEvidenceUrl(14, 'comparison.json')),
      readEvidenceUrl(labEvidenceUrl(14, 'before.txt')),
      readEvidenceUrl(labEvidenceUrl(14, 'after.txt')),
    ]);
    const comparison = JSON.parse(comparisonText);
    const runs = Object.fromEntries(comparison.runs.map((run) => [run.variant, run]));
    const beforeSummary = beforeText.match(/\d+ failed, \d+ passed/)?.[0] || 'Нәтиже оқылмады';
    const afterSummary = afterText.match(/\d+ passed(?:, \d+ warning)?/)?.[0] || 'Нәтиже оқылмады';
    lab14EvidenceStatus.textContent = comparison.demonstration_passed
      ? `Жергілікті pipeline демонстрациясы: before — ${beforeSummary}, exit ${runs.before?.exit_code}; after — ${afterSummary}, exit ${runs.after?.exit_code}. GitHub Actions remote run push немесе manual dispatch кезінде орындалады.`
      : 'Before / after pipeline демонстрациясының күтілген нәтижесі алынбады. Толық логтарды ашыңыз.';

    const beforeCard = evidenceNode('article', '', 'evidence-card');
    beforeCard.append(evidenceNode('h4', 'Before · quality gate тоқтады'));
    beforeCard.append(evidenceNode('p', `Regression: ${beforeSummary}`));
    beforeCard.append(evidenceNode('p', `Test stage exit code: ${runs.before?.exit_code ?? '—'}`));
    beforeCard.append(evidenceNode('p', 'Қате есептеу assertion-дары сәтсіз болып, pipeline сәтсіз деп белгіленеді.'));

    const afterCard = evidenceNode('article', '', 'evidence-card');
    afterCard.append(evidenceNode('h4', 'After · quality gate өтті'));
    afterCard.append(evidenceNode('p', `Regression: ${afterSummary}`));
    afterCard.append(evidenceNode('p', `Test stage exit code: ${runs.after?.exit_code ?? '—'}`));
    afterCard.append(evidenceNode('p', 'Build, static analysis, 85% coverage gate және browser checks workflow ішінде ретімен орындалады.'));
    lab14Comparison.replaceChildren(beforeCard, afterCard);
    lab14Evidence.dataset.loaded = 'true';
  } catch (error) {
    lab14EvidenceStatus.textContent = `Дәлел файлдарын жүктеу мүмкін болмады: ${error.message}`;
    lab14EvidenceStatus.classList.add('evidence-error');
    lab14Evidence.dataset.loaded = 'false';
  }
}

const lab15CodeFiles = [
  ['before-pricing.py', 'Before · қате pricing есептеулері'],
  ['after-pricing.py', 'After · түзетілген pricing есептеулері'],
  ['before-security.py', 'Before · SQL injection және raw HTML ақаулары'],
  ['after-security.py', 'After · түзетілген SQLite/session сақтау коды'],
  ['safe-ui.js', 'After · браузерде қауіпсіз textContent қолдану'],
  ['test-regression.py', 'Regression suite · 10 тест'],
  ['test-security.py', 'Security suite · authentication / injection checks'],
  ['workflow.yml', 'GitHub Actions quality workflow'],
];

const lab15ResultFiles = [
  ['summary.md', 'Қорытынды QA есебі · метрикалар және release шешімі'],
  ['summary.json', 'Қорытынды метрикалар · JSON'],
  ['checks.json', 'CI quality stages нәтижесі'],
  ['full-checks.json', 'Full checks · browser / load / ZAP қоса'],
  ['pytest.xml', 'Full pytest suite нәтижесі · JUnit XML'],
  ['coverage.json', 'Statement және branch coverage'],
  ['coverage.xml', 'Coverage · Cobertura XML'],
  ['before-after.log', 'Бұрынғы және түзетілген нұсқалардың regression run-дары'],
  ['pipeline-demo.log', 'Lab 14 failed → fixed pipeline demo'],
  ['tests.log', 'Pytest және coverage журналы'],
  ['analysis.log', 'Ruff static analysis журналы'],
  ['build.log', 'Frontend және есептерді build журналы'],
  ['cases.log', '20 test case нәтижесі'],
  ['debugger.log', 'Debugging нәтижесі'],
  ['stability.log', 'Flaky regression test тексерісі'],
  ['browser.log', 'Chromium UI test нәтижесі'],
  ['load.log', 'Locust performance profile-дары'],
  ['security-demo.log', 'Security before / after тексерісі'],
  ['zap.log', 'OWASP ZAP passive scan нәтижесі'],
  ['zap-summary.json', 'ZAP alert саны before / after'],
  ['lab8.log', 'Pylint, Ruff және Radon analysis нәтижесі'],
];

function metricCard(title, lines) {
  const card = evidenceNode('article', '', 'evidence-card');
  card.append(evidenceNode('h4', title));
  lines.forEach((line) => card.append(evidenceNode('p', line)));
  return card;
}

async function loadLab15Evidence() {
  if (lab15Evidence.dataset.loaded === 'true' || lab15Evidence.dataset.loaded === 'loading') return;
  lab15Evidence.dataset.loaded = 'loading';
  lab15EvidenceStatus.classList.remove('evidence-error');
  renderEvidenceArtifacts(lab15CodeArtifacts, 15, lab15CodeFiles);
  renderEvidenceArtifacts(lab15ResultArtifacts, 15, lab15ResultFiles);
  document.querySelector('#lab15-performance-graph').src = labEvidenceUrl(15, 'performance.svg');
  try {
    const [summaryText, checksText] = await Promise.all([
      readEvidenceUrl(labEvidenceUrl(15, 'summary.json')),
      readEvidenceUrl(labEvidenceUrl(15, 'full-checks.json')),
    ]);
    const summary = JSON.parse(summaryText);
    const checks = JSON.parse(checksText);
    const testResults = summary.pytest;
    const coverage = summary.coverage;
    const load50 = summary.load.profiles.find((profile) => profile.profile === 'load50');
    const zapBefore = summary.zap.runs.find((scan) => scan.variant === 'before');
    const zapAfter = summary.zap.runs.find((scan) => scan.variant === 'after');
    const failingStages = checks.stages.filter((stage) => stage.exit_code !== 0);
    lab15EvidenceStatus.textContent = `${checks.stages.length} full quality stage: ${failingStages.length ? 'сәтсіз stage бар' : 'бәрі өтті'}. Localhost оқу демосы: ${summary.local_demo_ready ? 'GO' : 'NO GO'}; production release: ${summary.production_ready ? 'GO' : 'NO GO'}.`;
    lab15Summary.replaceChildren(
      metricCard('Автоматты тесттер', [`${testResults.passed}/${testResults.total} passed · pass rate ${testResults.pass_rate}%`, `${testResults.failed} failed · ${testResults.errors} errors · ${testResults.xfailed} expected failures · ${testResults.skipped} skipped`]),
      metricCard('Coverage', [`Statements: ${coverage.covered_lines}/${coverage.num_statements}`, `Branches: ${coverage.covered_branches}/${coverage.num_branches} · жалпы ${coverage.percent_covered}% · gate 85%`]),
      metricCard('Browser және load', [`Chromium: ${summary.browser.expected} passed · ${summary.browser.unexpected} failed`, `50 VU: p95 ${load50?.p95_ms ?? '—'} ms · error ${load50?.error_rate_percent ?? '—'}%`]),
      metricCard('Security retest', [`ZAP before: ${zapBefore?.alert_count ?? '—'} alert`, `ZAP after: ${zapAfter?.alert_count ?? '—'} alert · High: ${zapAfter?.high ?? '—'}`]),
      metricCard('Release readiness', [`Local demo: ${summary.local_demo_ready ? 'GO' : 'NO GO'}`, `Production: ${summary.production_ready ? 'GO' : 'NO GO'} · тәуекелдер қорытынды есепте берілген`]),
      metricCard('CI stages', [`${checks.stages.length - failingStages.length}/${checks.stages.length} passed`, `Failed stages: ${failingStages.length ? failingStages.map((stage) => stage.name).join(', ') : 'жоқ'}`]),
    );
    lab15Evidence.dataset.loaded = 'true';
  } catch (error) {
    lab15EvidenceStatus.textContent = `Дәлел файлдарын жүктеу мүмкін болмады: ${error.message}`;
    lab15EvidenceStatus.classList.add('evidence-error');
    lab15Evidence.dataset.loaded = 'false';
  }
}

function applyFilter(selected) {
  document.querySelectorAll('.work-card').forEach((card) => {
    card.classList.toggle('hidden', selected !== 'all' && card.dataset.kind !== selected);
  });
}

filters.forEach((filter) => {
  filter.addEventListener('click', () => {
    filters.forEach((item) => {
      item.classList.toggle('active', item === filter);
      item.setAttribute('aria-pressed', String(item === filter));
    });
    applyFilter(filter.dataset.filter);
  });
});

function showReport(lab) {
  document.querySelector('#report-title').textContent = lab.title;
  document.querySelector('#report-content').textContent = lab.report;
  lab12Evidence.hidden = lab.id !== 12;
  lab13Evidence.hidden = lab.id !== 13;
  lab14Evidence.hidden = lab.id !== 14;
  lab15Evidence.hidden = lab.id !== 15;
  if (lab.id === 12) loadLab12Evidence();
  if (lab.id === 13) loadLab13Evidence();
  if (lab.id === 14) loadLab14Evidence();
  if (lab.id === 15) loadLab15Evidence();
  if (downloadUrl) URL.revokeObjectURL(downloadUrl);
  downloadUrl = URL.createObjectURL(new Blob([lab.report], { type: 'text/markdown;charset=utf-8' }));
  const download = document.querySelector('#download-report');
  download.href = downloadUrl;
  download.download = `lab${lab.id}-report.md`;
  dialog.showModal();
}

document.querySelector('#close-report').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', (event) => { if (event.target === dialog) dialog.close(); });

fetch('./labs.json').then((response) => {
  if (!response.ok) throw new Error('Есептерді жүктеу мүмкін болмады.');
  return response.json();
}).then((labs) => {
  const fragment = document.createDocumentFragment();
  labs.forEach((lab) => {
    const card = document.createElement('article');
    card.className = `work-card${lab.id === 1 ? ' featured' : ''}`;
    card.dataset.kind = 'lab';
    const top = document.createElement('div');
    top.className = 'card-top';
    const tag = document.createElement('span');
    tag.className = 'tag lab-tag';
    tag.textContent = `LAB ${String(lab.id).padStart(2, '0')}`;
    top.append(tag);
    const title = document.createElement('h3');
    title.textContent = lab.title.replace(/^\d+\s*зертханалық жұмыс\s*[—–:]?\s*/i, '');
    const description = document.createElement('p');
    description.textContent = '20 тапсырманың есебі, орындау командалары және тексеру дәлелдері.';
    const button = document.createElement('button');
    button.className = 'card-link';
    button.type = 'button';
    button.textContent = 'Есепті оқу →';
    button.addEventListener('click', () => showReport(lab));
    card.append(top, title, description, button);
    fragment.append(card);
  });
  grid.prepend(fragment);
  document.querySelector('#catalogue-status').textContent = `${labs.length} зертханалық есеп қолжетімді.`;
  applyFilter(document.querySelector('.filter.active').dataset.filter);
}).catch((error) => { document.querySelector('#catalogue-status').textContent = error.message; });
