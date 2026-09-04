import { useNavigate } from "react-router-dom";

function Home() {
  const navigate = useNavigate();

  return (
    <div className="home">
      <div className="hero">
        <div className="logo">🛡️</div>

        <h1>SafeSphere</h1>

        <p>
          Understand difficult online interactions
          and discover safer next steps.
        </p>

        <p className="small-text">
          Share only what you are comfortable sharing.
        </p>

        <button onClick={() => navigate("/analyze")}>
          Start Analysis
        </button>
      </div>
    </div>
  );
}

export default Home;