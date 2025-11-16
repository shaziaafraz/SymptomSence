import React from "react";

export default function ResultCard({ data }) {
  if (!data) return null;

  // Severity color mapping
  const severityColor = {
    High: "#d9534f",     // red
    Medium: "#f0ad4e",   // yellow
    Low: "#5cb85c"       // green
  }[data.severity] || "#5cb85c";

  return (
    <div className="result-card">
      <h3 className="result-title">{data.disease}</h3>

      <div className="result-item">
        <strong>Probability:</strong> {data.probability}
      </div>

      <div className="result-item severity-row">
        <strong>Severity:</strong>

        <span
          className="severity-badge"
          style={{
            color: severityColor,
            fontWeight: "700",
            fontSize: "20px",
            marginLeft: "8px"
          }}
        >
          {data.severity}
        </span>
      </div>

      <div className="result-item">
        <strong>Medication:</strong>
        <p>{data.medication}</p>
      </div>

      <div className="result-item">
        <strong>Recommendation:</strong>
        <p>{data.recommendation}</p>
      </div>

      <div className="result-item">
        <strong>Description:</strong>
        <p>{data.description}</p>
      </div>
    </div>
  );
}
