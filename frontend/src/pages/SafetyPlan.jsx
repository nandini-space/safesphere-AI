import { Navigate, useNavigate } from "react-router-dom";
import { useAnalysis } from "../context/AnalysisContext";

function SafetyPlan() {
  const navigate = useNavigate();
  const { result } = useAnalysis();
  if (!result?.safety_plan) return <Navigate to="/analyze" replace />;
  const plan = result.safety_plan;
  return <div className="page safety-page"><div className="analysis-container">
    <div className="analysis-header"><span className="soft-badge">Your safety plan</span><h1>Choose your next steps</h1><p>{plan.message}</p></div>
    <div className="question-card"><h3>Suggested actions</h3><ol className="safety-steps">{plan.steps?.map((step) => <li key={step}>{step}</li>)}</ol></div>
    <div className="privacy-note">Take your time. This is supportive guidance, and you can choose the steps that feel right for you.</div>
    <button className="start-button" onClick={() => navigate("/vault")}>Open evidence vault</button><button className="choice" onClick={() => navigate("/")}>Back to home</button>
  </div></div>;
}
export default SafetyPlan;
