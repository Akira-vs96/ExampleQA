const filters = document.querySelectorAll('.filter');
const cards = document.querySelectorAll('.work-card');

filters.forEach((filter) => {
  filter.addEventListener('click', () => {
    filters.forEach((item) => item.classList.remove('active'));
    filter.classList.add('active');

    const selected = filter.dataset.filter;
    cards.forEach((card) => {
      card.classList.toggle('hidden', selected !== 'all' && card.dataset.kind !== selected);
    });
  });
});
