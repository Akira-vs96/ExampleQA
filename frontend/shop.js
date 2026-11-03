const status = document.querySelector('#status');

async function api(path, options = {}) {
  const response = await fetch(`./api/shop${path}`, {
    ...options,
    headers: { 'Content-Type': 'application/json', ...options.headers },
  });
  const body = response.status === 204 ? null : await response.json();
  if (!response.ok) {
    throw new Error(typeof body.detail === 'string' ? body.detail : 'Деректерді тексеріңіз.');
  }
  return body;
}

async function search() {
  const query = document.querySelector('#query').value;
  const products = await api(`/products?q=${encodeURIComponent(query)}`);
  const list = document.querySelector('#products');
  list.replaceChildren();
  products.forEach((product) => {
    const item = document.createElement('li');
    item.textContent = `${product.name} · ${product.price} ₸`;
    list.append(item);
  });
  if (!products.length) {
    const empty = document.createElement('li');
    empty.textContent = 'Тауар табылмады.';
    list.append(empty);
  }
}

document.querySelector('#account-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const register = event.submitter?.id === 'register';
  const credentials = {
    username: document.querySelector('#username').value,
    password: document.querySelector('#password').value,
  };
  try {
    await api(register ? '/register' : '/login', { method: 'POST', body: JSON.stringify(credentials) });
    status.textContent = register ? 'Тіркелу сәтті. Енді жүйеге кіріңіз.' : `Қош келдіңіз, ${credentials.username}!`;
  } catch (error) { status.textContent = error.message; }
});

document.querySelector('#logout').addEventListener('click', async () => {
  try {
    await api('/session', { method: 'DELETE' });
    document.querySelector('#password').value = '';
    document.querySelector('#quote-result').textContent = '';
    status.textContent = 'Жүйеден шықтыңыз.';
  } catch (error) { status.textContent = error.message; }
});

document.querySelector('#search-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  try { await search(); } catch (error) { status.textContent = error.message; }
});

document.querySelector('#quote-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  try {
    const quote = await api('/quote', {
      method: 'POST',
      body: JSON.stringify({
        items: [{ product_id: Number(document.querySelector('#product').value), quantity: Number(document.querySelector('#quantity').value) }],
        percent: Number(document.querySelector('#percent').value),
      }),
    });
    document.querySelector('#quote-result').textContent = `Барлығы: ${quote.total} ₸ · жеткізу: ${quote.shipping} ₸`;
  } catch (error) {
    document.querySelector('#quote-result').textContent = '';
    status.textContent = error.message;
  }
});

search().catch((error) => { status.textContent = error.message; });
