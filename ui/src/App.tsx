import React, { useMemo, useState } from 'react';
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  Node,
  Edge,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { agentNodes, handoffs, loops, taskScores, executionLogs } from './sampleData';

const nodes: Node[] = agentNodes.map((agent, index) => ({
  id: agent.id,
  position: { x: 120 + index * 260, y: agent.weakLink ? 260 : 120 },
  data: {
    label: `${agent.label}\nScore: ${agent.score} • Trust: ${agent.trustScore}\nCost: $${agent.costUsd} • ${agent.latencySeconds}s\nTokens: ${agent.tokens}\n${agent.weakLink ? 'WEAK LINK' : agent.status}`,
    kind: 'agent',
    ...agent,
  },
  style: {
    border: agent.weakLink ? '3px solid #ef4444' : '2px solid #22c55e',
    padding: 12,
    borderRadius: 10,
    whiteSpace: 'pre-line',
    background: agent.weakLink ? '#fef2f2' : '#f0fdf4',
    minWidth: 220,
  },
}));

const handoffEdges: Edge[] = handoffs.map((handoff) => ({
  id: handoff.id,
  source: handoff.source,
  target: handoff.target,
  label: `${handoff.label} • score ${handoff.score}`,
  data: { kind: 'handoff', ...handoff },
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
  data: { kind: 'loop', ...loop },
}));

const edges: Edge[] = [...handoffEdges, ...loopEdges];

function resolveTarget(log: any) {
  return (
    nodes.find((node) => node.id === log.targetId)?.data ||
    edges.find((edge) => edge.id === log.targetId)?.data ||
    null
  );
}

function DetailPanel({ selected }: { selected: any }) {
  if (!selected) {
    return (
      <aside style={panelStyle}>
        <h2>Inspector</h2>
        <p>Click a log row to inspect the exact event.</p>
      </aside>
    );
  }

  const target = selected.event ? resolveTarget(selected.event) : selected;

  return (
    <aside style={panelStyle}>
      {selected.event && (
        <div style={cardStyle}>
          <h2>Log Event</h2>
          <p><strong>Time:</strong> {selected.event.time}</p>
          <p><strong>Type:</strong> {selected.event.type}</p>
          <p><strong>Message:</strong> {selected.event.message}</p>
          <p><strong>Event Score:</strong> {selected.event.score}</p>
        </div>
      )}

      {target?.kind === 'agent' && (
        <>
          <h2>{target.label}</h2>
          <p><strong>Role:</strong> {target.role}</p>
          <p><strong>Trust:</strong> {target.trustScore}</p>
          <p><strong>Score:</strong> {target.score}</p>
          <p><strong>Cost:</strong> ${target.costUsd}</p>
          <p><strong>Latency:</strong> {target.latencySeconds}s</p>
          <p><strong>Tokens:</strong> {target.tokens}</p>
          <p><strong>Weak Link:</strong> {String(target.weakLink)}</p>
          <p><strong>Input:</strong> {target.lastInput}</p>
          <p><strong>Output:</strong> {target.lastOutput}</p>
          <h3>Task Scores</h3>
          {taskScores.filter((score) => score.agent === target.id).map((score) => (
            <div key={`${score.taskId}-${score.agent}`} style={cardStyle}>
              <div><strong>Task:</strong> {score.taskId}</div>
              <div><strong>Score:</strong> {score.score}</div>
              <div><strong>Passed:</strong> {String(score.passed)}</div>
            </div>
          ))}
        </>
      )}

      {target?.kind === 'loop' && (
        <>
          <h2>Loop Event</h2>
          <p><strong>From:</strong> {target.source}</p>
          <p><strong>To:</strong> {target.target}</p>
          <p><strong>Reason:</strong> {target.label}</p>
          <p><strong>Iterations:</strong> {target.iterations}</p>
          <p><strong>Cost:</strong> ${target.costUsd}</p>
          <p><strong>Latency:</strong> {target.latencySeconds}s</p>
          <p><strong>Improved Score:</strong> {String(target.improvedScore)}</p>
        </>
      )}

      {target?.kind === 'handoff' && (
        <>
          <h2>Handoff Event</h2>
          <p><strong>From:</strong> {target.source}</p>
          <p><strong>To:</strong> {target.target}</p>
          <p><strong>Passed Value:</strong> {target.label}</p>
          <p><strong>Handoff Score:</strong> {target.score}</p>
        </>
      )}
    </aside>
  );
}

function LogsTable({ onSelectLog }: { onSelectLog: (log: any) => void }) {
  return (
    <div style={logsStyle}>
      <h3>Execution Logs</h3>
      <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 13 }}>
        <thead>
          <tr>
            <th style={thStyle}>Time</th>
            <th style={thStyle}>Type</th>
            <th style={thStyle}>Event</th>
            <th style={thStyle}>Score</th>
          </tr>
        </thead>
        <tbody>
          {executionLogs.map((log) => (
            <tr key={log.id} onClick={() => onSelectLog(log)} style={{ cursor: 'pointer' }}>
              <td style={tdStyle}>{log.time}</td>
              <td style={tdStyle}>{log.type}</td>
              <td style={tdStyle}>{log.message}</td>
              <td style={tdStyle}>{log.score}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

const panelStyle: React.CSSProperties = { width: 380, padding: 20, borderLeft: '1px solid #e5e7eb', background: '#ffffff', overflow: 'auto' };
const cardStyle: React.CSSProperties = { border: '1px solid #e5e7eb', borderRadius: 8, padding: 10, marginBottom: 10, background: '#f9fafb' };
const logsStyle: React.CSSProperties = { height: 220, borderTop: '1px solid #e5e7eb', background: '#fff', padding: '12px 16px', overflow: 'auto' };
const thStyle: React.CSSProperties = { textAlign: 'left', borderBottom: '1px solid #e5e7eb', padding: 8 };
const tdStyle: React.CSSProperties = { borderBottom: '1px solid #f3f4f6', padding: 8 };

export default function App() {
  const [selected, setSelected] = useState<any>(null);
  const flowNodes = useMemo(() => nodes, []);
  const flowEdges = useMemo(() => edges, []);

  return (
    <div style={{ display: 'flex', width: '100vw', height: '100vh' }}>
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
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
        <LogsTable onSelectLog={(log) => setSelected({ event: log })} />
      </div>
      <DetailPanel selected={selected} />
    </div>
  );
}
