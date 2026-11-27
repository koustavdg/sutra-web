const { test } = require('node:test');
const assert = require('node:assert/strict');
const { median, summarize, sample, markdown, meetsBudget } = require('../scripts/performance-loop.cjs');

test('medians are numeric and independent, not averages or best runs', () => {
  assert.equal(median([99, 75, 76]), 76);
  assert.equal(median([1, 9, 3, 5]), 4);
  const row = { performance: 75, accessibility: 100, seo: 100, fcp_ms: 900, lcp_ms: 1000, tbt_ms: 0, cls: 0, bytes: 2000 };
  assert.equal(summarize([row, {...row, performance: 99}, {...row, performance: 76}]).performance, 76);
});
test('runtime errors and missing metrics never become zero or passing scores', () => {
  assert.throws(() => sample({runtimeError: {message: 'navigation failed'}}), /navigation failed/);
  assert.throws(() => sample({categories: {}}), /Missing score/);
});
test('existing guide budgets stay enforced while new home/hub baselines are reporting-only', () => {
  const median = {performance: 84, accessibility: 100, seo: 100};
  assert.equal(meetsBudget({path: '/kavita-reader.html', median}), false);
  assert.equal(meetsBudget({path: '/', median}), true);
  assert.equal(meetsBudget({path: '/', median: {...median, seo: 94}}), false);
});
test('comparison rejects incompatible runs and reports observed deltas', () => {
  const a = { label: 'before', runs: 3, machine: {cpu: 'same'}, lighthouseVersion: '13.5.0', browserVersion: 'same',
    pages: [{path: '/', median: {performance: 75, accessibility: 100, seo: 100, lcp_ms: 4000, tbt_ms: 0, cls: 0, bytes: 102400}}] };
  const b = {...a, label: 'after', pages: [{path: '/', median: {...a.pages[0].median, performance: 95, lcp_ms: 2000}}]};
  assert.match(markdown(b, a), /20 \| -2.00/);
  assert.throws(() => markdown({...b, runs: 1}, a), /Incompatible/);
  assert.throws(() => markdown({...b, pages: []}, a), /pages differ/);
});
