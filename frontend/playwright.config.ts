import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: Boolean(process.env.CI),
  retries: 0,
  reporter: 'list',
  use: { baseURL: 'http://127.0.0.1:43572', trace: 'retain-on-failure' },
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'], viewport: { width: 390, height: 844 }, reducedMotion: 'reduce' } }],
  webServer: {
    command: 'npm run preview -- --host 127.0.0.1 --port 43572 --strictPort',
    url: 'http://127.0.0.1:43572',
    reuseExistingServer: false,
  },
});
