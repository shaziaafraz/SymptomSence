import React from 'react';
import { Link, useLocation } from 'react-router-dom';

export default function Navbar() {
  const loc = useLocation();
  return (
    <header className="navbar">
      <div className="nav-inner container-grid">
        <div className="logo">
          <div className="logo-mark">🩺</div>
          <Link to="/" className="logo-text">SymptomSence</Link>
        </div>

        <nav className="nav-links">
          <Link className={loc.pathname==='/'? 'active':''} to="/">Home</Link>
          <Link className={loc.pathname==='/prediction'? 'active':''} to="/prediction">Prediction</Link>
          <Link className={loc.pathname==='/tele-support'? 'active':''} to="/tele-support">Tele-Support</Link>
        </nav>

        <div className="nav-cta">
          <Link to="/prediction" className="btn btn-primary">Predict Disease</Link>
        </div>
      </div>
    </header>
  );
}
