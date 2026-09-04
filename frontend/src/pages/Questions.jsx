import { useNavigate } from "react-router-dom";

function Questions() {
  const navigate = useNavigate();

  return (
    <div className="page">
      <h1>A Few Questions</h1>

      <p>
        Answer these questions to help us understand the situation better.
      </p>

      <h3>How did this interaction make you feel?</h3>

      <button onClick={() => alert("You selected: Uncomfortable")}>
  Uncomfortable
</button>

<button onClick={() => alert("You selected: Confused")}>
  Confused
</button>

<button onClick={() => alert("You selected: Worried")}>
  Worried
</button>

<button onClick={() => alert("You selected: Fine")}>
  Fine
</button>

      <br />
      <br />

      <button onClick={() => navigate("/results")}>
        Continue
      </button>
    </div>
  );
}

export default Questions;