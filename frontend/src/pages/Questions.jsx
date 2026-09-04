import { useState } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import { useAnalysis } from "../context/AnalysisContext";
import { assessRisk } from "../services/api";

const choices = [["yes", "Yes"], ["no", "No"], ["not_sure", "Not sure"]];

function Questions() {
  const navigate = useNavigate();
  const { analysis, answers, context, setAnswers, setContext, setResult } = useAnalysis();
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [contextAnswers, setContextAnswers] = useState({ known: "", repeated: "" });
  if (!analysis) return <Navigate to="/analyze" replace />;

  const setAnswer = (id, value) => setAnswers({ ...answers, [id]: value });
  const setContextAnswer = (field, value) => {
    setContextAnswers({ ...contextAnswers, [field]: value });
    if (field === "known") setContext({ ...context, unknown_sender: value === "no" });
    if (field === "repeated") setContext({ ...context, repeated_behavior: value === "yes" });
  };

  const submit = async () => {
    const unanswered = analysis.questions.filter((question) => !answers[question.id]);
    if (unanswered.length) {
      setError("Please answer each question, or choose Not sure.");
      return;
    }
    setError("");
    setIsLoading(true);
    const indicatorAnswers = Object.fromEntries(analysis.questions.map((question) => [
      question.indicator,
      answers[question.id] === "not_sure" ? "maybe" : answers[question.id],
    ]));
    try {
      const response = await assessRisk({
        indicators: analysis.indicators,
        context,
        answers: indicatorAnswers,
        summary: analysis.summary,
        case_name: `SafeSphere Analysis - ${new Date().toLocaleString()}`,
      });
      setResult(response);
      navigate("/results");
    } catch {
      setError("Unable to complete the assessment. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return <div className="page questions-page"><div className="analysis-container">
    <div className="analysis-header"><span className="soft-badge">A little more context</span><h1>A few questions</h1><p>Your answers help tailor the assessment. You can choose Not sure whenever needed.</p></div>
    {analysis.questions.map((question) => <div className="question-card" key={question.id}>
      <h3>{question.question}</h3><div className="choice-row">{choices.map(([value, label]) => <button key={value} className={answers[question.id] === value ? "choice active" : "choice"} onClick={() => setAnswer(question.id, value)}>{label}</button>)}</div>
    </div>)}
    <div className="question-card"><h3>Do you know this person personally?</h3><div className="choice-row">{choices.map(([value, label]) => <button key={value} className={contextAnswers.known === value ? "choice active" : "choice"} onClick={() => setContextAnswer("known", value)}>{label}</button>)}</div>
      <h3 className="context-question">Has this behavior happened repeatedly?</h3><div className="choice-row">{choices.map(([value, label]) => <button key={value} className={contextAnswers.repeated === value ? "choice active" : "choice"} onClick={() => setContextAnswer("repeated", value)}>{label}</button>)}</div>
    </div>
    {error && <p className="form-error" role="alert">{error}</p>}
    <button className="start-button" onClick={submit} disabled={isLoading}>{isLoading ? "Completing assessment..." : "View results"}</button>
  </div></div>;
}
export default Questions;
