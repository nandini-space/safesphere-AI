import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Analyze() {
  const [type, setType] = useState("text");
  const [text, setText] = useState("");

  const navigate = useNavigate();

  const handleAnalyze = () => {
    if (type === "text" && !text.trim()) {
      alert("Please enter a conversation.");
      return;
    }

    navigate("/questions");
  };

  return (
    <div className="page">
      <h1>Analyze an Interaction</h1>

      <p>Choose how you want to provide the interaction.</p>

      <div className="tabs">
        <button onClick={() => setType("text")}>
          📝 Conversation
        </button>

        <button onClick={() => setType("image")}>
          📷 Screenshot
        </button>

        <button onClick={() => setType("audio")}>
          🎙️ Audio
        </button>
      </div>

      {type === "text" && (
        <textarea
          placeholder="Paste the conversation here..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
      )}

      {type === "image" && (
        <div>
          <p>Select a screenshot:</p>
          <input type="file" accept="image/*" />
        </div>
      )}

      {type === "audio" && (
        <div>
          <p>Select an audio recording:</p>
          <input type="file" accept="audio/*" />
        </div>
      )}

      <button onClick={handleAnalyze}>
        Analyze
      </button>
    </div>
  );
}

export default Analyze;