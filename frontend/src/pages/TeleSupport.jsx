import React, { useState } from "react";
import InputField from "../components/InputField";
import Button from "../components/Button";

export default function TeleSupport() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [status, setStatus] = useState(""); // success message
  const [error, setError] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    setStatus("");
    setError("");

    if (!email.trim()) {
      setError("Please enter your email.");
      return;
    }

    if (!message.trim()) {
      setError("Please enter your message.");
      return;
    }

    // Simulated success (since no backend is attached)
    setTimeout(() => {
      setStatus("Message sent successfully. Our team will reach you soon.");
      setEmail("");
      setMessage("");
    }, 500);
  }

  return (
    <section className="page container-grid">

      <div className="support-card">
        <h2>Tele Support</h2>

        <form onSubmit={handleSubmit} className="form-stack">

          <InputField
            label="Email"
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <label className="input-label">
            <div className="input-label-text">Message</div>
            <textarea
              className="input-field textarea"
              placeholder="Write your message here..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
            ></textarea>
          </label>

          {error && <div className="form-error">{error}</div>}
          {status && <div className="form-status">{status}</div>} 

          <div className="form-actions">
            <Button type="submit" className="btn-primary">
              Send
            </Button>
          </div>
        </form>
      </div>

    </section>
  );
}
