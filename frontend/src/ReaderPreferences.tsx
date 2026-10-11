import { useEffect, useState } from 'react';

let sessionTextSize = 13;
let hasUnsavedSessionChoice = false;

export function readTextSize(): number {
  if (hasUnsavedSessionChoice) return sessionTextSize;
  try { sessionTextSize = localStorage.getItem('wot-reader-text-size') === '16' ? 16 : 13; }
  catch { /* Retain the choice when moving between screens with storage blocked. */ }
  return sessionTextSize;
}

export function saveTextSize(size: number): boolean {
  sessionTextSize = size === 16 ? 16 : 13;
  try {
    localStorage.setItem('wot-reader-text-size', String(sessionTextSize));
    hasUnsavedSessionChoice = false;
    return true;
  } catch {
    hasUnsavedSessionChoice = true;
    return false;
  }
}

export default function ReaderPreferences() {
  const [size, setSize] = useState(readTextSize);
  const [saved, setSaved] = useState(true);
  useEffect(() => {
    document.documentElement.style.setProperty('--artifact-text-size', `${size}px`);
    setSaved(saveTextSize(size));
  }, [size]);
  return <details className="reader-preferences">
    <summary>Reading preferences</summary>
    <div className="reader-options">
      <label>Artifact text size<select value={size} onChange={event => setSize(Number(event.target.value))}>
        <option value={13}>Standard</option><option value={16}>Larger</option>
      </select></label>
      <p role="status">{saved ? 'Saved in this browser. Applies to artifacts and final responses.' : 'Storage unavailable. Kept for this session.'}</p>
    </div>
  </details>;
}
