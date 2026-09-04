import { Navigate, useNavigate } from "react-router-dom";
import { useAnalysis } from "../context/AnalysisContext";

function Results() {
  const navigate = useNavigate();
  const { analysis, result } = useAnalysis();
  if (!analysis || !result) return <Navigate to="/analyze" replace />;
  const { assessment, safety_plan: safetyPlan, escalation_timeline: timeline = [] } = result;
  return <div className="page results-page"><div className="analysis-container">
    <div className="analysis-header"><span className="soft-badge">Your SafeSphere results</span><h1>Interaction overview</h1><p>{analysis.summary || "Here is a calm overview of the patterns found in this interaction."}</p></div>
    <div className={`question-card level-card level-${assessment.level.toLowerCase()}`}><h3>Overall concern level</h3><strong>{assessment.level}</strong><p>Risk score: {assessment.score} / 100</p></div>
    <section className="question-card"><h3>Risk breakdown</h3>{assessment.breakdown.length ? <ul>{assessment.breakdown.map((item, index) => <li key={`${item.indicator}-${index}`}>{item.indicator.replaceAll("_", " ")}: +{item.points} points</li>)}</ul> : <p>No additional risk points were added.</p>}</section>
    <section className="question-card"><h3>Detected indicators</h3>{analysis.indicators.length ? <div className="data-list">{analysis.indicators.map((indicator) => <div key={indicator.name}><strong>{indicator.name.replaceAll("_", " ")}</strong> <span>Severity {indicator.severity}/3</span>{indicator.evidence && <p>“{indicator.evidence}”</p>}</div>)}</div> : <p>No concerning patterns were identified from the text provided.</p>}</section>
    <section className="question-card"><h3>Escalation timeline</h3>{timeline.length ? <div className="timeline">{timeline.map((item) => <div className="timeline-item" key={item.indicator}><strong>Stage {item.stage}: {item.label}</strong><p>{item.description}</p>{item.evidence && <small>Evidence: “{item.evidence}”</small>}</div>)}</div> : <p>No escalation timeline was generated.</p>}</section>
    <section className="question-card"><h3>Safer next steps</h3><p>{safetyPlan?.message}</p><ol>{safetyPlan?.steps?.map((step) => <li key={step}>{step}</li>)}</ol><p className="guidance-note">This guidance can help you reflect on the interaction; it is not an absolute prediction.</p></section>
    <button className="start-button" onClick={() => navigate("/safety-plan")}>Open safety plan</button><button className="choice" onClick={() => navigate("/vault")}>Open evidence vault</button>
  </div></div>;
}
export default Results;
