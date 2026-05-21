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
- AI and agent evaluation research

## First Concrete Vertical: CLEARBench

CLEARBench is the first implementation vertical inside Agent Research.

It is inspired by the CLEAR framework from *Beyond Accuracy: A Multi-Dimensional Framework for Evaluating Enterprise Agentic AI Systems*.

CLEAR evaluates agentic systems across five production dimensions:

- **Cost**: token usage, estimated API cost, cost per success, cost-normalized accuracy
- **Latency**: wall-clock execution time, p50/p95 latency, SLA compliance
- **Efficacy**: task success and domain-specific grading
- **Assurance**: safety, policy compliance, prompt-injection resistance, data-leak prevention
- **Reliability**: repeated-run stability through pass@k-style measurements

The goal is to move beyond accuracy-only benchmarks and produce reproducible evaluation artifacts for enterprise AI agents.

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
No evaluation without reproducible artifacts.
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

## Evaluation Loop

```text
benchmark
  → run agent/model
  → capture traces
  → grade outputs
  → calculate CLEAR metrics
  → generate report
  → compare alternatives
  → preserve artifacts
```

## Quick Start

```bash
pip install -e .
agent-research clear run benchmarks/clearbench_mini --agent echo --repeats 3 --output outputs/clearbench-mini-echo
agent-research clear report outputs/clearbench-mini-echo
```

## Repository Boundary

```text
Agent-Research
  → evidence gathering, research contracts, and research-backed evaluation verticals

Agent-Trust
  → provenance and trust scoring

Agent-Eval
  → shared scoring and evaluation methods

Agent-Analytics
  → adoption/performance signals

Agent-Team
  → uses research and evaluation to make better decisions
```
