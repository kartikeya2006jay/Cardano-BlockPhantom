// src/App.js
import React, { useState } from "react";
import axios from "axios";
import "./App.css";

// --- MUST MATCH .env (React CRA) ---
const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:8000";

export default function App() {
  const [chain, setChain] = useState("cardano");
  const [address, setAddress] = useState("");
  const [risk, setRisk] = useState(null);
  const [txs, setTxs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [useDemo, setUseDemo] = useState(false);

  // Real working sample addresses
  const demoAddresses = {
    ethereum: "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
    cardano:
      "addr1q9jx0gxyjz5sx4gmwgu3z2hdqq67dnw2h9xmc8k45td90vlpukr79dc4w22lv7yumwnz0mn4048322vhm4d9p3cpv9cswhrz06",
  };

  // -------------------------------
  // MAIN FETCH FUNCTION
  // -------------------------------
  async function analyze(demoFlag, detectedChain, detectedAddress) {
    setError("");
    setRisk(null);
    setTxs([]);
    setLoading(true);

    try {
      const query = demoFlag ? "?demo=true" : "";
      const encoded = encodeURIComponent(detectedAddress.trim());

      const riskURL = `${API_BASE}/wallet/${detectedChain}/${encoded}/risk${query}`;
      const histURL = `${API_BASE}/wallet/${detectedChain}/${encoded}/history${query}`;

      console.log("Calling risk:", riskURL);

      const [riskResp, histResp] = await Promise.all([
        axios.get(riskURL),
        axios.get(histURL),
      ]);

      setRisk(riskResp.data);
      setTxs(histResp.data.transactions || []);
    } catch (err) {
      console.error("Error:", err);
      setError("Could not fetch data. Check API_BASE or backend status.");
    } finally {
      setLoading(false);
    }
  }

  // -------------------------------
  // AUTO-DETECT + MAIN ACTION
  // -------------------------------
  const analyzeClicked = async () => {
    const addr = address.trim();

    // DEMO MODE
    if (!addr && useDemo) {
      const demoAddr = demoAddresses[chain];
      setAddress(demoAddr);
      await analyze(true, chain, demoAddr);
      return;
    }

    if (!addr) {
      setError("Enter a wallet address.");
      return;
    }

    // AUTO-DETECT REAL CHAIN
    let detectedChain = chain;

    if (addr.startsWith("0x")) {
      detectedChain = "ethereum";
      setChain("ethereum");
    }

    // Valid Cardano patterns only
    if (addr.startsWith("addr1") || addr.startsWith("addr_test1")) {
      detectedChain = "cardano";
      setChain("cardano");
    }

    // ---- LIVE MODE ----
    await analyze(false, detectedChain, addr);

    // ---- AUTO-DEMO fallback if needed ----
    setTimeout(async () => {
      if (useDemo && (txs.length === 0 || (risk && risk.score === 0))) {
        const demoAddr = demoAddresses[detectedChain];
        setAddress(demoAddr);
        await analyze(true, detectedChain, demoAddr);
      }
    }, 300);
  };

  const downloadPDF = () => {
    const q = useDemo ? "?demo=true" : "";
    const encoded = encodeURIComponent(address.trim());
    window.open(`${API_BASE}/wallet/${chain}/${encoded}/pdf${q}`, "_blank");
  };

  return (
    <div className="page">
      <header className="header">
        <div className="brand">
          <div className="logo">🛡️</div>
          <div className="brand-name">BlockPhantom</div>
        </div>
      </header>

      <main className="main">
        <h1>Web3 Risk Intelligence</h1>
        <p className="subtitle">Analyze ETH & ADA wallets with advanced scoring.</p>

        <div className="analyze-card">
          <div className="chains">
            <button
              className={chain === "ethereum" ? "active" : ""}
              onClick={() => setChain("ethereum")}
            >
              Ethereum
            </button>

            <button
              className={chain === "cardano" ? "active" : ""}
              onClick={() => setChain("cardano")}
            >
              Cardano
            </button>
          </div>

          <div className="input-row">
            <input
              value={address}
              onChange={(e) => setAddress(e.target.value)}
              placeholder="Wallet address (0x... or addr1...)"
            />
            <button className="primary" onClick={analyzeClicked} disabled={loading}>
              {loading ? "Analyzing..." : "Analyze"}
            </button>
          </div>

          <div className="controls">
            <label>
              <input
                type="checkbox"
                checked={useDemo}
                onChange={(e) => setUseDemo(e.target.checked)}
              />{" "}
              Use Demo fallback
            </label>

            <div className="demo-buttons">
              <button
                onClick={() => {
                  setChain("ethereum");
                  setAddress(demoAddresses.ethereum);
                }}
              >
                ETH Demo
              </button>
              <button
                onClick={() => {
                  setChain("cardano");
                  setAddress(demoAddresses.cardano);
                }}
              >
                ADA Demo
              </button>
            </div>
          </div>

          {error && <div className="error">{error}</div>}
        </div>

        {risk && (
          <section className="results">
            <div className="left">
              <div className="score">{risk.score}</div>
              <div className="label">Risk Score</div>
            </div>

            <div className="right">
              <div><strong>Probability:</strong> {risk.probability}</div>
              <div><strong>Level:</strong> {risk.level}</div>
              <div><strong>Tx Count:</strong> {risk.details?.count}</div>
              {risk.demo && <div className="demo-badge">DEMO DATA</div>}

              <button className="pdf" onClick={downloadPDF}>
                Download PDF
              </button>
            </div>

            <div className="breakdown">
              <h3>Breakdown</h3>
              <div className="stats">
                <div className="stat">
                  <div className="label">Average</div>
                  <div className="value">{Number(risk.details?.avg).toPrecision(4)}</div>
                </div>
                <div className="stat">
                  <div className="label">Std Dev</div>
                  <div className="value">{Number(risk.details?.std).toPrecision(4)}</div>
                </div>
                <div className="stat">
                  <div className="label">Count</div>
                  <div className="value">{risk.details?.count}</div>
                </div>
              </div>
            </div>

            <div className="tx-list">
              <h3>Recent Transactions</h3>

              {txs.length === 0 ? (
                <div className="muted">No transactions</div>
              ) : (
                txs.slice(0, 8).map((t, i) => <pre key={i}>{JSON.stringify(t, null, 2)}</pre>)
              )}
            </div>
          </section>
        )}
      </main>

      <footer className="footer">© 2025 BlockPhantom</footer>
    </div>
  );
}
