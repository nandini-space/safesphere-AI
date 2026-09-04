import { useNavigate } from "react-router-dom";

function Results() {
  const navigate = useNavigate();

  return (
    <div className="page">

      <div className="analysis-container">

        {/* Header */}
        <div className="analysis-header">

          <span className="soft-badge">
            🛡️ Your SafeSphere Results
          </span>

          <h1>Interaction Overview</h1>

          <p>
            Here is a calm summary of the patterns
            identified from the interaction.
          </p>

        </div>

        {/* Risk Card */}
        <div className="question-card">

          <h3>Overall Risk Level</h3>

          <div
            style={{
              padding: "20px",
              borderRadius: "15px",
              background: "#fff8e7",
              marginTop: "15px"
            }}
          >

            <strong
              style={{
                color: "#d99a19",
                fontSize: "24px"
              }}
            >
              Moderate
            </strong>

            <p>
              Some patterns may deserve attention.
              Consider reviewing the guidance below.
            </p>

          </div>

        </div>

        {/* Why Flagged */}
        <div className="question-card">

          <h3>🔎 Why was this flagged?</h3>

          <p>
            SafeSphere identified some communication
            patterns that may be worth looking at more
            carefully.
          </p>

        </div>

        {/* Detected Patterns */}
        <div className="question-card">

          <h3>💡 Detected Patterns</h3>

          <div className="choice-row">

            <button className="choice">
              Repeated Pressure
            </button>

            <button className="choice">
              Uncomfortable Communication
            </button>

            <button className="choice">
              Boundary Concerns
            </button>

          </div>

        </div>

        {/* Timeline */}
        <div className="question-card">

          <h3>📈 Escalation Timeline</h3>

          <p>
            SafeSphere can help you review whether
            communication patterns changed over time.
          </p>

          <div
            style={{
              marginTop: "20px",
              padding: "20px",
              borderRadius: "14px",
              background: "#f7f2ff"
            }}
          >

            <p>
              <strong>Earlier:</strong> Normal interaction
            </p>

            <p>
              <strong>Later:</strong> Increased pressure
            </p>

            <p>
              <strong>Current:</strong> Something feels
              uncomfortable
            </p>

          </div>

        </div>

        {/* Next Steps */}
        <div className="question-card">

          <h3>🌱 Safer Next Steps</h3>

          <p>
            You can take your time before deciding what
            to do next.
          </p>

          <ul>
            <li>Consider setting clear boundaries.</li>
            <li>Talk to someone you trust.</li>
            <li>Keep important evidence if needed.</li>
            <li>Take a break from the interaction if necessary.</li>
          </ul>

        </div>

        {/* Navigation Buttons */}
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
            onClick={() => navigate("/safety-plan")}
          >
            Create Safety Plan →
          </button>

          <button
            className="choice"
            onClick={() => navigate("/vault")}
          >
            Open Evidence Vault
          </button>

        </div>

      </div>

    </div>
  );
}

export default Results;