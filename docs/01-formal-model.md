# Formal model

## Web state

At iteration `t`, define the web as:

`W_t = (V_t, E_t, D_t, F_t, L_t, B_t)`

where:

- `V` is the set of thought nodes;
- `E` is the set of typed directed edges;
- `D` is the active set of task dimensions;
- `F` is the frontier of eligible operations;
- `L` is the ledger of constraints, assumptions, contradictions, and open questions;
- `B` is the remaining budget vector.

The budget vector may include model calls, input tokens, output tokens, wall time, tool calls, and monetary cost.

## Node contract

Each node should be compact and independently interpretable:

```yaml
id: n17
type: hypothesis
dimension: causal
content: "..."
status: candidate
parents: [n4, n9]
assumptions: [a2]
evidence: [e5]
scores:
  relevance: 0.0
  plausibility: 0.0
  novelty: 0.0
  information_value: 0.0
  risk: 0.0
  confidence: 0.0
cost:
  output_tokens: 0
```

Recommended node types: `problem`, `constraint`, `subproblem`, `observation`, `hypothesis`, `candidate`, `evidence`, `critique`, `counterexample`, `test`, `decision`, and `synthesis`.

Recommended statuses: `candidate`, `active`, `verified`, `weakened`, `rejected`, `merged`, and `selected`.

## Edge contract

Use a small controlled vocabulary:

- `decomposes`: source breaks into target;
- `depends_on`: source requires target;
- `supports`: source raises credibility of target;
- `contradicts`: source and target cannot both hold under stated conditions;
- `refines`: target makes source more precise;
- `tests`: source can verify or falsify target;
- `analogous_to`: structural similarity useful for transfer;
- `alternative_to`: competing candidate;
- `synthesizes`: target combines sources;
- `derived_from`: provenance relation.

An edge should include a short justification and, when meaningful, a strength and evidence reference.

## Operators

Let `o` be a candidate operation. Initial operators are:

- `FRAME`: extract objective, constraints, success test, unknowns, and relevant dimensions;
- `DECOMPOSE`: create subproblems and dependencies;
- `DIVERGE`: generate non-redundant candidates from selected dimensions;
- `LINK`: add a semantically justified cross-path edge;
- `CHALLENGE`: search for a counterexample, violated constraint, or hidden assumption;
- `VERIFY`: use evidence, calculation, execution, retrieval, or a task-specific checker;
- `REFINE`: repair or specialize a promising node;
- `MERGE`: deduplicate equivalent nodes;
- `SYNTHESIZE`: combine compatible nodes into a stronger candidate;
- `PRUNE`: deactivate dominated, invalid, or low-value regions;
- `SELECT`: choose the best supported solution;
- `STOP`: terminate with answer and uncertainty report.

## Scheduling heuristic

For each frontier operation, estimate:

`priority(o) = [gain(o) × impact(o) × uncertainty(o) × diversity(o)] / [cost(o) × risk(o)]`

All terms are normalized heuristics, not calibrated probabilities. A practical score can use weighted sums with epsilon denominators. The important experimental requirement is to log the version and weights.

Possible components of `gain`:

- expected reduction in critical uncertainty;
- expected improvement in constraint satisfaction;
- new dimensional coverage;
- ability to discriminate between leading candidates;
- ability to unlock a blocked dependency.

Penalize:

- semantic redundancy;
- unsupported graph density;
- repeated evaluation by the same method;
- paths whose best-case value cannot beat the incumbent;
- operations likely to exhaust the reserve needed for final verification.

## Candidate utility

An initial decision utility is:

`U(v) = w_q Q + w_e E + w_c C + w_r R + w_d D - w_k K - w_u U_n`

where `Q` is task quality, `E` evidence support, `C` constraint coverage, `R` robustness, `D` useful diversity contributed, `K` cost, and `U_n` unresolved critical uncertainty. Scores and weights must be task-specific and recorded before evaluating final outputs when feasible.

## Invariants

1. Every active node is connected to the problem or a required subproblem.
2. Every synthesis records its source nodes.
3. Rejected nodes retain a concise rejection reason.
4. Critical factual claims have evidence or are labeled assumptions.
5. Contradictions are resolved, scoped, or listed as unresolved before selection.
6. A reserved budget remains for final verification and answer construction.
7. No node is considered independently confirmed by a paraphrase of its own ancestry.

## Stopping conditions

Stop when all mandatory constraints are satisfied and any one condition holds:

- verifier-backed acceptance threshold is reached;
- the top candidate remains stable across the last `k` meaningful operations;
- no frontier operation has positive expected net value;
- the remaining budget equals the verification reserve;
- all viable alternatives are dominated or rejected;
- the hard budget is reached.

Return `budget_exhausted` rather than pretending convergence when the hard limit caused termination.

