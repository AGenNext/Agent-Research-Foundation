# Agent Research

Agent Research defines reusable research intelligence contracts for AGenNext agentic systems.

## Responsibility

Agent Research owns research collection, evidence tracking, and research-to-decision workflows.

It helps agents ground product, technical, market, and architecture decisions in evidence.

## Scope

Agent Research covers:

- academic research tracking
- arXiv/paper evidence
- market research
- competitor research
- technical due diligence
- tool/library research
- license and ecosystem research
- research freshness checks
- research-to-decision traceability

## Consumers

- Agent-Team
- Agent-Knowledge
- Agent-Blueprint
- Agent-Eval
- Agent-Bench
- Model-Router
- future AGenNext products

## Core Principle

```text
No strategic decision without evidence.
No evidence without source.
No source without freshness and provenance.
```

## Research Loop

```text
question
  → search sources
  → collect evidence
  → evaluate trust
  → synthesize options
  → recommend decision
  → link decision to evidence
  → refresh when evidence changes
```

## Repository Boundary

```text
Agent-Research
  → evidence gathering and research contracts

Agent-Trust
  → provenance and trust scoring

Agent-Eval
  → scoring and evaluation methods

Agent-Analytics
  → adoption/performance signals

Agent-Team
  → uses research to make better decisions
```
