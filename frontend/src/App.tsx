import { FormEvent, useEffect, useMemo, useRef, useState } from "react";
import { api } from "./api";
import type { Agent, Config, Node, Run, RunEvent, Snapshot } from "./types";

const TERMINAL = new Set(["completed", "partial", "failed", "cancelled"]);

function Mark({ children }: { children: string }) {
  return <span className={`status status-${children}`}>{children.replaceAll("_", " ")}</span>;
}

function Composer({ agents, config, onCreate, busy }: { agents: Agent[]; config: Config | null; onCreate: (q: string, ids: string[], rounds: number) => void; busy: boolean }) {
  const [query, setQuery] = useState("");
  const [selected, setSelected] = useState<string[]>(agents.map(a => a.id));
  const [rounds, setRounds] = useState(2);
  useEffect(() => { setSelected(agents.map(a => a.id)); }, [agents]);
  const requiredCalls = selected.length * rounds + 1;
  function submit(event: FormEvent) { event.preventDefault(); if (query.trim() && selected.length >= 2) onCreate(query.trim(), selected, rounds); }
  return <form className="composer" onSubmit={submit}>
    <div className="eyebrow">New inquiry</div>
    <h1>Think in a web,<br /><em>not a line.</em></h1>
    <p className="lede">Independent specialists explore the question, review neighboring perspectives, and hand a connected evidence web to a master evaluator.</p>
    {!config?.openai_configured && <div className="notice warning" role="alert"><strong>API key required.</strong> Set <code>OPENAI_API_KEY</code> on the server to enable live model calls.</div>}
    <label htmlFor="query">What should the agents examine?</label>
    <textarea id="query" value={query} onChange={e => setQuery(e.target.value)} placeholder="Ask a complex question, compare approaches, test a plan, or explore a decision…" rows={6} maxLength={12000} required />
    <div className="form-row">
      <label>Collaboration depth<select value={rounds} onChange={e => setRounds(Number(e.target.value))}><option value={1}>One pass · independent</option><option value={2}>Two passes · peer review</option></select></label>
      <div><span className="field-label">Live call budget</span><div className="budget-preview"><strong>{requiredCalls}</strong><span>model calls</span></div></div>
    </div>
    <fieldset><legend>Specialist team <span>{selected.length} selected</span></legend><div className="role-grid">
      {agents.map(agent => <label className={`role-check ${selected.includes(agent.id) ? "selected" : ""}`} key={agent.id} style={{"--accent": agent.accent} as React.CSSProperties}>
        <input type="checkbox" checked={selected.includes(agent.id)} onChange={() => setSelected(s => s.includes(agent.id) ? s.filter(id => id !== agent.id) : [...s, agent.id])} />
        <span className="role-dot" /><span><strong>{agent.name}</strong><small>{agent.role}</small></span>
      </label>)}
    </div></fieldset>
    <p className="fineprint" role="status">{selected.length < 2 ? "Select at least two specialists." : requiredCalls > (config?.max_calls || 20) ? "Reduce the team or collaboration depth to fit the call budget." : ""}</p>
    <button className="primary" disabled={busy || !config?.openai_configured || query.trim().length < 3 || selected.length < 2 || requiredCalls > (config?.max_calls || 20)}>{busy ? "Starting…" : "Build the thought web"}<span aria-hidden="true">→</span></button>
    <p className="fineprint">Outputs are experimental and may be wrong. Concise decision artifacts are shown—not private hidden reasoning.</p>
  </form>;
}

function Graph({ snapshot, selected, onSelect }: { snapshot: Snapshot; selected: string | null; onSelect: (id: string) => void }) {
  const nodes = snapshot.nodes;
  const positions = useMemo(() => {
    const map: Record<string, {x:number;y:number}> = { query: {x: 50, y: 10}, master: {x: 50, y: 90} };
    const middle = nodes.filter(n => n.id !== "query" && n.id !== "master");
    middle.forEach((node, i) => { const row = node.id.endsWith("r2") ? 62 : 34; const same = middle.filter(n => n.id.endsWith(node.id.slice(-2))); const idx = same.findIndex(n => n.id === node.id); map[node.id] = { x: 8 + (84 * (idx + .5) / Math.max(same.length, 1)), y: row }; });
    return map;
  }, [nodes]);
  return <div className="graph-wrap">
    <div className="panel-heading"><div><span className="eyebrow">Live topology</span><h2>Thought web</h2></div><span>{nodes.length} nodes · {snapshot.edges.length} links</span></div>
    <div className="graph" role="region" aria-label={`Thought web with ${nodes.length} nodes and ${snapshot.edges.length} typed links`}>
      <svg aria-hidden="true" viewBox="0 0 100 100" preserveAspectRatio="none">{snapshot.edges.map((edge, i) => { const a=positions[edge.source], b=positions[edge.target]; return a&&b ? <g key={i}><line x1={a.x} y1={a.y} x2={b.x} y2={b.y} className={`edge edge-${edge.relation}`} vectorEffect="non-scaling-stroke" /></g> : null; })}</svg>
      {nodes.map(node => { const p=positions[node.id] || {x:50,y:50}; return <button key={node.id} onClick={() => onSelect(node.id)} className={`graph-node type-${node.type} ${selected===node.id?"active":""}`} style={{left:`${p.x}%`,top:`${p.y}%`}}><span>{node.type}</span><strong>{node.label}</strong></button>; })}
    </div>
    <details className="accessible-list"><summary>Text view of nodes and relationships</summary><ul>{nodes.map(n => <li key={n.id}><button onClick={() => onSelect(n.id)}>{n.label}</button> — {n.type}, {n.status}</li>)}</ul><ul>{snapshot.edges.map((e,i)=><li key={i}>{e.source} <strong>{e.relation}</strong> {e.target}</li>)}</ul></details>
  </div>;
}

