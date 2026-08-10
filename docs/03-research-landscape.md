# Research landscape

WoT is inspired by a family of inference-time reasoning methods. The distinctions below define the starting research question; they do not establish that WoT performs better.

## Relevant foundations

- **Chain of Thought (CoT)** elicits intermediate reasoning steps in a linear sequence.
- **Self-consistency** samples multiple reasoning paths and aggregates answers, demonstrating value from diverse trajectories.
- **ReAct** interleaves reasoning artifacts with actions and observations, grounding some decisions in an environment.
- **Tree of Thoughts (ToT)** searches over coherent intermediate thoughts, with evaluation, lookahead, and backtracking.
- **Graph of Thoughts (GoT)** models thoughts as vertices with dependencies as edges and supports transformations such as aggregation and feedback.
- **Algorithm of Thoughts (AoT)** prompts an algorithmic exploration trajectory within one or a few calls to reduce orchestration cost.
- **Everything of Thoughts (XoT)** combines learned guidance with search to target performance, efficiency, and flexibility.

## WoT research position

| Property | Linear chain | Tree search | General thought graph | Proposed WoT |
|---|---:|---:|---:|---:|
| Multiple candidates | limited | yes | yes | yes |
| Cross-branch links | no | limited | yes | yes |
| Typed epistemic edges | no | no | possible | required |
| Task-selected dimensions | no | optional | optional | required at framing |
| Contradiction/assumption ledger | no | optional | optional | required |
| Adaptive value-per-cost scheduler | no | often search heuristic | implementation-dependent | required |
| Synthesis with provenance | no | limited | yes | required |
| Explicit marginal-value stopping | no | budget/depth | implementation-dependent | required |

The honest null hypothesis is that these additions are bookkeeping overhead and a well-designed GoT, ToT, or self-consistency baseline performs as well at lower cost.

## Primary sources

- Wei et al., [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903), 2022.
- Wang et al., [Self-Consistency Improves Chain of Thought Reasoning in Language Models](https://arxiv.org/abs/2203.11171), 2022.
- Yao et al., [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629), 2022/2023.
- Yao et al., [Tree of Thoughts: Deliberate Problem Solving with Large Language Models](https://arxiv.org/abs/2305.10601), 2023.
- Besta et al., [Graph of Thoughts: Solving Elaborate Problems with Large Language Models](https://arxiv.org/abs/2308.09687), 2023.
- Sel et al., [Algorithm of Thoughts: Enhancing Exploration of Ideas in Large Language Models](https://arxiv.org/abs/2308.10379), 2023.
- Ding et al., [Everything of Thoughts: Defying the Law of Penrose Triangle for Thought Generation](https://arxiv.org/abs/2311.04254), 2023.

## Open research questions

1. Which task features predict a benefit from web construction?
2. Do typed edges improve decisions, or merely improve interpretability?
3. Which dimensions reliably create functional rather than cosmetic diversity?
4. Does cross-path synthesis outperform selecting the best independent path?
5. Can a model estimate marginal value well enough to schedule its own search?
6. How sparse should the web remain as task complexity grows?
7. Which verification mixtures reduce correlated model errors?
8. Can a compact single-call WoT approximate an orchestrated multi-call version?
9. When does additional deliberation cause overthinking or answer degradation?
10. How should useful reasoning artifacts be exposed without relying on private reasoning traces?

