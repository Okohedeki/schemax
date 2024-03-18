import React, { useState } from 'react';
import ReactFlowLogic from './ReactFlowLogic';
import DataDictionary from './DataDictionary';
import LargeLanguageModel from './LargeLanguageModel';
import Connections from './Connections';

const Dashboard = () => {
  const [activeComponent, setActiveComponent] = useState('ReactFlowLogic');

  const renderComponent = () => {
    switch (activeComponent) {
      case 'ReactFlowLogic':
        return <ReactFlowLogic />;
      case 'DataDictionary':
        return <DataDictionary />;
      case 'LargeLanguageModel':
        return <LargeLanguageModel />;
      case 'Connections':
        return <Connections />;
      default:
        return null;
    }
  };

  return (
    <div style={{ display: 'flex', height: '100vh' }}>
      <div style={{ width: '20%', background: '#f0f0f0' }}>
        <ul>
          <li onClick={() => setActiveComponent('ReactFlowLogic')}>Schema Mapping</li>
          <li onClick={() => setActiveComponent('DataDictionary')}>Data Dictionary</li>
          <li onClick={() => setActiveComponent('LargeLanguageModel')}>Large Language Model</li>
          <li onClick={() => setActiveComponent('Connections')}>Connections</li>
        </ul>
      </div>
      <div style={{ flex: 1 }}>
        {renderComponent()}
      </div>
    </div>
  );
};

export default Dashboard;