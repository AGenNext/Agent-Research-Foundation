# Surface Selection Protocol

## Objective

Select a catalyst surface based on real dynamic reaction behavior, not static barriers alone.

## Protocol

1. Define reaction and target product.
2. Define operating conditions.
3. Generate candidate surfaces.
4. Compute static descriptors.
5. Estimate transition-state-theory rate.
6. Run enhanced sampling or metadynamics.
7. Build the free-energy surface.
8. Run reactive flux correction.
9. Analyze recrossing and multiple channels.
10. Score activity, selectivity, stability, poisoning risk, recrossing loss, manufacturability, and cost.
11. Apply rejection gates.
12. Rank surfaces.
13. Publish a decision record with provenance.

## Decision Principle

Do not select a surface only because of a low activation barrier.

Select the surface with the best corrected real-world behavior under the target operating condition.

## Rejection Gates

Reject a surface if any of these are true:

- adsorption is too weak
- adsorption is too strong
- surface reconstructs badly under operating conditions
- poisoning risk is high
- recrossing loss is high
- uncertainty is high
- manufacturing is unrealistic
- cost exceeds the target envelope

## Required Evidence

Each selected or rejected surface should include:

- reaction definition
- surface identity
- operating condition
- static descriptor values
- dynamic correction method
- uncertainty estimate
- scoring weights
- decision reason
- provenance record
