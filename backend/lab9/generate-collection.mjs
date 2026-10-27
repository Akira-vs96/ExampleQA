import { writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const directory = fileURLToPath(new URL('.', import.meta.url));
const json = (name, value) => writeFileSync(`${directory}${name}`, `${JSON.stringify(value, null, 2)}\n`);
const scenarios = [];
const check = (name, code) => `pm.test(${JSON.stringify(name)}, function () { ${code} });`;
const errorBody = check('Қате туралы хабарлама бар', 'pm.expect(data.message).to.be.a("string").and.not.empty;');
const productSchema = {
  type: 'object',
  required: ['id', 'title', 'price', 'category', 'stock'],
  properties: {
    id: { type: 'integer', minimum: 1 },
    title: { type: 'string', minLength: 1 },
    price: { type: 'number', minimum: 0 },
    category: { type: 'string', minLength: 1 },
    stock: { type: 'integer', minimum: 0 },
  },
};
const schemaCheck = check('Product JSON Schema дұрыс', `pm.response.to.have.jsonSchema(${JSON.stringify(productSchema)});`);

function add(group, title, method, path, expected, purpose, tests, options = {}) {
  const id = `TC${String(scenarios.length + 1).padStart(2, '0')}`;
  const script = [
    check(`HTTP ${expected}`, `pm.response.to.have.status(${expected});`),
    // `data` is a predefined sandbox variable (iteration data) in Postman/Newman.
    'var responseData = pm.response.json();',
    ...tests.map(code => code.replace(/\bdata\b/g, 'responseData')),
  ];
  const request = {
    method,
    header: [{ key: 'Accept', value: 'application/json', type: 'text' }],
    auth: options.auth ?? { type: 'noauth' },
    url: { raw: `{{baseUrl}}${path}`, host: ['{{baseUrl}}'], path: path.split('?')[0].slice(1).split('/') },
    description: `${id}. ${purpose}\n\nКүтілетін HTTP коды: ${expected}. Барлық сұраныстарда JSON, Content-Type және Response Time тексеріледі.`,
  };
  if (path.includes('?')) {
    request.url.query = path.split('?')[1].split('&').map(pair => {
      const [key, ...value] = pair.split('=');
      return { key, value: value.join('=') };
    });
  }
  if (options.body !== undefined || options.raw !== undefined) {
    request.header.push({ key: 'Content-Type', value: 'application/json', type: 'text' });
    request.body = {
      mode: 'raw',
      raw: options.raw ?? JSON.stringify(options.body, null, 2),
      options: { raw: { language: 'json' } },
    };
  }
  if (options.headers) request.header.push(...options.headers);
  const item = {
    name: `${id} — ${title}`,
    // A login also sets cookies. Disable the jar so authentication tests exercise only Bearer headers.
    protocolProfileBehavior: { disableCookies: true },
    request,
    event: [{ listen: 'test', script: { type: 'text/javascript', exec: script } }],
    response: [],
  };
  scenarios.push({ id, group, title, method, path, expected, purpose, item });
}

add('01 — GET және пагинация', 'API қолжетімділігі', 'GET', '/test', 200,
  'Сервис жұмысын және HTTP әдісінің echo жауабын тексеру.', [
    check('API status=ok, method=GET', 'pm.expect(data).to.include({status: "ok", method: "GET"});'),
  ]);
add('01 — GET және пагинация', 'Тауарлар тізімі', 'GET', '/products?limit=10&skip=0', 200,
  'Он тауардың құрылымын, санын және пагинация метадеректерін тексеру.', [
    check('10 тауар және метадеректер', 'pm.expect(data.products).to.be.an("array").with.lengthOf(10); pm.expect(data.limit).to.eql(10); pm.expect(data.skip).to.eql(0); pm.expect(data.total).to.be.a("number").and.at.least(10);'),
    check('Тізімдегі әрбір Product schema дұрыс', `data.products.forEach(product => pm.expect(product).to.have.jsonSchema(${JSON.stringify(productSchema)}));`),
    'pm.collectionVariables.set("total", data.total);',
  ]);
add('01 — GET және пагинация', 'Бір тауарды алу', 'GET', '/products/1', 200,
  'id=1 тауарын алу; бастапқы title және price мәндерін кейінгі салыстыруға сақтау.', [
    schemaCheck,
    check('id=1', 'pm.expect(data.id).to.eql(1);'),
    'pm.collectionVariables.set("originalTitle", data.title);',
    'pm.collectionVariables.set("originalPrice", data.price);',
  ]);
add('01 — GET және пагинация', 'Іздеу', 'GET', '/products/search?q=phone&limit=5', 200,
  'phone іздеу нәтижелерін және limit шектеуін тексеру.', [
    check('Іздеу нәтижесі бос емес және limit сақталған', 'pm.expect(data.products).to.be.an("array"); pm.expect(data.products.length).to.be.within(1, 5); pm.expect(data.total).to.be.at.least(data.products.length);'),
    check('Іздеу нәтижелерінде phone кездеседі', 'data.products.forEach(p => pm.expect(JSON.stringify(p).toLowerCase()).to.include("phone"));'),
  ]);
add('01 — GET және пагинация', 'Boundary: limit=1, skip=0', 'GET', '/products?limit=1&skip=0', 200,
  'Ең кіші оң page size және төменгі skip шекарасын тексеру.', [
    check('Бірінші бір тауар', 'pm.expect(data.products).to.have.lengthOf(1); pm.expect(data.products[0].id).to.eql(1); pm.expect(data.skip).to.eql(0); pm.expect(data.limit).to.eql(1);'),
    'pm.collectionVariables.set("firstId", data.products[0].id);',
  ]);
add('01 — GET және пагинация', 'Boundary: skip=1', 'GET', '/products?limit=1&skip=1', 200,
  'Бірінші жазбаны өткізіп, келесі тауардың келуін тексеру.', [
    check('Басқа тауар және skip=1', 'pm.expect(data.products).to.have.lengthOf(1); pm.expect(data.products[0].id).not.to.eql(Number(pm.collectionVariables.get("firstId"))); pm.expect(data.skip).to.eql(1);'),
  ]);
add('01 — GET және пагинация', 'Boundary: limit=0', 'GET', '/products?limit=0&select=id', 200,
  'Құжаттама бойынша limit=0 барлық жазбаларды қайтарады; нақты соңғы және жоқ ID мәндерін есептеу.', [
    check('Барлық ID қайтарылды', 'pm.expect(data.products).to.be.an("array").and.not.empty; pm.expect(data.products.length).to.eql(data.total); pm.expect(data.skip).to.eql(0); data.products.forEach(p => pm.expect(p.id).to.be.a("number"));'),
    check('select=id артық өрістерді алып тастайды', 'data.products.forEach(p => pm.expect(p).to.have.all.keys("id"));'),
    'const lastId = Math.max(...data.products.map(p => p.id));',
    'pm.collectionVariables.set("lastId", lastId);',
    'pm.collectionVariables.set("missingId", lastId + 100000);',
    'pm.collectionVariables.set("total", data.total);',
    'pm.collectionVariables.set("lastOffset", data.total - 1);',
    'pm.collectionVariables.set("beyondOffset", data.total + 1);',
  ]);
add('02 — Теріс және шекаралық мәндер', 'Boundary: соңғы жарамды ID', 'GET', '/products/{{lastId}}', 200,
  'Жоғарғы жарамды ID шекарасында тауардың бар екенін тексеру.', [
    schemaCheck,
    check('Соңғы ID сәйкес', 'pm.expect(data.id).to.eql(Number(pm.collectionVariables.get("lastId")));'),
  ]);
add('02 — Теріс және шекаралық мәндер', 'Boundary: ID=0', 'GET', '/products/0', 404,
  'Ең кіші жарамды ID-ден төмен мән үшін 404 күту.', [errorBody]);
add('02 — Теріс және шекаралық мәндер', 'Жоқ ID', 'GET', '/products/{{missingId}}', 404,
  'Жоғарғы ID шекарасынан тыс ресурс үшін 404 күту.', [errorBody]);
add('02 — Теріс және шекаралық мәндер', 'Қате параметр: мәтіндік ID', 'GET', '/products/abc', 404,
  'Сандық ID орнына abc жіберу; DummyJSON-ның нақты шарты — 404.', [errorBody]);
add('02 — Теріс және шекаралық мәндер', 'Бос параметр: q=', 'GET', '/products/search?q=&limit=5', 200,
  'Бос іздеу жолы барлық тауарлар жиынын іздейді; 400 күтпейміз.', [
    check('Бос q толық жиыннан бет қайтарады', 'pm.expect(data.total).to.eql(Number(pm.collectionVariables.get("total"))); pm.expect(data.products).to.have.lengthOf(5);'),
  ]);
add('02 — Теріс және шекаралық мәндер', 'Boundary: skip=total', 'GET', '/products?limit=1&skip={{total}}', 200,
  'Соңғы жазбадан кейінгі offset бос массив қайтаруы тиіс.', [
    check('Нәтиже бос, total сақталған', 'pm.expect(data.products).to.eql([]); pm.expect(data.total).to.eql(Number(pm.collectionVariables.get("total"))); pm.expect(data.skip).to.eql(data.total);'),
  ]);
add('02 — Теріс және шекаралық мәндер', 'Boundary: skip=total−1', 'GET', '/products?limit=1&skip={{lastOffset}}', 200,
  'Соңғы қолжетімді бетте бір жазба болуы тиіс.', [
    check('Соңғы бетте бір тауар', 'pm.expect(data.products).to.have.lengthOf(1); pm.expect(data.products[0].id).to.eql(Number(pm.collectionVariables.get("lastId"))); pm.expect(data.skip).to.eql(Number(pm.collectionVariables.get("lastOffset")));'),
  ]);
add('02 — Теріс және шекаралық мәндер', 'Boundary: skip=total+1', 'GET', '/products?limit=1&skip={{beyondOffset}}', 200,
  'Жиыннан тыс offset сервер қатесін тудырмай, бос массив қайтарады.', [
    check('Шектен тыс бет бос', 'pm.expect(data.products).to.eql([]); pm.expect(data.total).to.eql(Number(pm.collectionVariables.get("total"))); pm.expect(data.skip).to.eql(Number(pm.collectionVariables.get("beyondOffset")));'),
  ]);

add('03 — POST PUT PATCH DELETE', 'POST: тауар қосу', 'POST', '/products/add', 201,
  'Жаңа тауарды имитациялық жасау және жіберілген өрістерді тексеру.', [
    check('Жасалған тауар өрістері', 'pm.expect(data).to.include({title: "Lab9 Test Product", price: 29.99, stock: 10}); pm.expect(data.id).to.be.above(Number(pm.collectionVariables.get("lastId")));'),
    'pm.collectionVariables.set("createdId", data.id);',
  ], { body: { title: 'Lab9 Test Product', price: 29.99, stock: 10 } });
add('03 — POST PUT PATCH DELETE', 'POST нәтижесі серверде сақталмайды', 'GET', '/products/{{createdId}}', 404,
  'Құжаттамадағы POST имитациясын тәуелсіз GET арқылы дәлелдеу.', [errorBody]);
add('03 — POST PUT PATCH DELETE', 'PUT: title және price өзгерту', 'PUT', '/products/1', 200,
  'DummyJSON PUT өңдеуін тексеру: жіберілген title және price жаңартылады.', [
    check('PUT өрістері жаңартылған', 'pm.expect(data).to.include({id: 1, title: "Lab9 PUT Product", price: 49.99});'),
    schemaCheck,
  ], { body: { title: 'Lab9 PUT Product', price: 49.99 } });
add('03 — POST PUT PATCH DELETE', 'PATCH: тек price өзгерту', 'PATCH', '/products/1', 200,
  'price өзгеріп, жіберілмеген title бастапқы мәнін сақтауын тексеру.', [
    check('price өзгерді, title сақталды', 'pm.expect(data.id).to.eql(1); pm.expect(data.price).to.eql(19.99); pm.expect(data.title).to.eql(pm.collectionVariables.get("originalTitle"));'),
  ], { body: { price: 19.99 } });
add('03 — POST PUT PATCH DELETE', 'PUT/PATCH өзгерістері сақталмайды', 'GET', '/products/1', 200,
  'Бастапқы тауардың өзгермегенін тәуелсіз GET арқылы тексеру.', [
    check('Бастапқы title және price', 'pm.expect(data.title).to.eql(pm.collectionVariables.get("originalTitle")); pm.expect(data.price).to.eql(Number(pm.collectionVariables.get("originalPrice")));'),
  ]);
add('03 — POST PUT PATCH DELETE', 'DELETE: тауарды жою', 'DELETE', '/products/1', 200,
  'Жою имитациясында id, isDeleted және deletedOn өрістерін тексеру.', [
    check('Жою расталған', 'pm.expect(data).to.include({id: 1, isDeleted: true}); pm.expect(data.deletedOn).to.be.a("string"); pm.expect(Number.isNaN(Date.parse(data.deletedOn))).to.eql(false);'),
  ]);
add('03 — POST PUT PATCH DELETE', 'DELETE нәтижесі серверде сақталмайды', 'GET', '/products/1', 200,
  'Имитациялық жоюдан кейін ресурс қолжетімді болып қалатынын тексеру.', [
    check('Тауар әлі бар', 'pm.expect(data.id).to.eql(1); pm.expect(data.title).to.eql(pm.collectionVariables.get("originalTitle")); pm.expect(data).not.to.have.property("isDeleted");'),
  ]);
add('03 — POST PUT PATCH DELETE', 'PUT: жоқ ресурс', 'PUT', '/products/{{missingId}}', 404,
  'Жоқ тауарды PUT арқылы жаңарту қатесін тексеру.', [errorBody], { body: { title: 'Missing' } });
add('03 — POST PUT PATCH DELETE', 'PATCH: жоқ ресурс', 'PATCH', '/products/{{missingId}}', 404,
  'Жоқ тауарды PATCH арқылы жаңарту қатесін тексеру.', [errorBody], { body: { price: 1 } });
add('03 — POST PUT PATCH DELETE', 'DELETE: жоқ ресурс', 'DELETE', '/products/{{missingId}}', 404,
  'Жоқ тауарды жою үшін 404 күту.', [errorBody]);
add('03 — POST PUT PATCH DELETE', 'POST: бүлінген JSON', 'POST', '/products/add', 400,
  'Синтаксисі бұзылған JSON үшін клиент қатесін тексеру.', [errorBody], { raw: '{"title":' });

add('04 — Authentication', 'Токен жоқ', 'GET', '/auth/me', 401,
  'Cookie jar өшірілген: Authorization жоқ сұранысқа 401 күту.', [
    errorBody,
    check('Қорғалған профиль берілмеді', 'pm.expect(data).not.to.have.property("username");'),
  ]);
add('04 — Authentication', 'Жарамсыз Bearer токен', 'GET', '/auth/me', 401,
  'Жарамсыз токенді сервердің қабылдамауын тексеру.', [errorBody], {
    headers: [{ key: 'Authorization', value: 'Bearer lab9-invalid-token', type: 'text' }],
  });
add('04 — Authentication', 'Қате құпиясөз', 'POST', '/auth/login', 400,
  'Қате пароль үшін DummyJSON шарты бойынша 400 және токеннің болмауын тексеру.', [
    errorBody,
    check('Токен берілмеді', 'pm.expect(data).not.to.have.property("accessToken");'),
  ], { body: { username: '{{username}}', password: 'lab9-wrong-password' } });
add('04 — Authentication', 'Бос логин және пароль', 'POST', '/auth/login', 400,
  'Екі бос міндетті параметрмен кірудің қабылданбауын тексеру.', [errorBody], {
    body: { username: '', password: '' },
  });
add('04 — Authentication', 'Міндетті password параметрі жоқ', 'POST', '/auth/login', 400,
  'Бос мән мен мүлде жоқ параметрді бөлек тексеру.', [errorBody], { body: { username: '{{username}}' } });
add('04 — Authentication', 'Дұрыс логин: токен алу', 'POST', '/auth/login', 200,
  'Құжаттамадағы ашық демо деректермен кіру; accessToken-ді автоматты сақтау.', [
    check('Дұрыс пайдаланушы', 'pm.expect(data.username).to.eql(pm.environment.get("username")); pm.expect(data.id).to.be.a("number");'),
    check('Access және refresh JWT берілген', String.raw`pm.expect(data.accessToken).to.be.a("string").and.match(/^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$/); pm.expect(data.refreshToken).to.be.a("string").and.not.empty;`),
    'pm.collectionVariables.set("accessToken", data.accessToken);',
    'pm.collectionVariables.set("userId", data.id);',
  ], { body: { username: '{{username}}', password: '{{password}}', expiresInMins: 30 } });
const bearer = { type: 'bearer', bearer: [{ key: 'token', value: '{{accessToken}}', type: 'string' }] };
add('04 — Authentication', 'Жарамды токенмен профиль алу', 'GET', '/auth/me', 200,
  'Жаңа алынған Bearer токенді тексеру; профильде пароль болмауы тиіс.', [
    check('Профиль логинмен сәйкес', 'pm.expect(data.id).to.eql(Number(pm.collectionVariables.get("userId"))); pm.expect(data.username).to.eql(pm.environment.get("username"));'),
    check('Пароль жауапта жоқ', 'pm.expect(data).not.to.have.property("password");'),
  ], { auth: bearer });
add('04 — Authentication', 'Қорғалған тауарлар тізімі', 'GET', '/auth/products?limit=1', 200,
  'Bearer токенмен қорғалған ресурсты алу.', [
    check('Қорғалған тізім қолжетімді', 'pm.expect(data.products).to.be.an("array").with.lengthOf(1); pm.expect(data.products[0].id).to.be.a("number");'),
  ], { auth: bearer });

const groups = [...new Set(scenarios.map(s => s.group))].map(name => ({
  name, item: scenarios.filter(s => s.group === name).map(s => s.item),
}));
json('Lab9_DummyJSON.postman_collection.json', {
  info: {
    _postman_id: '4191dca5-1ae9-49c5-8531-683ac5e37e09',
    name: 'Lab 9 — REST API Testing — DummyJSON (34 scenarios)',
    description: '9-зертханалық жұмыс. 34 нақты HTTP сценарийі: GET/POST/PUT/PATCH/DELETE, status, JSON Schema, headers, authentication, negative/boundary және response time. Толық коллекцияны ретімен іске қосыңыз. API жазу операцияларын сақтамайды. Документация: https://dummyjson.com/docs/products және https://dummyjson.com/docs/auth. Cookie jar әр сұраныс үшін өшірілген.',
    schema: 'https://schema.getpostman.com/json/collection/v2.1.0/collection.json',
  },
  auth: { type: 'noauth' },
  variable: ['accessToken', 'userId', 'total', 'firstId', 'lastId', 'missingId', 'lastOffset', 'beyondOffset', 'originalTitle', 'originalPrice', 'createdId'].map(key => ({ key, value: '', type: 'string' })),
  event: [
    { listen: 'prerequest', script: { type: 'text/javascript', exec: [
      'if (pm.info.requestName.startsWith("TC01")) {',
      '  ["accessToken", "userId", "total", "firstId", "lastId", "missingId", "lastOffset", "beyondOffset", "originalTitle", "originalPrice", "createdId"].forEach(key => pm.collectionVariables.unset(key));',
      '}',
    ] } },
    { listen: 'test', script: { type: 'text/javascript', exec: [
      check('Header: Content-Type = JSON', String.raw`pm.expect(pm.response.headers.get("Content-Type")).to.match(/^application\/json\b/i);`),
      check('Response Body: жарамды JSON', 'pm.response.json();'),
      check('Response Time < maxResponseTimeMs', 'pm.expect(pm.response.responseTime).to.be.below(Number(pm.environment.get("maxResponseTimeMs")));'),
    ] } },
  ],
  item: groups,
});
json('Lab9_DummyJSON.postman_environment.json', {
  id: '9ae07b39-3acd-4466-b1e1-f250d89fc112',
  name: 'Lab9 — DummyJSON',
  values: [
    { key: 'baseUrl', value: 'https://dummyjson.com', type: 'default', enabled: true },
    { key: 'username', value: 'emilys', type: 'default', enabled: true },
    // Public test credentials from https://dummyjson.com/docs/auth, not a private account.
    { key: 'password', value: 'emilyspass', type: 'secret', enabled: true },
    { key: 'maxResponseTimeMs', value: '5000', type: 'default', enabled: true },
  ],
  _postman_variable_scope: 'environment',
});
json('scenarios.json', scenarios.map(({ item, ...scenario }) => scenario));
const rows = scenarios.map(s => `| ${s.id} | ${s.method} | \`${s.path}\` | ${s.title} | ${s.expected} |`);
writeFileSync(`${directory}SCENARIOS.md`, [
  '# Lab 9 — 34 тестілік сценарий', '',
  'Әр жол — бөлек HTTP сұранысы. Әр сұраныста қосымша Content-Type, JSON және уақыт assertions орындалады.', '',
  '| ID | Method | Endpoint | Тексеру | Күтілетін HTTP |',
  '|---|---|---|---|---:|', ...rows, '',
  'Айнымалылар толық коллекцияны ретімен іске қосқанда автоматты есептеледі. `lastId` — нақты максималды ID; `total` — нақты жазбалар саны.',
  '',
].join('\n'));
console.log(`Generated ${scenarios.length} scenarios in ${directory}`);
