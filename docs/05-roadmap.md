# Research roadmap

## Phase 0: specification

- Stabilize vocabulary, node/edge contracts, and controller states.
- Create a hand-executable prompt-only protocol.
- Define baselines and experiment records.
- Select small, checkable pilot tasks.

Exit: two researchers can independently execute the protocol and produce comparable logs.

## Phase 1: manual pilots

- Run direct, CoT, self-consistency, ToT, and WoT on 20–50 tasks.
- Inspect whether dimensions create real diversity.
- Measure graph overhead and identify useless fields.
- Build a failure taxonomy.

Exit: reproducible evidence that at least one WoT mechanism sometimes changes outcomes beneficially.

## Phase 2: minimal orchestrator

- Implement typed state storage and schema validation.
- Add configurable operators, budgets, and event logging.
- Add semantic deduplication and deterministic verifiers.
- Reproduce manual runs.

Exit: automated logs match the formal model and runs are replayable.

## Phase 3: controlled evaluation

- Run budget-matched baselines across task families and models.
- Perform required ablations.
- Estimate uncertainty and Pareto frontiers.
- Test the gate that decides whether WoT is warranted.

Exit: a supported scope claim or an explicit null result.

## Phase 4: controller learning

- Learn operator selection from logged outcomes.
- Compare learned, heuristic, and fixed controllers.
- Evaluate transfer across task families and model versions.
- Add safeguards against reward hacking and evaluator exploitation.

Exit: controller improvement holds on hidden tasks without greater normalized cost.

## Phase 5: release

- Publish specification, prompts, code, seeds, task splits, and full results.
- Document privacy, safety, and reproducibility limitations.
- Version the method independently from implementations.

## Immediate backlog

1. Define the first 25-task pilot set.
2. Choose a machine-readable graph serialization.
3. Implement schema validation and token/cost logging.
4. Write baseline prompt templates.
5. Agree on the initial scheduler weights and reserve policy.
6. Design a semantic diversity measure resistant to paraphrase.
7. Create golden examples of useful and useless edges.
8. Create failure labels for premature convergence, graph sprawl, correlated verification, false synthesis, and overthinking.

