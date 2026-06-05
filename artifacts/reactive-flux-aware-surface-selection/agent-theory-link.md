---
title: Reactive Flux Theory → Agent Evaluation Theory (CLEAR) Link
license: CC-BY-4.0
tags:
  - reactive-flux
  - recrossing
  - metadynamics
  - agent-evaluation
  - CLEAR
  - reliability
  - decision-model
  - research-to-decision
---

# Reactive Flux Theory → Agent Evaluation Theory

This note links the surface-reaction rate paper that seeded the
`reactive-flux-aware-surface-selection` artifact to **agent theory** as it is
defined in this foundation: the CLEAR evaluation framework (Cost, Latency,
Efficacy, Assurance, Reliability) and the research-to-decision loop.

The connection is not a loose metaphor. Both domains estimate a **rate of
successful transitions across a decision boundary**, and both show that the
*naive equilibrium estimate overcounts true successes* unless it is multiplied
by a *dynamical correction*. In chemistry that correction is the transmission
coefficient; in agent evaluation it is repeated-run reliability.

## Research Contract

```yaml
research_id: rf-2025-agent-theory-link
question: >
  How does first-principles reactive flux theory for surface reactions map
  onto the foundation's agent-evaluation theory (CLEAR), and what design
  guidance does it transfer?
scope: >
  Conceptual transfer only. Maps rate-theory constructs to CLEAR dimensions and
  to the research/evaluation loops. No new simulation or benchmark data.
sources:
  - id: source.paper
    citation: >
      Li C, Zeng X, Li Y, Li Z, Guo H, Jiang B. "First Principles Reactive Flux
      Theory for Surface Reactions: Multiple Channels and Recrossing Dynamics."
    artifact_ref: artifacts/reactive-flux-aware-surface-selection/
  - id: source.clear
    citation: >
      "Beyond Accuracy: A Multi-Dimensional Framework for Evaluating Enterprise
      Agentic AI Systems" (CLEAR framework, per repository README).
    artifact_ref: README.md#first-concrete-vertical-clearbench
source_freshness_requirements:
  - Re-check if CLEARBench dimensions or weights change.
  - Re-check if the surface-selection artifact gains computed simulation data.
trust_refs: []
options_considered:
  - Standalone RL/rate-theory write-up (rejected: not grounded in this repo).
  - Bridge note inside the existing reactive-flux artifact (chosen).
recommendation: >
  Adopt the recrossing/κ ↔ pass@k Reliability mapping as the canonical framing
  that connects the reactive-flux artifact to CLEARBench, and reuse the
  "multiple channels" and "collective-variable selection" lessons when
  designing competing-goal and abstraction-sensitive agent benchmarks.
assumptions:
  - "Agent theory" here means the foundation's CLEAR evaluation theory, not
    reinforcement-learning theory in general.
  - The mapping is structural/analogical; it transfers design guidance, not
    numerical results.
risks:
  - Over-claiming a physical equivalence where only a structural analogy holds.
limitations:
  - No empirical validation of the analogy against CLEARBench runs yet.
decision_refs:
  - Informs future CLEARBench task design (competing-goal, reliability gates).
```

## Core mapping

The paper factorizes the rate as **k = κ · k_TST**: a naive transition-state
estimate `k_TST` corrected by a transmission coefficient `κ ≤ 1` that removes
trajectories which cross the dividing surface but recross back. CLEAR makes the
same move for agents.

| Reactive flux construct | CLEAR / agent-evaluation analogue |
| --- | --- |
| Dividing surface at the transition state | The commitment / success boundary a run must cross |
| TST rate `k_TST` (equilibrium, no recrossing) | Single-shot accuracy — counts a crossing as a success |
| Transmission coefficient `κ ≤ 1` (recrossing) | **Reliability**: pass@k over repeated runs corrects apparent success |
| Recrossing trajectory (crosses then returns) | A run that "succeeds" once but is not stable on repeat (flaky pass / churn) |
| Harmonic approximation overcounts soft-mode entropy → 20–100× rate error | Optimistic point estimates overstate real-world agent throughput |
| Multiple coupled channels (oxidation vs desorption) | Competing goals/actions an agent cannot cleanly separate |
| Collective-variable choice (too few ⇒ wrong free energy) | State-abstraction / metric choice — wrong features ⇒ wrong verdict |
| Metadynamics bias to escape minima | Adaptive exploration to surface rare failure modes |
| Dividing-surface independence (Bennett–Chandler) | Robust metrics: the verdict should not depend on exactly where the bar is drawn |

## Three transferable lessons

1. **Reliability is a recrossing correction.** The paper's headline failure of
   transition-state theory — overcounting success by 20–100× because it ignores
   recrossing — is the chemistry statement of why single-run accuracy
   overstates agent quality. CLEAR's Reliability dimension plays the role of the
   `κ` factor: it discounts runs that "cross the bar" once but recross on repeat.
   Treat `κ` and repeated-run reliability as the same correction.

   **Implementation note (do not over-claim).** As of this commit, CLEARBench's
   Reliability is computed by `agent_research/core/metrics.py::pass_at_k`, which
   returns the *mean success rate over repeated runs*
   (`sum(results) / len(results)`); `build_summary` applies it to the flattened
   run successes. It does **not** yet compute per-k pass@3/5/8, the standard
   pass@k "at least one of k succeeds" estimator, or success **variance**. Those
   richer estimators are **proposed** here as the natural way to make the `κ`
   analogy quantitative — they are design input, not existing measurements. Any
   downstream decision record citing pass@3/5/8 or variance must treat them as
   proposed until the implementation is aligned.

2. **Multiple channels need multiple coordinates.** CO oxidation could not be
   evaluated in isolation because CO desorption competes for the same adsorbate;
   a single reaction coordinate gave the wrong free energy. The agent analogue:
   benchmarks for tasks with **competing goals** (e.g. helpfulness vs. an
   Assurance/safety constraint) must measure both channels jointly, or the
   primary-channel score is corrupted. This argues for multi-objective CLEAR
   tasks rather than single-axis ones.

3. **Abstraction choice decides correctness.** Choosing too few collective
   variables produced a confidently wrong result (paper Fig. S2). The same holds
   for agent metrics: pick the wrong observables/state abstraction and the
   evaluation is wrong with false confidence. Validate metric sufficiency the way
   the paper validates CV sufficiency — by checking that the verdict has
   converged as you add observables.

## How this plugs into the foundation's loops

- **Research loop** — this note is the `synthesize options → recommend → link
  decision to evidence` step for the question above, with provenance to both
  sources.
- **Evaluation loop** — the recrossing↔Reliability mapping is direct design
  input to CLEARBench: it justifies repeated-run gates and competing-goal tasks
  as first-class, not optional.

## Status

Conceptual bridge artifact. Structural analogy only; no computed simulation or
CLEARBench data attached yet. Companion to `README.md` and
`protocol/surface_selection_protocol.md` in this artifact.