function RunWorkspace({ runId, agents, onExit }: { runId: string; agents: Agent[]; onExit: () => void }) {
  const [error, setError] = useState("");
  const [run, setRun] = useState<Run | null>(null), [events, setEvents] = useState<RunEvent[]>([]), [streams, setStreams] = useState<Record<string,string>>({}), [finalStream, setFinalStream] = useState(""), [selected, setSelected] = useState<string|null>(null), [connection, setConnection] = useState("connecting");
  const source = useRef<EventSource|null>(null);
  async function refresh() { try { setRun(await api.run(runId)); setError(""); } catch (e) { setError(e instanceof Error ? e.message : "Could not load this run"); } }
  useEffect(() => {
    refresh(); const es = new EventSource(`/api/v1/runs/${runId}/events`); source.current=es;
    es.onopen=()=>setConnection("live"); es.onerror=()=>setConnection("reconnecting");
    const types=["run.created","run.started","phase.changed","agent.started","agent.delta","agent.completed","agent.failed","node.created","budget.updated","master.started","final.delta","run.completed","run.partial","run.failed","run.cancelled"];
    types.forEach(type=>es.addEventListener(type,(raw)=>{ const event=JSON.parse((raw as MessageEvent).data) as RunEvent; setEvents(v=>[...v.slice(-119),event]); if(type==="agent.delta"){const p=event.payload as {agent_id:string;delta:string};setStreams(v=>({...v,[p.agent_id]:(v[p.agent_id]||"")+p.delta}));} if(type==="final.delta"){const p=event.payload as {delta:string};setFinalStream(v=>v+p.delta);} if(type==="run.completed"||type==="run.partial"||type==="run.failed"||type==="run.cancelled"){es.close();setConnection("closed");} if(type!=="agent.delta"&&type!=="final.delta") refresh(); }));
    return ()=>es.close();
  },[runId]);
  if(!run) return <main className="loading"><div role="status">{error || "Connecting to the thought web…"}</div>{error && <div><button className="quiet" onClick={refresh}>Retry</button><button className="quiet" onClick={onExit}>Back to inquiries</button></div>}</main>;
  const snapshot=run.snapshot, node=snapshot.nodes.find(n=>n.id===selected);
  return <main className="workspace">
    <header className="topbar"><button className="brand" onClick={onExit}><span className="brand-mark">W</span><span>Web of Thoughts<small>Research workbench</small></span></button><div className="run-meta"><Mark>{snapshot.status}</Mark><span className={`connection ${connection}`}>{connection}</span><span>{snapshot.model}</span>{!TERMINAL.has(snapshot.status)&&<button className="quiet danger" onClick={()=>api.cancel(runId).catch(e=>setError(e.message))}>Cancel run</button>}</div></header>
    {error && <div className="global-error" role="alert">{error}</div>}
    <section className="query-strip"><span className="eyebrow">Inquiry</span><p>{snapshot.query}</p><div className="usage"><span><strong>{snapshot.usage.calls}</strong> / {snapshot.usage.max_calls} calls</span><span><strong>{snapshot.usage.input_tokens + snapshot.usage.output_tokens}</strong> tokens</span></div></section>
    <div className="workspace-grid"><section className="agent-column"><div className="panel-heading"><div><span className="eyebrow">Council</span><h2>Specialists</h2></div></div>{snapshot.agents.map(agent=><button key={agent.id} className={`agent-card ${selected?.startsWith(agent.id)?"active":""}`} onClick={()=>{const related=[...snapshot.nodes].reverse().find(n=>n.agent_id===agent.id);if(related)setSelected(related.id)}} style={{"--accent":agent.accent} as React.CSSProperties}><span className="role-dot"/><span><strong>{agent.name}</strong><small>{streams[agent.id]?.slice(-100)||agent.role}</small></span><Mark>{agent.status||"queued"}</Mark></button>)}<div className="activity"><h3>Activity</h3><div aria-live="polite">{events.slice(-8).reverse().map(e=><p key={e.sequence}><time>{new Date(e.timestamp).toLocaleTimeString([], {hour:"2-digit",minute:"2-digit"})}</time>{e.type.replaceAll("."," · ")}</p>)}</div></div></section>
      <Graph snapshot={snapshot} selected={selected} onSelect={setSelected}/>
      <aside className="inspector"><div className="panel-heading"><div><span className="eyebrow">Inspector</span><h2>{node?.label||"Select a node"}</h2></div></div>{node?<><div className="node-meta"><Mark>{node.status}</Mark><span>{node.type}</span></div><div className="artifact">{node.content}</div></>:<p className="empty">Choose any thought node or specialist to inspect its public decision artifact and provenance.</p>}</aside>
    </div>
    {(snapshot.final_answer||finalStream)&&<section className="final"><div><span className="eyebrow">Master evaluation</span><h2>{snapshot.final_answer?"Final response":"Synthesizing…"}</h2><p className="termination">{snapshot.termination_reason?`Stopped: ${snapshot.termination_reason.replaceAll("_"," ")}`:"Evaluating the complete web"}</p></div><div className="final-copy">{snapshot.final_answer||finalStream}</div><button className="quiet" disabled={!snapshot.final_answer} onClick={()=>navigator.clipboard.writeText(snapshot.final_answer||"").catch(()=>setError("Clipboard unavailable. Select and copy the response text."))}>Copy response</button></section>}
  </main>;
}

