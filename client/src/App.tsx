import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { Dashboard } from './pages/DashboardWithAuth';
import ValuationWizard from './pages/ValuationWizard';

function App() {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/valuation" element={<ValuationWizard />} />
        </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;
