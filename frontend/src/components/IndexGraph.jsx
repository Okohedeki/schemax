// Diagram2.jsx
import React from 'react';
import ReactFlow, {
    addEdge,
    ConnectionLineType,
    Panel,
    ReactFlowProvider,
  } from 'reactflow';

  const IndexGraph = () => {
    // Fake nodes for IndexGraph
    const nodes = [
      { id: '1', type: 'input', data: { label: 'Input Node' }, position: { x: 250, y: 5 } },
      { id: '2', data: { label: 'Node 2' }, position: { x: 100, y: 100 } }
    ];
  
    // Fake edges for IndexGraph
    const fakeEdges = [
      { id: 'e1-2', source: '1', target: '2', type: 'step', animated: true, label: 'Edge 1 to 2' },
      // Add more fake edges here if needed
    ];
  
    // Return the ReactFlow component with nodes and edges
    return <ReactFlow elements={nodes.concat(fakeEdges)} connectionLineType={ConnectionLineType.SmoothStep} />;
  };
  
  export default IndexGraph;