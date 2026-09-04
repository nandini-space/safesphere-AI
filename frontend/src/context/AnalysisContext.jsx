import { createContext, useContext, useState } from "react";

const AnalysisContext = createContext(null);

export function AnalysisProvider({ children }) {
  const [conversation, setConversation] = useState("");
  const [analysis, setAnalysis] = useState(null);
  const [answers, setAnswers] = useState({});
  const [context, setContext] = useState({
    unknown_sender: false,
    repeated_behavior: false,
  });
  const [result, setResult] = useState(null);

  const beginAnalysis = (text, newAnalysis) => {
    setConversation(text);
    setAnalysis(newAnalysis);
    setAnswers({});
    setContext({ unknown_sender: false, repeated_behavior: false });
    setResult(null);
  };

  return (
    <AnalysisContext.Provider value={{
      conversation, analysis, answers, context, result,
      setAnswers, setContext, setResult, beginAnalysis,
    }}>
      {children}
    </AnalysisContext.Provider>
  );
}

// eslint-disable-next-line react-refresh/only-export-components
export function useAnalysis() {
  const value = useContext(AnalysisContext);
  if (!value) throw new Error("useAnalysis must be used inside AnalysisProvider");
  return value;
}
