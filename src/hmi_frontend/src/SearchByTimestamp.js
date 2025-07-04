import React, {useState} from "react";
import {useNavigate} from "react-router-dom";
import './SearchByTimestamp.css';

function SearchByTimestamp() {
  const [start, setStart] = useState("");
  const [end, setEnd] = useState("");
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!start || !end) {
      setError("Please fill in both timestamps");
      return;
    }

    try {
      const response = await fetch(`http://localhost:8000/api/log_data/?start=${encodeURIComponent(start)}&end=${encodeURIComponent(end)}`, {
        cache: "no-store"
      });
      if (!response.ok) {
        console.error("Fetch failed with status:", response.status);
        throw new Error("Failed to fetch items");
      }

      const data = await response.json(); // make sure the server returns pure JSON!
      navigate('/results', { state: { data } });
    } catch (err) {
      setError(err.message);
    }
  };

  return (
      <div>
        <h2>Search Items by Timestamp</h2>
        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: "1rem" }}>
            <h3>Select the starting time</h3>
            <input
                className="date-input"
                type="datetime-local"
                value={start}
                onChange={(e) => setStart(e.target.value)}
                required
            />
          </div>

          <div style={{ marginBottom: "1rem" }}>
            <h3>Select the ending time</h3>
            <input
                className="date-input"
                type="datetime-local"
                value={end}
                onChange={(e) => setEnd(e.target.value)}
                required            />
          </div>

          <button className="btn-primary" type="submit">Retrieve Data</button>
        </form>

        {error && <p style={{ color: "red", marginTop: "1rem" }}>{error}</p>}
      </div>
  );
}

export default SearchByTimestamp;
