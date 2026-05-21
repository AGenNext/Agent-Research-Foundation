export const agentNodes = [
  {
    id: 'planner',
    label: 'Planner Agent',
    role: 'Breaks task into subtasks',
    trustScore: 0.82,
    status: 'passed',
    weakLink: false,
  },
  {
    id: 'researcher',
    label: 'Research Agent',
    role: 'Collects evidence and sources',
    trustScore: 0.76,
    status: 'passed',
    weakLink: false,
  },
  {
    id: 'coder',
    label: 'Coder Agent',
    role: 'Implements solution',
    trustScore: 0.61,
    status: 'warning',
    weakLink: true,
  },
  {
    id: 'reviewer',
    label: 'Reviewer Agent',
    role: 'Checks correctness and risk',
    trustScore: 0.88,
    status: 'passed',
    weakLink: false,
  },
  {
    id: 'executor',
    label: 'Execution Agent',
    role: 'Runs tests and tools',
    trustScore: 0.93,
    status: 'passed',
    weakLink: false,
  },
];

export const handoffs = [
  {
    id: 'handoff-planner-researcher',
    source: 'planner',
    target: 'researcher',
    label: 'research plan + assumptions',
    score: 0.84,
  },
  {
    id: 'handoff-researcher-coder',
    source: 'researcher',
    target: 'coder',
    label: 'evidence + implementation constraints',
    score: 0.71,
  },
  {
    id: 'handoff-coder-reviewer',
    source: 'coder',
    target: 'reviewer',
    label: 'patch + rationale',
    score: 0.58,
  },
  {
    id: 'handoff-reviewer-executor',
    source: 'reviewer',
    target: 'executor',
    label: 'test plan + risk notes',
    score: 0.91,
  },
];

export const loops = [
  {
    id: 'loop-reviewer-coder',
    source: 'reviewer',
    target: 'coder',
    label: 'revision loop: security issue found',
    iterations: 2,
    costUsd: 0.042,
    latencySeconds: 18.4,
    improvedScore: true,
  },
  {
    id: 'loop-executor-coder',
    source: 'executor',
    target: 'coder',
    label: 'test-fix loop: failing unit test',
    iterations: 3,
    costUsd: 0.061,
    latencySeconds: 31.7,
    improvedScore: false,
  },
];

export const taskScores = [
  {
    taskId: 'software_dev_bugfix_001',
    agent: 'planner',
    score: 0.86,
    passed: true,
  },
  {
    taskId: 'software_dev_bugfix_001',
    agent: 'researcher',
    score: 0.74,
    passed: true,
  },
  {
    taskId: 'software_dev_bugfix_001',
    agent: 'coder',
    score: 0.52,
    passed: false,
  },
  {
    taskId: 'software_dev_bugfix_001',
    agent: 'reviewer',
    score: 0.89,
    passed: true,
  },
  {
    taskId: 'software_dev_bugfix_001',
    agent: 'executor',
    score: 0.94,
    passed: true,
  },
];
