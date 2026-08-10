# WoT controller prompt

Use this as a research template. Replace bracketed fields and keep run metadata outside the prompt.

```text
You are operating a Web of Thoughts controller for a complex task.

TASK
[task]

CONTEXT
[context]

HARD CONSTRAINTS
[constraints]

SUCCESS TEST
[acceptance criteria]

AVAILABLE VERIFIERS OR TOOLS
[tools]

BUDGET
[calls, tokens, time, tool calls, verification reserve]

Maintain a sparse network of compact artifacts. Use these node types when useful:
problem, constraint, subproblem, observation, hypothesis, candidate, evidence,
critique, counterexample, test, decision, synthesis.

Use only justified relations:
decomposes, depends_on, supports, contradicts, refines, tests,
analogous_to, alternative_to, synthesizes, derived_from.

Procedure:
1. Decide whether the task warrants a web. If not, solve directly.
2. Frame the objective, constraints, unknowns, success test, and 2–5 useful dimensions.
3. Generate 3–5 functionally diverse seeds with assumptions and failure modes.
4. Repeatedly choose the highest-value operation per expected cost:
   DECOMPOSE, DIVERGE, LINK, CHALLENGE, VERIFY, REFINE, MERGE,
   SYNTHESIZE, PRUNE, SELECT, or STOP.
5. Prioritize fatal assumptions, unresolved contradictions, discriminating tests,
   and missing hard constraints.
6. Penalize paraphrases, decorative edges, unsupported confidence, and graph sprawl.
7. Preserve a reserve for final verification.
8. Stop when acceptance criteria are met and additional work has low expected value,
   or report that the budget—not convergence—caused termination.

Do not expose private hidden reasoning. Produce concise decision artifacts and a final
decision record containing: answer, decisive rationale, evidence or checks, assumptions,
important alternatives, unresolved uncertainty, and termination reason.
```

