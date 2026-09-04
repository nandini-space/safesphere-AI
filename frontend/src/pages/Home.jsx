import { useNavigate } from "react-router-dom";

function Home() {
  const navigate = useNavigate();

  return (
    <div className="home">

      {/* Navigation */}
      <nav className="navbar">

        {/* Logo */}
        <div
          className="brand"
          onClick={() => navigate("/")}
          style={{ cursor: "pointer" }}
        >
          🛡️ <span>Safe<span>Sphere</span></span>
        </div>


        {/* Navigation Links */}
        <div className="nav-links">

          <button onClick={() => navigate("/")}>
            Home
          </button>

          <button onClick={() => navigate("/analyze")}>
            Analyze
          </button>

          <button onClick={() => navigate("/vault")}>
            Vault
          </button>

        </div>

      </nav>


      {/* Hero */}
      <main>

        <section className="hero-section">

          <div className="hero-content">

            <div className="badge">
              ✨ AI-Powered Digital Safety
            </div>


            <h1>
              Welcome to SafeSphere
            </h1>


            <p>
              A calm and supportive space to understand
              difficult online interactions and discover
              safer next steps.
            </p>


            {/* Privacy */}
            <div className="privacy-box">

              🛡️

              <div>

                <strong>
                  Your privacy comes first.
                </strong>

                <br />

                <small>
                  Share only what you're comfortable sharing.
                </small>

              </div>

            </div>


            {/* Start Analysis */}
            <button
              className="start-button"
              onClick={() => navigate("/analyze")}
            >
              Start Analysis →
            </button>

          </div>


          {/* Illustration */}
          <div className="hero-art">

            <div className="shield-circle">

              🛡️

              <div className="heart">
                ♥
              </div>

            </div>

          </div>

        </section>

        {/* Feature Cards */}
        <section className="features">

          <div className="feature-card pink-card">

            <div className="feature-icon">
              ?
            </div>

            <div>

              <h3>
                Understand
              </h3>

              <p>
                Identify patterns in online conversations.
              </p>

            </div>

          </div>


          <div className="feature-card yellow-card">

            <div className="feature-icon">
              💡
            </div>

            <div>

              <h3>
                Get Guidance
              </h3>

              <p>
                Receive clear and supportive next steps.
              </p>

            </div>

          </div>


          <div className="feature-card mint-card">

            <div className="feature-icon">
              🔐
            </div>

            <div>

              <h3>
                Stay Private
              </h3>

              <p>
                Keep control over what you choose to share.
              </p>

            </div>

          </div>

        </section>


        {/* Support Section */}
        <section className="support-card">

          <div className="support-icon">
            💗
          </div>


          <div>

            <h2>
              You're Not Alone
            </h2>

            <p>
              SafeSphere is here to support you with
              empathy, understanding, and tools for
              a safer digital experience.
            </p>

          </div>


          <div className="quote">

            <span>
              “
            </span>

            <p>
              It's okay to ask for help.
              <br />
              It's okay to prioritize your safety.
            </p>

          </div>

        </section>

      </main>

    </div>
  );
}

export default Home;