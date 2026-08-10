# Node generator

```text
Given the problem frame and current web summary, propose at most [N] new nodes for
the requested operation [OPERATOR] and dimension [DIMENSION].

Each proposal must include:
- type and compact content;
- parent or target node IDs;
- assumptions;
- what makes it non-redundant;
- expected decision value;
- likely failure mode;
- cheapest discriminating test;
- estimated cost.

Return no proposal when existing nodes already cover the useful space.
Do not score a node more highly merely because it is detailed or confidently written.
```

