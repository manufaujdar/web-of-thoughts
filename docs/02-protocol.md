# WoT protocol

## Inputs

- the task and available context;
- success criteria and hard constraints;
- available tools or verifiers;
- budget vector;
- risk level;
- desired output contract.

## Phase 0: gate

Estimate whether structured search is useful. If the task is simple, low-ambiguity, or cheaply verifiable through a direct method, use that method and record `wot_gate: bypassed`.

## Phase 1: frame

Create a root problem node, a constraint ledger, an unknowns ledger, and a success test. Select two to five dimensions that are likely to expose materially different solutions or risks. Avoid generic dimensions with no decision relevance.

Output: `problem frame`, `dimensions`, `acceptance criteria`, `budget allocation`.

## Phase 2: seed

Generate a small portfolio of candidates. Each seed should state its core mechanism, assumptions, expected advantage, likely failure mode, and a discriminating test. Reject semantic duplicates.

Default hypothesis: three to five strong seeds outperform a large undifferentiated batch for efficiency. This must be tested by task family.

## Phase 3: construct

Decompose only where it unlocks independent work or verification. Link candidates to shared constraints, evidence, and subproblems. Add cross-path edges only when the relation is useful.

The web should remain sparse. Edge creation is an operation with cost, not mandatory bookkeeping between every pair.

## Phase 4: schedule

Build the frontier from applicable operators. Choose the operation with the greatest estimated value per cost while retaining a final verification reserve.

Typical priorities:

1. test fatal assumptions in the current leader;
2. resolve contradictions affecting the final decision;
3. run discriminating tests between close candidates;
4. fill missing hard constraints;
5. synthesize complementary strengths;
6. explore a new dimension only if coverage has a meaningful gap.

## Phase 5: challenge and verify

Use the cheapest reliable verifier available: deterministic code, formal constraint check, authoritative retrieval, calculation, simulation, or independent evaluation prompt. Record verifier type and result.

Do not let one evaluator both invent and certify a claim without marking the dependence. For high-risk results, use heterogeneous verification.

## Phase 6: synthesize

Create a synthesis node only when it improves the candidate. It must list:

- source nodes;
- compatible components retained;
- conflicts and their resolution;
- constraints newly satisfied or violated;
- remaining assumptions;
- expected improvement over the strongest parent.

If combination introduces incoherence, retain separate candidates.

## Phase 7: prune and compress

Reject invalid candidates, merge duplicates, deactivate dominated paths, and compress stable regions into summaries with provenance. Never delete evidence needed to audit the final selection.

## Phase 8: select and stop

Rank viable candidates using predeclared criteria. Apply the stopping rules in the formal model. Produce an answer that contains the solution, decisive rationale, key evidence, important assumptions, unresolved uncertainty, and—when useful—alternatives considered.

## Pseudocode

```text
W = FRAME(task, constraints, budget)
if not needs_web(W): return DIRECT_SOLVE(W)

W = SEED(W, dimensions=select_dimensions(W))
reserve verification budget

while budget remains above reserve:
    F = enumerate_applicable_operations(W)
    score each operation by expected gain per cost
    if stop_condition(W, F): break
    o = select(F)
    W = apply(o, W)
    W = update_ledgers_scores_and_costs(W)
    W = prune_or_compress_if_needed(W)

W = FINAL_VERIFY(W, reserve)
return SELECT_AND_RENDER(W)
```

## Output levels

- `answer_only`: final answer plus uncertainty labels;
- `decision_record`: answer, criteria, alternatives, decisive evidence, and caveats;
- `research_trace`: structured nodes, edges, scores, costs, verifier results, and controller actions.

The research trace should contain concise artifacts and decisions, not require disclosure of private hidden chain-of-thought.

