import { useEffect, useState } from 'react';

export function readTextSize(): number {
  try { return localStorage.getItem('wot-reader-text-size') === '16' ? 16 : 13; }
  catch { return 13; }
}

export default function ReaderPreferences() {
  const [size, setSize] = useState(readTextSize);
  const [saved, setSaved] = useState(true);
  useEffect(() => {
    document.documentElement.style.setProperty('--artifact-text-size', `${size}px`);
    try { localStorage.setItem('wot-reader-text-size', String(size)); setSaved(true); }
    catch { setSaved(false); }
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
