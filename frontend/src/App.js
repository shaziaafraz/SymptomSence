import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Prediction from './pages/Prediction';
import TeleSupport from './pages/TeleSupport';
import Navbar from './components/Navbar';
import Footer from './components/Footer';

function App() {
  return (
    <div className="app">
      <Navbar />
      <main className="container">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/prediction" element={<Prediction />} />
          <Route path="/tele-support" element={<TeleSupport />} />
        </Routes>
      </main>
      <Footer />
    </div>
  );
}

export default App;
