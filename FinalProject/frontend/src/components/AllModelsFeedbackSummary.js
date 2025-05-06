import React, { useEffect, useState } from "react";
import NavbarDev from "./NavbarDev";

function getCookie(name) {
  const cookies = document.cookie.split(";").map(c => c.trim());
  for (const cookie of cookies) {
    if (cookie.startsWith(name + "=")) {
      return decodeURIComponent(cookie.split("=")[1]);
    }
  }
  return null;
}

export default function AllModelsFeedbackSummary() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/models-summary/", {
      credentials: "include",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
    })
      .then(res => res.json())
      .then(setData)
      .catch(err => console.error(err));
  }, []);

  return (
    <>
      <NavbarDev />
      <div style={{ padding: "80px 20px",  background: "linear-gradient(to bottom right, #007f3f, #8b8b8b)"
, minHeight: "100vh", color: "#fff" }}>
        {data.map((model) => (
          <div
            key={model.model_id}
            style={{
              background: "white",
              color: "#333",
              borderRadius: "10px",
              padding: "20px",
              margin: "20px auto",
              maxWidth: "800px",
              boxShadow: "0 2px 6px rgba(0,0,0,0.2)",
            }}
          >

            <h3 style={{ color: "#007f3f" }}>{model.model_name.split("/").pop()}</h3>
            <p>⭐ Average Rating: <strong>{model.average_rating ?? "No ratings yet"}</strong></p>
            {model.latest_feedbacks.length > 0 ? (
              model.latest_feedbacks.map(fb => (
                <div key={fb.id} style={{ marginTop: "10px", padding: "10px", borderTop: "1px solid #ccc" }}>
                  <p><strong>{fb.username}</strong> rated: {"⭐".repeat(fb.rating)} ({fb.rating})</p>
                  <p>{fb.feedback}</p>
                  <p style={{ fontSize: "0.8rem", color: "#666" }}>Submitted on {new Date(fb.created_at).toLocaleString()}</p>
                </div>
              ))
            ) : (
              <p>No feedback yet</p>
            )}
          </div>
        ))}
      </div>
    </>
  );
}
