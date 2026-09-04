import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Questions() {
  const navigate = useNavigate();

  const [feeling, setFeeling] = useState("");

  const handleContinue = () => {
    if (!feeling) {
      alert("Please select an option before continuing.");
      return;
    }

    navigate("/results");
  };

  return (
    <div className="page">

      <div className="analysis-container">

        <div className="analysis-header">

          <span className="soft-badge">
            💜 A little more context
          </span>

          <h1>A Few Questions</h1>

          <p>
            Answer these questions to help SafeSphere
            understand the situation better.
          </p>

        </div>

        <div className="question-card">

          <h3>
            How did this interaction make you feel?
          </h3>

          <div className="choice-row">

            <button
              className={
                feeling === "Uncomfortable"
                  ? "choice active"
                  : "choice"
              }
              onClick={() => setFeeling("Uncomfortable")}
            >
              Uncomfortable
            </button>

            <button
              className={
                feeling === "Confused"
                  ? "choice active"
                  : "choice"
              }
              onClick={() => setFeeling("Confused")}
            >
              Confused
            </button>

            <button
              className={
                feeling === "Worried"
                  ? "choice active"
                  : "choice"
              }
              onClick={() => setFeeling("Worried")}
            >
              Worried
            </button>

            <button
              className={
                feeling === "Fine"
                  ? "choice active"
                  : "choice"
              }
              onClick={() => setFeeling("Fine")}
            >
              Fine
            </button>

          </div>

        </div>

        <div className="privacy-note">
          🔒 You can skip anything you're not comfortable answering.
        </div>

        <button
          className="start-button"
          onClick={handleContinue}
        >
          Continue to Results →
        </button>

      </div>

    </div>
  );
}

export default Questions;