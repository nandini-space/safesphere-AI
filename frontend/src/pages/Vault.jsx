import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Vault() {
  const navigate = useNavigate();

  const [files, setFiles] = useState([]);

  const handleFileChange = (event) => {
    const selectedFiles = Array.from(event.target.files);

    setFiles((previousFiles) => [
      ...previousFiles,
      ...selectedFiles,
    ]);
  };

  const removeFile = (indexToRemove) => {
    setFiles((previousFiles) =>
      previousFiles.filter(
        (_, index) => index !== indexToRemove
      )
    );
  };

  return (
    <div className="page">

      <div className="analysis-container">

        {/* Header */}
        <div className="analysis-header">

          <span className="soft-badge">
            🔐 Your Evidence Vault
          </span>

          <h1>Keep Your Evidence Organized</h1>

          <p>
            Store important screenshots, recordings, or
            other files in one place for easy review.
          </p>

        </div>


        {/* Upload Card */}
        <div className="question-card">

          <h3>📁 Add Evidence</h3>

          <p>
            Select files from your computer to add them
            to this temporary vault.
          </p>

          <input
            type="file"
            multiple
            onChange={handleFileChange}
          />

        </div>


        {/* Files */}
        <div className="question-card">

          <h3>📋 Evidence Items</h3>

          {files.length === 0 ? (

            <p>
              No evidence has been added yet.
            </p>

          ) : (

            <div>

              {files.map((file, index) => (

                <div
                  key={`${file.name}-${index}`}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                    gap: "15px",
                    padding: "14px",
                    marginBottom: "10px",
                    borderRadius: "12px",
                    background: "#f7f2ff"
                  }}
                >

                  <div>

                    <strong>
                      {file.name}
                    </strong>

                    <p
                      style={{
                        margin: "5px 0 0",
                        fontSize: "13px",
                        color: "#6d6880"
                      }}
                    >
                      {(file.size / 1024).toFixed(1)} KB
                    </p>

                  </div>

                  <button
                    className="choice"
                    onClick={() => removeFile(index)}
                  >
                    Remove
                  </button>

                </div>

              ))}

            </div>

          )}

        </div>


        {/* Privacy Notice */}
        <div className="privacy-note">

          🔒 Privacy reminder: Only add files you are
          comfortable storing. This current version keeps
          selected files in the browser interface only.

        </div>


        {/* Navigation */}
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
            onClick={() => navigate("/")}
          >
            Back to Home
          </button>

          <button
            className="choice"
            onClick={() => navigate("/analyze")}
          >
            Analyze Another Interaction
          </button>

        </div>

      </div>

    </div>
  );
}

export default Vault;