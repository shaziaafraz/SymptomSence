import React from "react";
import "../styles/home.css";

export default function Home() {
  return (
    <section className="home-container">

      {/* Background Gradient */}
      <div className="bg-swirl"></div>

      <div className="home-inner">

        <div className="text-section">
          <h1 className="main-title">SymptomSense</h1>

          <h2 className="sub-title">
            AI Prediction of Diseases with Instant Medication and Explanation
          </h2>

          <p className="intro-text">
            SymptomSense delivers fast, accurate, and intelligent health predictions powered
            by advanced machine learning models. Designed to assist you in understanding your symptoms,
            it provides clarity, confidence, and guidance in real time.
          </p>

          <div className="why-card">
            <h3 className="why-heading">Why SymptomSense?</h3>

            <ul className="why-list">
              <li><strong>Fast Detection:</strong> Get instant predictions based on your symptoms.</li>
              <li><strong>High Accuracy:</strong> Trained using high-quality medical datasets.</li>
              <li><strong>Medication Guidance:</strong> Receive immediate treatment suggestions.</li>
              <li><strong>Clear Explanations:</strong> Understand every diagnosis with clarity.</li>
              <li><strong>Tele-Support:</strong> Connect to medical assistance effortlessly.</li>
            </ul>
          </div>
        </div>

      </div>
    </section>
  );
}
