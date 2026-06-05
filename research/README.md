# Research Collection

Tracked, provenance-backed research entries for the Agent Research Foundation.

Each entry follows [`contracts/research-contract.md`](../contracts/research-contract.md):
every recommendation is traceable to a current, cited source.

## Layout

```text
research/
  papers/   academic and perspective papers tracked as evidence
            <arxiv-id>-<slug>.md     human-readable evidence note
            <arxiv-id>-<slug>.yaml   structured research-contract entry
```

## Papers

| ID | Title | Authors | Source | Category | Captured |
| --- | --- | --- | --- | --- | --- |
| `paper-2605.29207-augmentation-to-reconstruction` | From Augmentation to Reconstruction: Guiding the AI Disruption to the Good Place | Rothschild, Hofman, Mobius, Lucier, Dillon, Goldstein, Immorlica, Slivkins (Microsoft Research) | [arXiv:2605.29207](papers/2605.29207-augmentation-to-reconstruction.md) | academic | 2026-06-04 |

## Adding an entry

1. Create `papers/<arxiv-id>-<slug>.md` with provenance, thesis, and key claims.
2. Create `papers/<arxiv-id>-<slug>.yaml` conforming to the research contract schema.
3. Add a row to the table above.
4. Link any decision that relies on the entry back to its `research_id`.
