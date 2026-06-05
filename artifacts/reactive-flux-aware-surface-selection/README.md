---
title: Reactive-Flux-Aware Surface Selection
license: CC-BY-4.0
tags:
  - catalysis
  - surface-science
  - materials-science
  - computational-chemistry
  - reactive-flux
  - transition-state-theory
  - metadynamics
  - decision-model
---

# Reactive-Flux-Aware Surface Selection

A reusable decision model, schema, and protocol for selecting catalyst surfaces using static descriptors, transition-state estimates, metadynamics, and reactive-flux-aware dynamic validation.

## Purpose

Traditional catalyst screening often relies on adsorption energies and activation barriers. This artifact defines a reusable model for evaluating catalyst surfaces under real operating conditions by adding:

- multiple reaction channels
- free-energy surface analysis
- recrossing correction
- uncertainty
- poisoning risk
- manufacturability
- provenance

## Core idea

A surface should not be selected only because it has a low static activation barrier.

A better surface-selection decision should consider:

```text
Surface Score =
  Activity
+ Selectivity
+ Stability
+ Low Poisoning Risk
+ Low Recrossing Loss
+ Manufacturability
+ Cost
```

## Workflow

```text
Define reaction
→ Generate candidate surfaces
→ Compute static descriptors
→ Estimate TST rate
→ Run metadynamics
→ Build free-energy surface
→ Apply reactive flux correction
→ Analyze recrossing
→ Score surfaces
→ Rank
→ Publish decision record
```

## Main entities

- Reaction
- Surface
- Material
- Facet
- Defect
- Alloy
- Support
- OperatingCondition
- Descriptor
- FreeEnergySurface
- ReactionChannel
- ReactiveFluxRun
- Score
- Decision
- Evidence
- Provenance

## Status

Initial schema and protocol artifact. It does not yet include computed DFT, metadynamics, or reactive-flux simulation outputs.

## Intended use

Use this artifact as a template for:

- catalyst surface screening
- computational catalysis benchmarking
- materials decision intelligence
- surface-reaction dataset governance
- ML-ready catalysis metadata
