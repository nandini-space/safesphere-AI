import { useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAnalysis } from "../context/AnalysisContext";
import { analyzeAudio, analyzeConversation, analyzeImage } from "../services/api";

const inputTypes = [
  { id: "text", label: "Text conversation" },
  { id: "image", label: "Screenshot" },
  { id: "audio", label: "Voice recording" },
];

function Analyze() {
  const MAX_FILE_SIZE = 10 * 1024 * 1024;
  const navigate = useNavigate();
  const { beginAnalysis } = useAnalysis();
  const fileInputRef = useRef(null);
  const [inputType, setInputType] = useState("text");
  const [text, setText] = useState("");
  const [file, setFile] = useState(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const changeType = (type) => {
    setInputType(type);
    setFile(null);
    setError("");
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  const handleAnalyze = async () => {
    if (inputType === "text" && !text.trim()) {
      setError("Please enter or paste a conversation before continuing.");
      return;
    }
    if (inputType !== "text" && !file) {
      setError(`Please choose a ${inputType === "image" ? "screenshot" : "voice recording"} first.`);
      return;
    }
    if (file && file.size > MAX_FILE_SIZE) {
      setError("Please choose a file smaller than 10 MB.");
      return;
    }

    setError("");
    setIsLoading(true);
    try {
      const response = inputType === "text"
        ? await analyzeConversation(text.trim())
        : inputType === "image"
          ? await analyzeImage(file)
          : await analyzeAudio(file);

      if (!response.analysis || !Array.isArray(response.analysis.indicators)) {
        throw new Error("Invalid analysis response");
      }
      beginAnalysis(response.extracted_text || text.trim() || file.name, response.analysis);
      navigate("/questions");
    } catch (requestError) {
      const setupError = requestError.message?.includes("not configured") || requestError.message?.includes("not installed");
      setError(setupError ? requestError.message : "Unable to analyze this interaction right now. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const fileLabel = inputType === "image" ? "Upload a chat screenshot" : "Upload a voice recording";
  const acceptedFiles = inputType === "image" ? "image/png,image/jpeg,image/webp" : "audio/wav,audio/x-wav,audio/mpeg,audio/mp4,audio/webm";

  return (
    <div className="page analyze-page"><div className="analysis-container">
      <div className="analysis-header">
        <span className="soft-badge">Private conversation check</span>
        <h1>Analyze an interaction</h1>
        <p>Choose text, a screenshot, or a voice recording. Share only what feels comfortable.</p>
      </div>
      <div className="question-card">
        <div className="input-type-tabs" role="tablist" aria-label="Analysis input type">
          {inputTypes.map((type) => <button key={type.id} className={inputType === type.id ? "choice active" : "choice"}
            onClick={() => changeType(type.id)} disabled={isLoading}>{type.label}</button>)}
        </div>
        {inputType === "text" ? <>
          <label className="field-label" htmlFor="conversation">Conversation</label>
          <textarea id="conversation" placeholder="Paste the conversation here..." value={text}
            onChange={(event) => setText(event.target.value)} disabled={isLoading} />
          <p className="field-help">Text analysis supports English, Hindi, Hinglish, and mixed conversations.</p>
        </> : <>
          <label className="field-label" htmlFor="media-file">{fileLabel}</label>
          <input ref={fileInputRef} id="media-file" className="media-input" type="file" accept={acceptedFiles} disabled={isLoading}
            onChange={(event) => setFile(event.target.files?.[0] || null)} />
          <p className="field-help">{inputType === "image" ? "PNG, JPG, and WebP screenshots up to 10 MB." : "WAV, MP3, M4A, or WebM audio up to 10 MB."}</p>
          {file && <p className="selected-file">Selected: {file.name}</p>}
        </>}
        {error && <p className="form-error" role="alert">{error}</p>}
        <button className="start-button" onClick={handleAnalyze} disabled={isLoading}>
          {isLoading ? `Analyzing ${inputType === "text" ? "the interaction" : "your upload"}...` : "Analyze interaction"}
        </button>
      </div>
    </div></div>
  );
}

export default Analyze;
