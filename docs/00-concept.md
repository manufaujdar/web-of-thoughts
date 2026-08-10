# Concept and scope

## Working definition

A **Web of Thoughts** is a dynamically constructed, typed graph of compact reasoning artifacts, governed by an adaptive controller and a finite resource budget.

Each node contains a useful artifact—such as a hypothesis, subproblem, constraint, observation, candidate action, critique, evidence item, or synthesis. Each edge states why two nodes are related. The controller chooses operations that expand, test, connect, compress, or terminate the web.

WoT has five defining properties:

1. **Multidimensional framing** — relevant perspectives are selected for the task rather than forcing every problem into the same decomposition.
2. **Typed topology** — links have semantics; they are not merely traversal history.
3. **Cross-path interaction** — partial ideas can challenge, support, or combine with ideas created elsewhere.
4. **Budget-aware control** — expansion competes with verification, synthesis, and stopping.
5. **Auditable output** — conclusions point to decisive evidence, assumptions, and unresolved uncertainty.

## Candidate dimensions

Dimensions are lenses used to create useful diversity. They are selected, not exhaustively applied.

- temporal: past causes, current state, future consequences;
- causal: mechanism, contributing factors, downstream effects;
- stakeholder: users, operators, adversaries, regulators, maintainers;
- abstraction: principles, strategies, mechanisms, implementation details;
- evidence: known facts, assumptions, unknowns, tests;
- objective: quality, cost, speed, safety, reversibility;
- scenario: optimistic, expected, pessimistic, adversarial;
- discipline: technical, economic, behavioral, ethical, operational.

Dimensions and node types are different. A `hypothesis` node may arise from an adversarial or economic dimension.

## What WoT is not

- A request to produce an extremely long step-by-step monologue.
- A fixed mind map applied to every task.
- Exhaustive search over all imaginable answers.
- Majority voting without analysis of shared failure modes.
- A synonym for Graph of Thoughts; WoT adds a specific controller, typed epistemic relations, dimensional coverage, and efficiency objective that must be empirically validated.
- A guarantee of factuality. External evidence and task-specific verifiers remain necessary.

## Intended task profile

WoT is most plausible when a task has several interacting constraints, multiple viable approaches, delayed consequences, decomposable subproblems, or a need to reconcile heterogeneous evidence. Examples include planning, architecture, diagnosis, research synthesis, policy analysis, and difficult constraint satisfaction.

Direct prompting should remain the default for simple retrieval, rewriting, classification, or calculations with a short deterministic path. The controller should be allowed to decide that no web is warranted.

## Proposed novelty boundary

The research contribution is not “reasoning as a graph” by itself. That idea already exists. The proposed contribution is the combination of:

- task-adaptive dimensions that create structured diversity;
- typed epistemic and compositional edges;
- an explicit frontier scheduler based on expected value per cost;
- contradiction and assumption ledgers;
- synthesis as a first-class operator;
- density and redundancy penalties;
- convergence and marginal-value stopping rules; and
- complete quality–cost–latency evaluation.

Every item is provisional until an ablation shows value.

## Design principles

### Structure must earn its cost

Each added node or edge should change a decision, resolve uncertainty, increase coverage, or enable synthesis. Decorative structure is overhead.

### Diversity before volume

Prefer candidates generated from meaningfully different assumptions or dimensions. Paraphrases do not count as independent paths.

### Critique must be targeted

Critique high-impact or high-uncertainty nodes first. Universal self-critique wastes tokens and can degrade correct answers.

### Synthesis is not voting

A synthesis must identify compatible components, resolve conflicts, preserve constraints, and state what was discarded.

### Confidence is evidence-sensitive

Scores are routing heuristics. Confidence should increase through independent evidence, executable checks, or agreement between genuinely diverse methods—not repetition.

### Stop intelligently

More thought is not always better. Stop when the best candidate satisfies acceptance criteria, critical contradictions are resolved, and expected gain from the frontier falls below its cost.

