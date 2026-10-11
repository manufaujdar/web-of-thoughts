import { afterEach, expect, it, vi } from 'vitest';
import { readTextSize } from './ReaderPreferences';
afterEach(() => vi.unstubAllGlobals());
it('accepts the offered larger size and rejects malformed storage', () => {
  for (const [saved, expected] of [['16', 16], ['13', 13], ['1000', 13], ['NaN', 13], [null, 13]]) {
    vi.stubGlobal('localStorage', { getItem: () => saved });
    expect(readTextSize()).toBe(expected);
  }
});
it('keeps a readable default when storage is blocked', () => {
  vi.stubGlobal('localStorage', { getItem: () => { throw new Error('blocked'); } });
  expect(readTextSize()).toBe(13);
});
