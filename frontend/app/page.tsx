"use client";
import { useState } from "react";

export default function HomePage() {
  const [cgpa, setCgpa] = useState<string>("7.0");
  const [iq, setIq] = useState<string>("85");
  const [prediction, setPrediction] = useState<number | null>(null);
  const [training, setTraining] = useState<boolean>(false);
  const [metrics, setMetrics] = useState<string>("");
  const [error, setError] = useState<string>("");

  const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

  async function handlePredict(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setPrediction(null);
    try {
      const res = await fetch(`${API_BASE}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ cgpa: Number(cgpa), iq: Number(iq) }),
      });
      if (!res.ok) {
        const data = await res.json().catch(() => ({} as { detail?: string }));
        throw new Error(data.detail || `Request failed: ${res.status}`);
      }
      const data = (await res.json()) as { prediction: number };
      setPrediction(data.prediction);
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : String(err);
      setError(message);
    }
  }

  async function handleTrain() {
    setTraining(true);
    setError("");
    setMetrics("");
    try {
      const res = await fetch(`${API_BASE}/train`, { method: "POST" });
      if (!res.ok) {
        const data = await res.json().catch(() => ({} as { detail?: string }));
        throw new Error(data.detail || `Request failed: ${res.status}`);
      }
      const data = (await res.json()) as { message: string; metrics?: unknown };
      setMetrics(JSON.stringify(data.metrics || {}, null, 2));
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : String(err);
      setError(message);
    } finally {
      setTraining(false);
    }
  }

  return (
    <main className="container stack">
      <header className="stack">
        <h1>Placement Predictor</h1>
        <p className="muted">
          Train the model on the backend and run predictions using CGPA and IQ.
        </p>
      </header>

      <section className="card stack">
        <div className="row">
          <button className="btn primary" onClick={handleTrain} disabled={training}>
            {training ? "Training..." : "Train (default dataset)"}
          </button>
        </div>
        {metrics && (
          <pre
            style={{
              background: "transparent",
              border: "1px dashed var(--border)",
              padding: 12,
              borderRadius: 8,
              overflowX: "auto",
              maxHeight: 240,
            }}
          >
            {metrics}
          </pre>
        )}
      </section>

      <section className="card">
        <form onSubmit={handlePredict} className="stack">
          <div className="row">
            <label>
              CGPA
              <input
                className="input"
                type="number"
                step="0.1"
                value={cgpa}
                onChange={(e) => setCgpa(e.target.value)}
                style={{ marginLeft: 8 }}
              />
            </label>
          </div>
          <div className="row">
            <label>
              IQ
              <input
                className="input"
                type="number"
                step="1"
                value={iq}
                onChange={(e) => setIq(e.target.value)}
                style={{ marginLeft: 8 }}
              />
            </label>
          </div>
          <div className="row">
            <button className="btn" type="submit">Predict</button>
          </div>
        </form>

        {prediction !== null && (
          <p style={{ marginTop: 16 }}>
            Prediction: <strong>{prediction === 1 ? "Placed" : "Not Placed"}</strong>
          </p>
        )}
        {error && (
          <p style={{ marginTop: 16, color: "#b00020" }}>Error: {error}</p>
        )}
      </section>
    </main>
  );
}