function History({ runs, onOpen }: { runs: Run[]; onOpen:(id:string)=>void }) { return <section className="history"><div className="section-title"><div><span className="eyebrow">Local record</span><h2>Recent inquiries</h2></div></div>{runs.length?<div className="history-list">{runs.map(run=><button key={run.id} onClick={()=>onOpen(run.id)}><Mark>{run.status}</Mark><span><strong>{run.query}</strong><small>{new Date(run.created_at).toLocaleString()} · {run.model}</small></span><span aria-hidden="true">→</span></button>)}</div>:<p className="empty">Completed and active runs will appear here.</p>}</section> }

export default function App(){ const[config,setConfig]=useState<Config|null>(null),[agents,setAgents]=useState<Agent[]>([]),[runs,setRuns]=useState<Run[]>([]),[active,setActive]=useState<string|null>(()=>location.hash.slice(1)||null),[busy,setBusy]=useState(false),[error,setError]=useState("");
  useEffect(()=>{const onHash=()=>setActive(location.hash.slice(1)||null);window.addEventListener("hashchange",onHash);return()=>window.removeEventListener("hashchange",onHash)},[]);
  useEffect(()=>{Promise.all([api.config(),api.agents(),api.runs()]).then(([c,a,r])=>{setConfig(c);setAgents(a);setRuns(r)}).catch(e=>setError(e.message))},[]);
  function open(id:string|null){setActive(id);location.hash=id||"";if(!id)api.runs().then(setRuns).catch(e=>setError(e.message))}
  async function create(q:string,ids:string[],rounds:number){try{setBusy(true);setError("");const result=await api.create(q,ids,rounds,ids.length*rounds+1);open(result.run_id)}catch(e){setError(e instanceof Error?e.message:"Could not start run")}finally{setBusy(false)}}
  if(active)return <RunWorkspace runId={active} agents={agents} onExit={()=>open(null)}/>;
  return <main><header className="home-nav"><div className="brand"><span className="brand-mark">W</span><span>Web of Thoughts<small>Experimental multi-agent reasoning</small></span></div><span className="local-pill">● Local persistence</span></header>{error&&<div className="global-error" role="alert">{error}</div>}<div className="home-grid"><Composer agents={agents} config={config} onCreate={create} busy={busy}/><div className="principle"><blockquote>“A useful web does not think more. It makes disagreement, evidence, and synthesis visible.”</blockquote><dl><div><dt>01</dt><dd><strong>Diverge</strong><span>Distinct roles generate functional alternatives.</span></dd></div><div><dt>02</dt><dd><strong>Connect</strong><span>Peer review exposes support and contradiction.</span></dd></div><div><dt>03</dt><dd><strong>Synthesize</strong><span>The master evaluates the full topology.</span></dd></div></dl></div></div><History runs={runs} onOpen={id=>open(id)}/><footer><span>Apache-2.0 · Research only</span><span>Prompts leave this device when sent to OpenAI.</span></footer></main> }
