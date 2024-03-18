import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import ReactFlowLogic from './components/ReactFlowLogic';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/schema-mapping" element={<ReactFlowLogic />} />
        {/* Add other nested routes here */}
      </Routes>
    </Router>
  );
};

export default App;