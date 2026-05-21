import React from 'react';
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';

const nodes = [
  {
    id: 'benchmark',
    position: { x: 100, y: 100 },
    data: { label: 'Benchmark Suite' },
    type: 'default',
  },
  {
    id: 'agent',
    position: { x: 400, y: 100 },
    data: { label: 'AI Agent' },
    type: 'default',
  },
  {
    id: 'grader',
    position: { x: 700, y: 100 },
    data: { label: 'Execution Grader' },
    type: 'default',
  },
  {
    id: 'metrics',
    position: { x: 1000, y: 100 },
    data: { label: 'CLEAR Metrics' },
    type: 'default',
  },
  {
    id: 'traces',
    position: { x: 700, y: 300 },
    data: { label: 'Trace Collector' },
    type: 'default',
  },
  {
    id: 'report',
    position: { x: 1000, y: 300 },
    data: { label: 'Reports & Dashboard' },
    type: 'default',
  },
];

const edges = [
  {
    id: 'e1',
    source: 'benchmark',
    target: 'agent',
  },
  {
    id: 'e2',
    source: 'agent',
    target: 'grader',
  },
  {
    id: 'e3',
    source: 'grader',
    target: 'metrics',
  },
  {
    id: 'e4',
    source: 'agent',
    target: 'traces',
  },
  {
    id: 'e5',
    source: 'metrics',
    target: 'report',
  },
  {
    id: 'e6',
    source: 'traces',
    target: 'report',
  },
];

export default function App() {
  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      <ReactFlow nodes={nodes} edges={edges} fitView>
        <Background />
        <MiniMap />
        <Controls />
      </ReactFlow>
    </div>
  );
}
