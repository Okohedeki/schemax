import React, { useState, useEffect, useCallback } from 'react';
import ReactFlow, {
  addEdge,
  ConnectionLineType,
  Panel,
  ReactFlowProvider,
} from 'reactflow';
import dagre from 'dagre';

import 'reactflow/dist/style.css';

const ConstraintGraph = ({ initialNodes, initialEdges }) => {
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);

  useEffect(() => {
    // Fetch data from backend route
    fetch('http://localhost:5000/getReactFlowData')
      .then(response => response.json())
      .then(data => {
        // Extract nodes and edges from the data
        const { nodes, edges } = data;

        // Set nodes and edges state
        setNodes(nodes);
        setEdges(edges);
      })
      .catch(error => console.error('Error fetching data:', error));
  }, []); // Empty dependency array ensures this effect runs only once

  const dagreGraph = new dagre.graphlib.Graph();
  dagreGraph.setDefaultEdgeLabel(() => ({}));
  
  const nodeWidth = 172;
  const nodeHeight = 36;
  
  const getLayoutedElements = (nodes, edges, direction = 'TB') => {
    const isHorizontal = direction === 'LR';
    dagreGraph.setGraph({ rankdir: direction });
  
    nodes.forEach((node) => {
      dagreGraph.setNode(node.id, { width: nodeWidth, height: nodeHeight });
    });
  
    edges.forEach((edge) => {
      dagreGraph.setEdge(edge.source, edge.target);
    });
  
    dagre.layout(dagreGraph);
  
    nodes.forEach((node) => {
      const nodeWithPosition = dagreGraph.node(node.id);
      node.targetPosition = isHorizontal ? 'left' : 'top';
      node.sourcePosition = isHorizontal ? 'right' : 'bottom';
  
      // We are shifting the dagre node position (anchor=center center) to the top left
      // so it matches the React Flow node anchor point (top left).
      node.position = {
        x: nodeWithPosition.x - nodeWidth / 2,
        y: nodeWithPosition.y - nodeHeight / 2,
      };
  
      return node;
    });
  
    return { nodes, edges };
  };
  
  const { nodes: layoutedNodes, edges: layoutedEdges } = getLayoutedElements(
    nodes,
    edges
  );
  
  const LayoutFlow = () => {
    const onConnect = useCallback(
      (params) =>
        setEdges((eds) =>
          addEdge({ ...params, type: ConnectionLineType.SmoothStep, animated: true }, eds)
        ),
      []
    );
    const onLayout = useCallback(
      (direction) => {
        const { nodes: layoutedNodes, edges: layoutedEdges } = getLayoutedElements(
          nodes,
          edges,
          direction
        );
  
        setNodes([...layoutedNodes]);
        setEdges([...layoutedEdges]);
      },
      [nodes, edges]
    );
  
    return (
      <ReactFlow
        nodes={layoutedNodes}
        edges={layoutedEdges}
        onConnect={onConnect}
        connectionLineType={ConnectionLineType.SmoothStep}
        fitView
      >
        <Panel position="top-right">
          <button onClick={() => onLayout('TB')}>vertical layout</button>
          <button onClick={() => onLayout('LR')}>horizontal layout</button>
        </Panel>
      </ReactFlow>
    );
  };
  
  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      <ReactFlowProvider>
        <LayoutFlow />
      </ReactFlowProvider>
    </div>
  );
}

export default ConstraintGraph;
