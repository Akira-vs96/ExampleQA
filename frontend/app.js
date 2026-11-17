const filters = document.querySelectorAll('.filter');
const grid = document.querySelector('#work-grid');
const dialog = document.querySelector('#report-dialog');
let downloadUrl;
const lab12Evidence = document.querySelector('#lab12-evidence');
const evidenceStatus = document.querySelector('#lab12-evidence-status');
const evidenceComparison = document.querySelector('#lab12-comparison');
const evidenceFindings = document.querySelector('#lab12-findings');
const evidenceArtifacts = document.querySelector('#lab12-artifacts');

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
  if (lab.id === 12) loadLab12Evidence();
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
