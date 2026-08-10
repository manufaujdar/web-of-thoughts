# Evaluation framework

## Claim discipline

The central claim to test is not “WoT produces impressive answers.” It is:

> Under matched models and declared resource budgets, WoT improves task utility or the quality–cost frontier on identifiable classes of complex tasks.

Pre-register the primary metric, budget, stopping rule, and comparison set before inspecting test results where feasible.

## Baselines

At minimum:

1. direct prompting;
2. zero-shot or few-shot Chain of Thought;
3. self-consistency with matched sample budget;
4. Tree of Thoughts with matched search budget;
5. Graph of Thoughts or the closest implementable graph baseline;
6. WoT without external verification;
7. full WoT.

Use the same model, temperature policy, tool permissions, context, and evaluation rubric unless the variable is explicitly under study.

## Task families

- deterministic planning and constraint satisfaction;
- mathematical or symbolic problems with executable checks;
- multi-hop research with source verification;
- diagnosis and troubleshooting with hidden ground truth;
- design or architecture tasks with expert rubrics;
- adversarial and ambiguity-rich decision scenarios;
- creative synthesis, evaluated separately because automatic judging is less reliable.

Include simple tasks to measure the cost of unnecessary deliberation.

## Metrics

### Quality

- exact success or task-specific score;
- hard-constraint satisfaction rate;
- factual precision and citation correctness;
- robustness under paraphrase or irrelevant context;
- calibration or selective accuracy where probabilities are elicited;
- expert blind preference for open-ended tasks.

### Efficiency

- total input and output tokens;
- model and tool calls;
- wall-clock latency;
- monetary cost at recorded prices;
- nodes and edges created, retained, verified, and used in the final answer;
- success per 1K tokens and utility per dollar.

### Search behavior

- candidate diversity before and after deduplication;
- fraction of nodes pruned or merged;
- contradiction resolution rate;
- verifier yield: decisions changed per verification cost;
- synthesis yield: accepted syntheses that outperform all parents;
- regret against the best generated candidate;
- termination reason and unused budget.

## Required ablations

- no dimensions;
- no typed edges;
- no cross-path links;
- no contradiction ledger;
- no synthesis;
- fixed breadth/depth instead of adaptive scheduling;
- no redundancy penalty;
- fixed hard stop instead of marginal-value stop;
- self-evaluation only versus heterogeneous verification.

Change one mechanism at a time. Factorial designs are useful after basic effects are established.

## Experimental validity

- Keep a hidden test set and prevent prompt tuning on it.
- Randomize method order and blind human judges.
- Use multiple seeds and report variance or confidence intervals.
- Check evaluator bias, including preference for longer or more structured answers.
- Separate development failures from task failures.
- Record all retries and invalid runs.
- Treat model version, date, and provider settings as experimental variables.
- Report Pareto frontiers rather than a single accuracy number when costs differ.

## Promotion criteria

A component moves from `hypothesis` to `candidate default` only if it shows a repeatable benefit on at least two task families without unacceptable regression in cost or simple-task behavior. It becomes a `default` only after replication on a second model family or independent implementation.

