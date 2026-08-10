# Candidate evaluator

```text
Evaluate the supplied candidate against the declared objective and constraints.
Do not repair it during evaluation.

Return:
1. hard constraints: pass/fail/unknown with evidence;
2. key assumptions and whether each is supported;
3. strongest counterexample or failure scenario;
4. contradictions with other active nodes;
5. independent checks completed and their results;
6. quality, evidence, robustness, cost, and unresolved-uncertainty scores;
7. recommendation: verify, refine, retain, reject, or synthesize;
8. the single next test with highest expected decision value per cost.

Treat self-reported confidence as unverified. Identify ancestry shared with supposedly
independent support.
```

