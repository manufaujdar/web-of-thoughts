import { expect, test } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

const snapshot = {
  run_id: 'synthetic', status: 'completed', query: 'Synthetic inquiry', model: 'synthetic-only', rounds: 1,
  agents: [], nodes: [{ id: 'query', type: 'query', label: 'Synthetic inquiry', content: 'Synthetic decision artifact.', status: 'completed', agent_id: null }], edges: [],
  usage: { calls: 0, max_calls: 0, input_tokens: 0, output_tokens: 0 }, final_answer: 'Synthetic final response.', termination_reason: 'completed', created_at: '2026-01-01T00:00:00Z',
};
const run = { id: 'synthetic', query: snapshot.query, status: snapshot.status, model: snapshot.model, created_at: snapshot.created_at, updated_at: snapshot.created_at, final_answer: snapshot.final_answer, error: null, snapshot };

test.beforeEach(async ({ context }) => {
  await context.route('**/*', async route => {
    const url = new URL(route.request().url());
    if (url.hostname !== '127.0.0.1') return route.abort();
    if (!url.pathname.startsWith('/api/')) return route.continue();
    // Every API route is intercepted: no server, provider or private record is used.
    if (url.pathname.endsWith('/events')) return route.fulfill({ contentType: 'text/event-stream', body: '' });
    const data = url.pathname.endsWith('/config') ? { model: 'synthetic-only', openai_configured: false, max_calls: 0, max_agents: 0, max_rounds: 1, experimental: true }
      : url.pathname.endsWith('/agents') ? [] : url.pathname === '/api/v1/runs' ? [run] : run;
    return route.fulfill({ json: data });
  });
});

async function chooseLarger(page: import('@playwright/test').Page) {
  const summary = page.getByText('Reading preferences', { exact: true });
  await summary.focus();
  await page.keyboard.press('Enter');
  await page.getByLabel('Artifact text size').selectOption('16');
}

test('actual inquiry/workspace reader preserves browser choice and has accessible controls', async ({ page }) => {
  await page.goto('/');
  await chooseLarger(page);
  const scan = await new AxeBuilder({ page }).include('.reader-preferences').withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze();
  expect(scan.violations).toEqual([]);
  await page.getByRole('button', { name: /Synthetic inquiry/ }).click();
  await page.locator('.graph-node').click();
  await expect(page.locator('.artifact')).toHaveCSS('font-size', '16px');
  // Existing design renders final synthesis two pixels larger than artifacts.
  await expect(page.locator('.final-copy')).toHaveCSS('font-size', '18px');
  await page.reload();
  await page.getByText('Reading preferences', { exact: true }).click();
  await expect(page.getByLabel('Artifact text size')).toHaveValue('16');
});

test('quota failure with readable stale storage preserves choice across actual screen remounts', async ({ page }) => {
  await page.addInitScript(() => {
    localStorage.setItem('wot-reader-text-size', '13');
    Storage.prototype.setItem = () => { throw new DOMException('Synthetic quota failure', 'QuotaExceededError'); };
  });
  await page.goto('/');
  await chooseLarger(page);
  await expect(page.locator('.reader-options [role="status"]')).toContainText('Kept for this session');
  await page.getByRole('button', { name: /Synthetic inquiry/ }).click();
  await page.getByText('Reading preferences', { exact: true }).click();
  await expect(page.getByLabel('Artifact text size')).toHaveValue('16');
  await expect(page.locator('.final-copy')).toHaveCSS('font-size', '18px');
});
