import React, { useState } from 'react';
import client from '../api/client';
import InputField from '../components/InputField';
import Button from '../components/Button';
import ResultCard from '../components/ResultCard';

export default function Prediction() {
  const [symptom, setSymptom] = useState('');
  const [age, setAge] = useState('');
  const [gender, setGender] = useState(''); // empty by default
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  async function handlePredict(e) {
    e.preventDefault();
    setError('');
    setResult(null);

    if (!symptom.trim()) {
      setError("Please enter symptoms.");
      return;
    }

    if (!gender) {
      setError("Please select gender.");
      return;
    }

    setLoading(true);

    try {
      // FIXED: backend expects "symptoms"
      const payload = { symptoms: symptom, age, gender };

      const res = await client.post("/predict", payload);

      // Backend returns: { results: [...] }
      setResult(res.data.results);
    } catch (err) {
      console.error(err);
      setError(err?.response?.data?.error || "Prediction failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="page container-grid">
      <div className="form-card">
        <h2>Disease Prediction Based on Symptoms</h2>

        <form onSubmit={handlePredict} className="form-stack">

          <InputField
            label="Symptoms"
            value={symptom}
            onChange={(e) => setSymptom(e.target.value)}
            placeholder="e.g., fever, headache, fatigue"
          />

          <InputField
            label="Age"
            type="number"
            value={age}
            onChange={(e) => setAge(e.target.value)}
            placeholder="Age"
          />

          {/* Gender Dropdown */}
          <label className="input-label">
            <div className="input-label-text">Gender</div>
            <select
              className="input-field"
              value={gender}
              onChange={(e) => setGender(e.target.value)}
            >
              <option value="">Select gender</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Other">Other</option>
            </select>
          </label>

          {error && <div className="form-error">{error}</div>}

          <div className="form-actions">
            <Button type="submit" className="btn-primary">
              {loading ? "Predicting..." : "Predict"}
            </Button>

            <Button
              type="button"
              className="btn-ghost"
              onClick={() => {
                setSymptom('');
                setAge('');
                setGender('');
                setResult(null);
                setError('');
              }}
            >
              Reset
            </Button>
          </div>
        </form>
      </div>

      <div className="result-area">
        {loading && <div className="loader">Loading...</div>}

        {/* DISPLAY ALL 3 RESULTS */}
        {result &&
          result.map((item, idx) => (
            <ResultCard key={idx} data={item} />
          ))}
      </div>
    </section>
  );
}
