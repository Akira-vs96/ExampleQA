const filters = document.querySelectorAll('.filter');
const grid = document.querySelector('#work-grid');
const dialog = document.querySelector('#report-dialog');
let downloadUrl;

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
