import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getVaultCase, getVaultCases } from "../services/api";

function Vault() {
  const navigate = useNavigate();
  const [cases, setCases] = useState([]);
  const [selectedCase, setSelectedCase] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [detailLoading, setDetailLoading] = useState(false);

  useEffect(() => { (async () => {
    try { const response = await getVaultCases(); setCases(response.cases || []); }
    catch { setError("Unable to load your saved cases."); }
    finally { setLoading(false); }
  })(); }, []);

  const openCase = async (id) => {
    setDetailLoading(true); setError("");
    try { const response = await getVaultCase(id); setSelectedCase(response.case); }
    catch { setError("Unable to load this saved case."); }
    finally { setDetailLoading(false); }
  };
  const formatDate = (date) => date ? new Date(date).toLocaleString() : "Date unavailable";

  return <div className="page vault-page"><div className="analysis-container">
    <div className="analysis-header"><span className="soft-badge">Your evidence vault</span><h1>Saved assessments</h1><p>Only assessment details saved by SafeSphere are shown here.</p></div>
    {error && <p className="form-error" role="alert">{error}</p>}
    <div className="question-card"><h3>Previous cases</h3>{loading ? <p>Loading saved cases...</p> : cases.length === 0 ? <p>No saved cases yet. Complete an assessment to see it here.</p> : <div className="vault-list">{cases.map((item) => <button className="vault-case" key={item.id} onClick={() => openCase(item.id)}><strong>{item.case_name || "SafeSphere Analysis"}</strong><span>{item.concern_level} · {item.risk_score}/100</span><small>{formatDate(item.created_at)}</small></button>)}</div>}</div>
    {(detailLoading || selectedCase) && <div className="question-card case-details-card"><h3>Case details</h3>{detailLoading ? <p>Loading case details...</p> : <><p>{selectedCase.summary}</p><p><strong>{selectedCase.concern_level}</strong> · {selectedCase.risk_score}/100</p><h4>Indicators</h4><ul>{selectedCase.indicators?.map((item) => <li key={item.name}>{item.name.replaceAll("_", " ")}{item.evidence ? `: ${item.evidence}` : ""}</li>)}</ul><h4>Safety plan</h4><p>{selectedCase.safety_plan?.message}</p><ol>{selectedCase.safety_plan?.steps?.map((step) => <li key={step}>{step}</li>)}</ol></>}</div>}
    <button className="start-button" onClick={() => navigate("/analyze")}>Analyze another interaction</button><button className="choice" onClick={() => navigate("/")}>Back to home</button>
  </div></div>;
}
export default Vault;
