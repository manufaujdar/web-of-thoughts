# Contributing

Web of Thoughts should evolve through explicit claims and reproducible evidence.

## Proposing a mechanism

An addition must state:

1. the failure mode it addresses;
2. the proposed mechanism;
3. why an existing operator cannot handle it;
4. expected quality benefit and resource cost;
5. a falsifiable prediction;
6. an ablation or comparison plan;
7. new risks or ways it can fail.

## Changing the specification

- Keep terminology consistent with the glossary.
- Label untested defaults as hypotheses.
- Update prompts, schema, and evaluation plan when a contract changes.
- Record breaking changes in a future changelog before implementation begins.
- Do not use benchmark anecdotes as general proof.

## Experiment review checklist

- Is the baseline strong and budget-matched?
- Is the outcome independently checkable or blindly judged?
- Are prompts, versions, seeds, failures, and actual costs recorded?
- Could answer length or formatting bias the evaluator?
- Is the conclusion narrower than or equal to the evidence?
- Are null and negative results retained?

