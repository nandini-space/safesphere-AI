import { useNavigate } from "react-router-dom";

function SafetyPlan() {
  const navigate = useNavigate();

  return (
    <div className="page">
      <div className="analysis-container">

        <div className="analysis-header">
          <span className="soft-badge">
            🌱 Your Safety Plan
          </span>

          <h1>Choose Your Next Steps</h1>

          <p>
            Here are some supportive actions you can consider.
            You can choose the steps that feel right for you.
          </p>
        </div>

        <div className="question-card">
          <h3>🛡️ Personal Safety Checklist</h3>

          <label>
            <input type="checkbox" />
            Take some space from the interaction
          </label>

          <br />

          <label>
            <input type="checkbox" />
            Review and adjust my privacy settings
          </label>

          <br />

          <label>
            <input type="checkbox" />
            Talk to someone I trust
          </label>

          <br />

          <label>
            <input type="checkbox" />
            Keep important evidence safely stored
          </label>

          <br />

          <label>
            <input type="checkbox" />
            Report the interaction if appropriate
          </label>
        </div>

        <div className="question-card">
          <h3>💜 Remember</h3>

          <p>
            You don't have to make every decision at once.
            Take your time and choose the steps that help
            you feel more comfortable and supported.
          </p>
        </div>

        <div
          style={{
            display: "flex",
            gap: "12px",
            flexWrap: "wrap",
            marginTop: "25px"
          }}
        >
          <button
            className="start-button"
            onClick={() => navigate("/vault")}
          >
            Continue to Evidence Vault →
          </button>

          <button
            className="choice"
            onClick={() => navigate("/")}
          >
            Back to Home
          </button>
        </div>

      </div>
    </div>
  );
}

export default SafetyPlan;