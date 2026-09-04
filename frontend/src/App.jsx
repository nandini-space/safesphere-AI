import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import Analyze from "./pages/Analyze";
import Questions from "./pages/Questions";
import Results from "./pages/Results";
import SafetyPlan from "./pages/SafetyPlan";
import Vault from "./pages/Vault";
import { AnalysisProvider } from "./context/AnalysisContext";

function App() {
  return (
    <BrowserRouter>
      <AnalysisProvider>
      <Routes>

        {/* Home */}
        <Route path="/" element={<Home />} />

        {/* Analyze Interaction */}
        <Route path="/analyze" element={<Analyze />} />

        {/* Questions */}
        <Route path="/questions" element={<Questions />} />

        {/* Results */}
        <Route path="/results" element={<Results />} />

        {/* Safety Plan */}
        <Route path="/safety-plan" element={<SafetyPlan />} />

        {/* Evidence Vault */}
        <Route path="/vault" element={<Vault />} />

      </Routes>
      </AnalysisProvider>
    </BrowserRouter>
  );
}

export default App;
