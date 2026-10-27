import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import newman from 'newman';

const directory = fileURLToPath(new URL('.', import.meta.url));
const load = name => JSON.parse(readFileSync(`${directory}${name}`, 'utf8'));
const collection = load('Lab9_DummyJSON.postman_collection.json');
const environment = load('Lab9_DummyJSON.postman_environment.json');
const scenarios = load('scenarios.json');
const startedAt = new Date().toISOString();
const baseUrl = environment.values.find(v => v.key === 'baseUrl').value;
const maxResponseTimeMs = Number(environment.values.find(v => v.key === 'maxResponseTimeMs').value);
const resultDirectory = `${directory}results/`;
mkdirSync(resultDirectory, { recursive: true });

// Tokens, cookies, and passwords never go into the saved report.
function redact(value) {
  if (Array.isArray(value)) return value.map(redact);
  if (value && typeof value === 'object') {
    return Object.fromEntries(Object.entries(value).map(([key, child]) => [
      key, /token|password|cookie|authorization/i.test(key) ? '[REDACTED]' : redact(child),
    ]));
  }
  return value;
}

newman.run({
  collection,
  environment,
  iterationCount: 1,
  delayRequest: 300,
  timeoutRequest: 15000,
  reporters: ['cli'],
  reporter: { cli: { noAssertions: true, noBanner: true } },
}, (error, summary) => {
  if (!summary) {
    console.error(error?.message ?? 'Newman summary is missing');
    process.exitCode = 1;
    return;
  }
  const executions = summary.run.executions.map(execution => {
    const scenario = scenarios.find(s => execution.item.name.startsWith(`${s.id} `));
    const response = execution.response;
    let body = null;
    if (response) {
      const raw = response.stream.toString('utf8');
      try { body = redact(JSON.parse(raw)); }
      catch { body = raw; }
    }
    const assertions = (execution.assertions ?? []).map(a => ({
      name: a.assertion,
      passed: !a.error && !a.skipped,
      skipped: Boolean(a.skipped),
      error: a.error?.message ?? null,
    }));
    const scriptErrors = summary.run.failures
      .filter(f => f.source?.id === execution.item.id && f.error?.name !== 'AssertionError')
      .map(f => f.error?.message ?? String(f.error));
    const headers = {};
    response?.headers.each(header => {
      if (['content-type', 'date', 'etag', 'x-ratelimit-limit', 'x-ratelimit-remaining'].includes(header.key.toLowerCase())) {
        headers[header.key.toLowerCase()] = header.value;
      }
    });
    return {
      id: scenario?.id,
      title: execution.item.name,
      method: execution.request.method,
      url: execution.request.url.toString(),
      expectedStatus: scenario?.expected,
      actualStatus: response?.code ?? null,
      responseTimeMs: response?.responseTime ?? null,
      responseSizeBytes: response?.responseSize ?? null,
      headers,
      assertions,
      scriptErrors,
      requestError: execution.requestError?.message ?? null,
      passed: Boolean(response) && response.code === scenario?.expected &&
        !execution.requestError && scriptErrors.length === 0 &&
        assertions.length >= 5 && assertions.every(a => a.passed),
      body,
    };
  });
  const times = executions.map(e => e.responseTimeMs).filter(t => typeof t === 'number').sort((a, b) => a - b);
  const mean = times.length ? times.reduce((a, b) => a + b, 0) / times.length : null;
  const failures = summary.run.failures.map(f => ({
    source: f.source?.name ?? null,
    test: f.error?.test ?? f.at ?? null,
    message: f.error?.message ?? String(f.error),
  }));
  const passed = !error && failures.length === 0 && executions.length === scenarios.length &&
    executions.every(e => e.passed);
  const report = {
    lab: 9,
    api: 'DummyJSON',
    documentation: ['https://dummyjson.com/docs', 'https://dummyjson.com/docs/products', 'https://dummyjson.com/docs/auth'],
    runner: `Newman ${newman.version ?? '6.2.1'}`,
    collection: collection.info.name,
    baseUrl,
    startedAt,
    completedAt: new Date().toISOString(),
    iterations: 1,
    requestDelayMs: 300,
    maxResponseTimeMs,
    passed,
    scenarios: { planned: scenarios.length, executed: executions.length, passed: executions.filter(e => e.passed).length, failed: executions.filter(e => !e.passed).length },
    assertions: summary.run.stats.assertions,
    timings: {
      minMs: times[0] ?? null,
      averageMs: mean === null ? null : Number(mean.toFixed(2)),
      p95Ms: times.length ? times[Math.ceil(times.length * 0.95) - 1] : null,
      maxMs: times.at(-1) ?? null,
      note: 'Бір итерация, клиент жағындағы HTTPS уақыты; жүктемелік тест немесе SLA дәлелі емес.',
    },
    error: error?.message ?? null,
    failures,
    executions,
  };
  writeFileSync(`${resultDirectory}newman-results.json`, `${JSON.stringify(report, null, 2)}\n`);
  const lines = [
    '# Lab 9 — нақты Newman нәтижесі', '',
    `- API: ${baseUrl}`,
    `- Runner: ${report.runner}; iterations: 1; request delay: 300 ms.`,
    `- Басталуы (UTC): ${report.startedAt}; аяқталуы (UTC): ${report.completedAt}.`,
    `- Нәтиже: **${passed ? 'PASS' : 'FAIL'}**.`,
    `- Сценарийлер: **${report.scenarios.passed}/${scenarios.length} PASS**, орындалғаны ${executions.length}, FAIL: ${report.scenarios.failed}.`,
    `- Assertions: ${report.assertions.total}; failed: ${report.assertions.failed}; pending: ${report.assertions.pending}.`,
    `- Уақыт (ms): min ${report.timings.minMs}; average ${report.timings.averageMs}; p95 ${report.timings.p95Ms}; max ${report.timings.maxMs}.`,
    `- Әр жауап үшін шек: < ${maxResponseTimeMs} ms.`, '',
    '| ID | Сценарий | Method | Күтілетін код | Нақты код | Уақыт, ms | Assertions өтті/барлығы | Нәтиже |',
    '|---|---|---|---:|---:|---:|---:|---|',
    ...executions.map(e => `| ${e.id} | ${e.title.replace(/^TC\d+ — /, '')} | ${e.method} | ${e.expectedStatus} | ${e.actualStatus ?? '—'} | ${e.responseTimeMs ?? '—'} | ${e.assertions.filter(a => a.passed).length}/${e.assertions.length} | ${e.passed ? 'PASS' : 'FAIL'} |`),
    '', '## Қателер', '',
    ...(failures.length ? failures.map(f => `- ${f.source}: ${f.test}: ${f.message}`) : ['Assertion немесе transport қатесі тіркелмеді.']),
    ...(error ? [`- Runner: ${error.message}`] : []),
    '', '## Нәтижені түсіндіру', '',
    '400/401/404 күтілетін теріс сценарийлерде PASS — дұрыс нәтиже. API жазу операцияларын имитациялайды; деректердің сақталмауы TC17/TC20/TC22 арқылы тексерілген.', '',
    'Бұл нақты Newman іске қосылуы. Postman GUI Collection Runner осы ортада орындалмады; GUI арқылы қайталау қадамдары [README.md](../README.md) ішінде. Бір итерация өнімділік немесе қолжетімділік SLA-ын дәлелдемейді.', '',
    'Әр assertion, response body және таңдалған response headers [newman-results.json](newman-results.json) ішінде. Токендер мен құпиясөздер жасырылған.', '',
  ];
  writeFileSync(`${resultDirectory}RUN_RESULTS.md`, lines.join('\n'));
  console.log(`\nLab 9: ${report.scenarios.passed}/${scenarios.length} scenarios; ${passed ? 'PASS' : 'FAIL'}.`);
  console.log(`Saved: ${resultDirectory}RUN_RESULTS.md`);
  console.log(`Saved: ${resultDirectory}newman-results.json`);
  process.exitCode = passed ? 0 : 1;
});
