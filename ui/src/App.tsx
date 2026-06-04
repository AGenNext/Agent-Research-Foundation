import React, { useEffect, useMemo, useState } from 'react';
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  Node,
  Edge,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import * as sampleData from './sampleData';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

type ClearBenchData = typeof sampleData;

function buildFlow(data: ClearBenchData) {
  const nodes: Node[] = data.agentNodes.map((agent: any, index: number) => ({
    id: agent.id,
    position: { x: 120 + index * 260, y: agent.weakLink ? 260 : 120 },
    data: {
      label: `${agent.label}\nScore: ${agent.score} • Trust: ${agent.trustScore}\nCost: $${agent.costUsd ?? 0} • ${agent.latencySeconds ?? 0}s\nTokens: ${agent.tokens ?? 0}\n${agent.weakLink ? 'WEAK LINK' : agent.status}`,
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

  const handoffEdges: Edge[] = data.handoffs.map((handoff: any) => ({
    id: handoff.id,
    source: handoff.source,
    target: handoff.target,
    label: `${handoff.label} • score ${handoff.score}`,
    data: { kind: 'handoff', ...handoff },
  }));

  const loopEdges: Edge[] = data.loops.map((loop: any) => ({
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

  return { nodes, edges: [...handoffEdges, ...loopEdges] };
}

function DetailPanel({ selected, data, nodes, edges }: { selected: any; data: ClearBenchData; nodes: Node[]; edges: Edge[] }) {
  function resolveTarget(log: any) {
    return (
      nodes.find((node) => node.id === log.targetId)?.data ||
      edges.find((edge) => edge.id === log.targetId)?.data ||
      null
    );
  }

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
          <p><strong>Cost:</strong> ${target.costUsd ?? 0}</p>
          <p><strong>Latency:</strong> {target.latencySeconds ?? 0}s</p>
          <p><strong>Tokens:</strong> {target.tokens ?? 0}</p>
          <p><strong>Weak Link:</strong> {String(target.weakLink)}</p>
          <p><strong>Input:</strong> {target.lastInput}</p>
          <p><strong>Output:</strong> {target.lastOutput}</p>
          <h3>Task Scores</h3>
          {data.taskScores.filter((score: any) => score.agent === target.id).map((score: any) => (
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

function LogsTable({ logs, onSelectLog }: { logs: any[]; onSelectLog: (log: any) => void }) {
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
          {logs.map((log) => (
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
  const [data, setData] = useState<ClearBenchData>(sampleData);
  const [source, setSource] = useState('local sample data');

  useEffect(() => {
    if (!API_BASE_URL) return;

    fetch(`${API_BASE_URL}/api/demo`)
      .then((response) => {
        if (!response.ok) throw new Error(`Backend returned ${response.status}`);
        return response.json();
      })
      .then((backendData) => {
        setData({ ...sampleData, ...backendData });
        setSource('backend API');
      })
      .catch(() => {
        setSource('local sample data');
      });
  }, []);

  const { nodes, edges } = useMemo(() => buildFlow(data), [data]);

  return (
    <div style={{ display: 'flex', width: '100vw', height: '100vh' }}>
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <div style={{ padding: '8px 16px', borderBottom: '1px solid #e5e7eb', background: '#fff' }}>
          Data source: <strong>{source}</strong>
        </div>
        <div style={{ flex: 1 }}>
          <ReactFlow
            nodes={nodes}
            edges={edges}
            fitView
            onNodeClick={(_, node) => setSelected(node.data)}
            onEdgeClick={(_, edge) => setSelected(edge.data)}
          >
            <Background />
            <MiniMap />
            <Controls />
          </ReactFlow>
        </div>
        <LogsTable logs={data.executionLogs} onSelectLog={(log) => setSelected({ event: log })} />
      </div>
      <DetailPanel selected={selected} data={data} nodes={nodes} edges={edges} />
    </div>
  );
}
