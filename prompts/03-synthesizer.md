# Synthesis operator

```text
Attempt to synthesize source nodes [IDS] into a candidate stronger than every source.

List:
- compatible components retained from each source;
- conflicts and how they are resolved;
- hard constraints preserved;
- new assumptions or failure modes introduced;
- evidence and provenance retained;
- expected improvement over the strongest source;
- a test that could show the synthesis is worse.

If the components are incompatible or combination adds no value, return NO_SYNTHESIS
with a concise reason. Do not average incompatible claims or use majority vote as synthesis.
```

