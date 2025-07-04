import React from 'react';
import { useLocation, useNavigate } from "react-router-dom";
import "./ResultsPage.css"

function ResultsPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const items = location.state?.data || [];

  return (
    <div style={{ maxWidth: "600px", margin: "auto", fontFamily: "Arial, sans-serif", textAlign: "center" }}>
      <h2>Results</h2>
      {items.length === 0 ? (
        <p>No data found for the selected range.</p>
      ) : (
        <table className="table-fuckery" style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th style={{ borderBottom: "2px solid #000", textAlign: "left", padding: "8px" }}>topicID</th>
              <th style={{ borderBottom: "2px solid #000", textAlign: "left", padding: "8px" }}>data</th>
              <th style={{ borderBottom: "2px solid #000", textAlign: "left", padding: "8px" }}>time</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item, index) => (
              <tr key={index} style={{ borderBottom: "1px solid #ddd" }}>
                <td style={{ padding: "8px" }}>{item.topicID}</td>
                <td style={{ padding: "8px" }}>{item.data}</td>
                <td style={{ padding: "8px" }}>{new Date(item.time).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      <button
        className="btn-primary"
        onClick={() => navigate(-1)}
        style={{ marginTop: "1rem" }}
      >
        Back to Search
      </button>
    </div>
  );
}

export default ResultsPage;
