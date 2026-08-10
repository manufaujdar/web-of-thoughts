import type { Agent, Config, Run } from "./types";

async function json<T>(url: string, init?: RequestInit): Promise<T> {
  const response = await fetch(url, init);
  const body = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(body.detail || `Request failed (${response.status})`);
  return body as T;
}

export const api = {
  config: () => json<Config>("/api/v1/config"),
  agents: () => json<Agent[]>("/api/v1/agents"),
  runs: () => json<Run[]>("/api/v1/runs"),
  run: (id: string) => json<Run>(`/api/v1/runs/${id}`),
  create: (query: string, agent_ids: string[], rounds: number, max_calls: number) =>
    json<{ run_id: string }>("/api/v1/runs", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, agent_ids, rounds, max_calls, max_wall_seconds: 240 })
    }),
  cancel: (id: string) => json(`/api/v1/runs/${id}/cancel`, { method: "POST" })
};
