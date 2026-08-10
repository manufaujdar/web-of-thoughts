export type Agent = { id: string; name: string; role: string; accent: string; status?: string };
export type Node = { id: string; type: string; label: string; content: string; status: string; agent_id: string | null };
export type Edge = { source: string; target: string; relation: string };
export type Usage = { calls: number; max_calls: number; input_tokens: number; output_tokens: number };
export type Snapshot = {
  run_id: string; status: string; query: string; model: string; rounds: number;
  agents: Agent[]; nodes: Node[]; edges: Edge[]; usage: Usage;
  final_answer: string | null; termination_reason: string | null; created_at: string;
};
export type Run = {
  id: string; query: string; status: string; model: string; created_at: string; updated_at: string;
  final_answer: string | null; error: string | null; snapshot: Snapshot;
};
export type Config = {
  model: string; reasoning_effort: string; openai_configured: boolean;
  max_agents: number; max_rounds: number; max_calls: number; experimental: boolean;
};
export type RunEvent = {
  sequence: number; run_id: string; type: string; timestamp: string; payload: Record<string, unknown>;
};
