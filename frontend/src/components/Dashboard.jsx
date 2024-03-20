import React, { useState } from 'react';
import ReactFlowLogic from './ReactFlowLogic';
import ConstraintGraph from './ConstraintGraph';
import IndexGraph from './IndexGraph';
import Connections from './Connections';
import DataDictionary from './DataDictionary';
import LargeLanguageModel from './LargeLanguageModel';

const Dashboard = () => {
  const [activeComponent, setActiveComponent] = useState('ReactFlowLogic');
  const [showButtons, setShowButtons] = useState(false);

  const renderComponent = () => {
    switch (activeComponent) {
      case 'ReactFlowLogic':
        return <ReactFlowLogic />;
      case 'ConstraintGraph':
        return <ConstraintGraph />;
      case 'IndexGraph':
        return <IndexGraph />;
      case 'Connections':
        return <Connections />;
      case 'DataDictionary':
        return <DataDictionary />;
      case 'LargeLanguageModel':
        return <LargeLanguageModel />;
      default:
        return null;
    }
  };

  const renderButtons = () => {
    if (!showButtons) return null;

    return (
      <div style={{ display: 'flex', justifyContent: 'center', padding: '1rem' }}>
        <button onClick={() => setActiveComponent('ReactFlowLogic')} style={{ marginRight: '1rem' }}>ReactFlowLogic</button>
        <button onClick={() => setActiveComponent('ConstraintGraph')} style={{ marginRight: '1rem' }}>Constraint Graph</button>
        <button onClick={() => setActiveComponent('IndexGraph')} style={{ marginRight: '1rem' }}>Index Graph</button>
      </div>
    );
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
      {/* Header */}
      <header style={{ backgroundColor: '#333', color: '#fff', padding: '1rem', textAlign: 'center' }}>
        <h1>Schemax</h1>
      </header>

      {/* Schema Mapping Section */}
      <div style={{ flex: 1 }}>
        <div style={{ display: 'flex', height: '100%' }}>
          <div style={{ width: '20%', background: '#f0f0f0' }}>
            <ul>
              <li style={{ cursor: 'pointer' }} onClick={() => setShowButtons(true)}>Schema Mapping</li>
              <li style={{ cursor: 'pointer' }} onClick={() => setActiveComponent('Connections')}>Connections</li>
            </ul>
          </div>
          <div style={{ flex: 1 }}>
            {showButtons && renderButtons()}
            {renderComponent()}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
