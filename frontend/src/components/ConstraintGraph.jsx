import React from 'react';
import ReactFlow, {
  ConnectionLineType,
} from 'reactflow';

const ConstraintGraph = () => {
  // Fake nodes for Diagram 3
  const nodes = [
    { id: 'B', data: { label: 'Node B' }, position: { x: 100, y: 100 } },
    { id: 'C', data: { label: 'Node C' }, position: { x: 400, y: 100 } },
  ];

  // Fake edges for Diagram 3
  const fakeEdges = [
    { id: 'eB-C', source: 'B', target: 'C', type: 'step', animated: true, label: 'Edge B to C' },
    // Add more fake edges here if needed
  ];

  // Combine nodes and edges
  const elements = [...nodes, ...fakeEdges];

  // Return the ReactFlow component with nodes and edges
  return (
    <ReactFlow
      elements={elements}
      connectionLineType={ConnectionLineType.SmoothStep}
      style={{ width: '100%', height: '100%' }}
    />
  );
};

export default ConstraintGraph;
