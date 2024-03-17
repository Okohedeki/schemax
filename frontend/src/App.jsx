import React, { useCallback } from 'react';
import ReactFlow, {
  addEdge,
  ConnectionLineType,
  Panel,
  useNodesState,
  useEdgesState,
} from 'reactflow';
import dagre from 'dagre';

import 'reactflow/dist/style.css';

const initialNodes = [{ 'id': 'Employees', 'type': 'table_node', 'data': { 'label': 'Employees' } },
{ 'id': 'Categories', 'type': 'table_node', 'data': { 'label': 'Categories' } },
{ 'id': 'Customers', 'type': 'table_node', 'data': { 'label': 'Customers' } },
{ 'id': 'Shippers', 'type': 'table_node', 'data': { 'label': 'Shippers' } },
{ 'id': 'Suppliers', 'type': 'table_node', 'data': { 'label': 'Suppliers' } },
{ 'id': 'Orders', 'type': 'table_node', 'data': { 'label': 'Orders' } },
{ 'id': 'Products', 'type': 'table_node', 'data': { 'label': 'Products' } },
{ 'id': 'Order Details', 'type': 'table_node', 'data': { 'label': 'Order Details' } },
{ 'id': 'CustomerCustomerDemo', 'type': 'table_node', 'data': { 'label': 'CustomerCustomerDemo' } },
{ 'id': 'CustomerDemographics', 'type': 'table_node', 'data': { 'label': 'CustomerDemographics' } },
{ 'id': 'Region', 'type': 'table_node', 'data': { 'label': 'Region' } },
{ 'id': 'Territories', 'type': 'table_node', 'data': { 'label': 'Territories' } },
{ 'id': 'EmployeeTerritories', 'type': 'table_node', 'data': { 'label': 'EmployeeTerritories' } },
{ 'id': 'trigger_trg_TestNoOp', 'type': 'trigger_node', 'data': { 'label': 'trg_TestNoOp' } },
{ 'id': 'trigger_trgAfterInsert', 'type': 'trigger_node', 'data': { 'label': 'trgAfterInsert' } },
{ 'id': 'trigger_nan', 'type': 'trigger_node', 'data': { 'label': 'None' } }];

const initialEdges = [{'id': 'Employees_trg_TestNoOp', 'source': 'Employees', 'target': 'trigger_trg_TestNoOp', 'type': 'edge_type', 'data': {'label': ''}}, 
{'id': 'Employees_trgAfterInsert', 'source': 'Employees', 'target': 'trigger_trgAfterInsert', 'type': 'edge_type', 'data': {'label': ''}}, 
{'id': 'Categories_nan', 'source': 'Categories', 'target': 'trigger_nan', 'type': 'edge_type', 'data': {'label': ''}},
 {'id': 'Customers_nan', 'source': 'Customers', 'target': 'trigger_nan', 'type': 'edge_type', 'data': {'label': ''}}, 
 {'id': 'Shippers_nan', 'source': 'Shippers', 'target': 'trigger_nan', 'type': 'edge_type', 'data': {'label': ''}}, 
 {'id': 'Suppliers_nan', 'source': 'Suppliers', 'target': 'trigger_nan', 'type': 'edge_type', 'data': {'label': ''}},
  {'id': 'Orders_nan', 'source': 'Orders', 'target': 'trigger_nan', 'type': 'edge_type', 'data': {'label': ''}}, 
  {'id': 'Products_nan', 'source': 'Products', 'target': 'trigger_nan', 'type': 'edge_type', 'data': {'label': ''}}, 
  {'id': 'Order Details_nan', 'source': 'Order Details', 'target': 'trigger_nan', 'type': 'edge_type', 'data': {'label': ''}}, 
  {'id': 'CustomerCustomerDemo_nan', 'source': 'CustomerCustomerDemo', 'target': 'trigger_nan', 'type': 'edge_type', 'data': {'label': ''}}, {'id': 'CustomerDemographics_nan', 'source': 'CustomerDemographics', 'target': 'trigger_nan', 'type': 'edge_type', 'data': {'label': ''}}, {'id': 'Region_nan', 'source': 'Region', 'target': 'trigger_nan', 'type': 'edge_type', 'data': {'label': ''}}, {'id': 'Territories_nan', 'source': 'Territories', 'target': 'trigger_nan', 'type': 'edge_type', 'data': {'label': ''}}, {'id': 'EmployeeTerritories_nan', 'source': 'EmployeeTerritories', 'target': 'trigger_nan', 'type': 'edge_type', 'data': {'label': ''}}]

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
    initialNodes,
    initialEdges
  );
  
  const LayoutFlow = () => {
    const [nodes, setNodes, onNodesChange] = useNodesState(layoutedNodes);
    const [edges, setEdges, onEdgesChange] = useEdgesState(layoutedEdges);
  
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
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
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
  
export default function App() {
  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      <ReactFlow nodes={initialNodes} edges={initialEdges} />
    </div>
  );
}