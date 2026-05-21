import React, { useMemo, useState } from 'react';
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  Node,
  Edge,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { agentNodes, handoffs, loops, taskScores } from './sampleData';

const nodes: Node[] = agentNodes.map((agent, index) => ({
  id: agent.id,
  position: { x: 120 + index * 260, y: agent.weakLink ? 240 : 120 },
  data: {
    label: `${agent.label}\nTrust: ${agent.trustScore}\n${agent.weakLink ? 'Weak Link' : agent.status}`,
    kind: 'agent',
    ...agent,
  },
  style: {
    border: agent.weakLink ? '3px solid #ef4444' : '2px solid #22c55e',
    padding: 12,
    borderRadius: 10,
    whiteSpace: 'pre-line',
    background: agent.weakLink ? '#fef2f2' : '#f0fdf4',
  },
}));

const handoffEdges: Edge[] = handoffs.map((handoff) => ({
  id: handoff.id,
  source: handoff.source,
  target: handoff.target,
  label: `${handoff.label} • score ${handoff.score}`,
  data: {
    kind: 'handoff',
    ...handoff,
  },
}));

const loopEdges: Edge[] = loops.map((loop) => ({
  id: loop.id,
  source: loop.source,
  target: loop.target,
  label: `↺ ${loop.iterations}x • ${loop.label}`,
  animated: true,
  style: {
    stroke: loop.improvedScore ? '#f59e0b' : '#ef4444',
    strokeWidth: 3,
  },
  data: {
    kind: 'loop',
    ...loop,
  },
}));

const edges: Edge[] = [...handoffEdges, ...loopEdges];

function DetailPanel({ selected }: { selected: any }) {
  if (!selected) {
    return (
      <aside style={panelStyle}>
        <h2>Inspector</h2>
        <p>Click an agent, handoff, or loop to inspect values.</p>
      </aside>
    );
  }

  if (selected.kind === 'agent') {
    const scores = taskScores.filter((score) => score.agent === selected.id);

    return (
      <aside style={panelStyle}>
        <h2>{selected.label}</h2>
        <p><strong>Role:</strong> {selected.role}</p>
        <p><strong>Trust Score:</strong> {selected.trustScore}</p>
        <p><strong>Status:</strong> {selected.status}</p>
        <p><strong>Weak Link:</strong> {String(selected.weakLink)}</p>
        <h3>Task Scores</h3>
        {scores.map((score) => (
          <div key={`${score.taskId}-${score.agent}`} style={cardStyle}>
            <div><strong>Task:</strong> {score.taskId}</div>
            <div><strong>Score:</strong> {score.score}</div>
            <div><strong>Passed:</strong> {String(score.passed)}</div>
          </div>
        ))}
      </aside>
    );
  }

  if (selected.kind === 'loop') {
    return (
      <aside style={panelStyle}>
        <h2>Loop Inspector</h2>
        <p><strong>From:</strong> {selected.source}</p>
        <p><strong>To:</strong> {selected.target}</p>
        <p><strong>Reason:</strong> {selected.label}</p>
        <p><strong>Iterations:</strong> {selected.iterations}</p>
        <p><strong>Cost:</strong> ${selected.costUsd}</p>
        <p><strong>Latency:</strong> {selected.latencySeconds}s</p>
        <p><strong>Improved Score:</strong> {String(selected.improvedScore)}</p>
      </aside>
    );
  }

  return (
    <aside style={panelStyle}>
      <h2>Handoff Inspector</h2>
      <p><strong>From:</strong> {selected.source}</p>
      <p><strong>To:</strong> {selected.target}</p>
      <p><strong>Passed Value:</strong> {selected.label}</p>
      <p><strong>Handoff Score:</strong> {selected.score}</p>
    </aside>
  );
}

const panelStyle: React.CSSProperties = {
  width: 360,
  padding: 20,
  borderLeft: '1px solid #e5e7eb',
  background: '#ffffff',
  overflow: 'auto',
};

const cardStyle: React.CSSProperties = {
  border: '1px solid #e5e7eb',
  borderRadius: 8,
  padding: 10,
  marginBottom: 10,
  background: '#f9fafb',
};

export default function App() {
  const [selected, setSelected] = useState<any>(null);

  const flowNodes = useMemo(() => nodes, []);
  const flowEdges = useMemo(() => edges, []);

  return (
    <div style={{ display: 'flex', width: '100vw', height: '100vh' }}>
      <div style={{ flex: 1 }}>
        <ReactFlow
          nodes={flowNodes}
          edges={flowEdges}
          fitView
          onNodeClick={(_, node) => setSelected(node.data)}
          onEdgeClick={(_, edge) => setSelected(edge.data)}
        >
          <Background />
          <MiniMap />
          <Controls />
        </ReactFlow>
      </div>
      <DetailPanel selected={selected} />
    </div>
  );
}
