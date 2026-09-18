import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './components/Dashboard';

function Home() {
  return (
    <div className="container min-vh-100 d-flex flex-column justify-content-center align-items-center text-center">
      <h1 className="display-4 fw-bold text-primary mb-3">Darukaa.Earth</h1>
      <p className="lead text-secondary w-75">
        Geospatial Carbon & Biodiversity Project Management Platform
      </p>
      <div className="mt-4 p-4 bg-light rounded shadow-sm border">
        <h5 className="text-muted">Phase 1-4 Foundation Complete</h5>
        <div className="mt-3">
          {/* For Hackathon demo purposes, linking directly to a generic project UUID */}
          <Link to="/projects/11111111-1111-1111-1111-111111111111" className="btn btn-primary">Open Sample Project Dashboard</Link>
        </div>
      </div>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <nav className="navbar navbar-dark bg-dark px-3">
        <span className="navbar-brand mb-0 h1"><Link to="/" className="text-white text-decoration-none">Darukaa.Earth</Link></span>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/projects/:projectId" element={<Dashboard />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
