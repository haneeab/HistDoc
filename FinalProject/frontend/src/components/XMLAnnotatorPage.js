import React, { useEffect, useState } from "react";
import { useHistory, useLocation } from "react-router-dom";
import Navbar from "./Navbar";

function useQuery() {
  return new URLSearchParams(useLocation().search);
}

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

const XMLAnnotatorPage = () => {
  const query = useQuery();
  const xmlId = query.get("xml_id");
  const [xmlText, setXmlText] = useState("");
const history = useHistory();

  useEffect(() => {
    fetch(`/api/ground-xml/${xmlId}/annotator/`, {
      credentials: "include",
    })
      .then((res) => res.json())
      .then((data) => setXmlText(data.xml));
  }, [xmlId]);

  const handleSave = () => {
    fetch(`/api/ground-xml/${xmlId}/annotator/`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      credentials: "include",
      body: JSON.stringify({ xml: xmlText }),
    })
      .then((res) => res.json())
      .then(() => {
        alert("XML saved successfully.");
history.goBack();  // go back
      });
  };

  return (
    <>
      <Navbar />
      <div style={{
        minHeight: "100vh",
        padding: "80px 20px",
        background: "linear-gradient(to bottom right, #007f3f, #8b8b8b)",
      }}>
        <div style={{ maxWidth: "900px", margin: "auto", background: "white", padding: "30px", borderRadius: "10px" }}>
          <h2 style={{ textAlign: "center", color: "#007f3f" }}>📝 XML Annotator</h2>
          <textarea
            value={xmlText}
            onChange={(e) => setXmlText(e.target.value)}
            rows={25}
            style={{ width: "100%", fontFamily: "monospace", fontSize: "14px", padding: "10px", borderRadius: "5px" }}
          />
          <button
            onClick={handleSave}
            style={{
              marginTop: "20px",
              backgroundColor: "#007f3f",
              color: "white",
              padding: "10px 20px",
              border: "none",
              borderRadius: "5px",
              fontWeight: "bold",
            }}
          >
            💾 Save Changes
          </button>
        </div>
      </div>
    </>
  );
};

export default XMLAnnotatorPage;
