import React, { useState, useEffect } from 'react';
import ReactFlowLayout from './ReactFlowLogic';

const App = () => {
  // You can keep your initialNodes and initialEdges state here
  
  return (
    <div style={{ display: 'flex', height: '100vh' }}>
      <div style={{ width: '20%', background: '#f0f0f0' }}>
        <ul>
          <li>Schema Mapping</li>
          <li>Data Dictionary</li>
          <li>Large Language Model</li>
          <li>Connections</li>
        </ul>
      </div>
      <div style={{ flex: 1 }}>
        <ReactFlowLayout />
      </div>
    </div>
  );
};

export default App;
