import React, { useEffect, useState } from "react";
import { useParams, useHistory } from "react-router-dom";
import NavbarDev from "./NavbarDev";

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + "=")) {
        return decodeURIComponent(cookie.substring(name.length + 1));
      }
    }
  }
  return cookieValue;
}

const AnnotateModelEditor = () => {
  const { modelId } = useParams();
const history = useHistory();
  const [code, setCode] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/api/annotate-model/${modelId}/`, {
      method: "GET",
      credentials: "include",
    })
      .then((res) => res.json())
      .then((data) => {
        setCode(data.code || "");
        setLoading(false);
      })
      .catch(() => {
        alert("❌ Failed to load model file.");
        setLoading(false);
      });
  }, [modelId]);

  const handleSave = () => {
    fetch(`http://127.0.0.1:8000/api/annotate-model/${modelId}/`, {
      method: "PATCH",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({ code }),
    })
      .then((res) => res.json())
      .then((data) => {
        alert("✅ Code updated successfully.");
history.push("/developer-models");
      })
      .catch(() => {
        alert("❌ Failed to update model.");
      });
  };

  return (
    <>
      <NavbarDev />
      <div style={{ padding: "100px 20px",        background: "linear-gradient(to bottom right, #007f3f, #8b8b8b)",
 minHeight: "100vh" }}>
        <div style={{ maxWidth: "900px", margin: "0 auto", background: "white", padding: "20px", borderRadius: "10px" }}>
          <h2 style={{ color: "#007f3f" }}>📝 Annotate Model #{modelId}</h2>
          {loading ? (
            <p>Loading...</p>
          ) : (
            <>
              <textarea
                value={code}
                onChange={(e) => setCode(e.target.value)}
                rows={25}
                style={{ width: "100%", fontFamily: "monospace", fontSize: "14px", padding: "10px" }}
              />
              <br />
              <button
                onClick={handleSave}
                style={{ marginTop: "10px", padding: "10px 20px", backgroundColor: "#007f3f", color: "white", border: "none", borderRadius: "5px" }}
              >
                💾 Save Changes
              </button>
            </>
          )}
        </div>
      </div>
    </>
  );
};

export default AnnotateModelEditor;
