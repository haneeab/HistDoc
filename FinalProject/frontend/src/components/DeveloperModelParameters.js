import React, { useEffect, useState } from "react";
import { useHistory, useParams } from "react-router-dom";

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

const DeveloperModelParameters = () => {
  const { id } = useParams();
const history = useHistory();
  const [parameters, setParameters] = useState([]);

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/api/developer-model-parameters/${id}/`, {
      credentials: "include",
    })
      .then((res) => res.json())
      .then((data) => setParameters(data));
  }, [id]);

  const handleParamChange = (index, field, value) => {
    const updated = [...parameters];
    updated[index][field] = value;
    setParameters(updated);
  };

  const addParameter = () => {
    setParameters((prev) => [...prev, { name: "", param_type: "", choices: "", default: "" }]);
  };

  const removeParameter = (index) => {
    const updated = [...parameters];
    updated.splice(index, 1);
    setParameters(updated);
  };

  const saveParameters = () => {
    fetch(`http://127.0.0.1:8000/api/developer-model-parameters/${id}/`, {
      method: "PATCH",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({ parameters }),
    })
      .then((res) => res.json())
      .then((data) => {
        alert("✅ Parameters updated");
        history.push("/developer-models");
      })
      .catch((err) => {
        alert("❌ Update failed");
        console.error(err);
      });
  };

  return (
    <>
      <NavbarDev />
      <div
        style={{
          minHeight: "100vh",
          padding: "100px 2rem 2rem",
          background: "linear-gradient(to bottom right, #007f3f, #8b8b8b)",
        }}
      >
        <div style={{ maxWidth: "900px", background: "white", padding: 30, borderRadius: 10, margin: "auto" }}>
          <h2 style={{ color: "#007f3f" }}>⚙ Edit Model Parameters</h2>

          {parameters.map((param, index) => (
            <div
              key={index}
              style={{ marginBottom: 10, border: "1px dashed #ccc", borderRadius: 8, padding: 10 }}
            >
              <input
                type="text"
                placeholder="Name"
                value={param.name}
                onChange={(e) => handleParamChange(index, "name", e.target.value)}
                style={{ padding: 6, width: "22%", marginRight: 10 }}
              />
              <select
                value={param.param_type}
                onChange={(e) => handleParamChange(index, "param_type", e.target.value)}
                style={{ padding: 6, width: "20%", marginRight: 10 }}
              >
                <option value="">Type</option>
                <option value="str">str</option>
                <option value="int">int</option>
                <option value="float">float</option>
                <option value="bool">bool</option>
              </select>
              <input
                type="text"
                placeholder="Choices (comma separated)"
                value={param.choices || ""}
                onChange={(e) => handleParamChange(index, "choices", e.target.value)}
                style={{ padding: 6, width: "30%", marginRight: 10 }}
              />
              <input
                type="text"
                placeholder="Default"
                value={param.default || ""}
                onChange={(e) => handleParamChange(index, "default", e.target.value)}
                style={{ padding: 6, width: "20%" }}
              />
              <button
                onClick={() => removeParameter(index)}
                style={{ marginLeft: 10, backgroundColor: "#ff4d4d", color: "white", border: "none", padding: "6px 10px", borderRadius: 5 }}
              >
                ❌
              </button>
            </div>
          ))}

          <button
            onClick={addParameter}
            style={{ marginTop: 20, backgroundColor: "#007f3f", color: "white", padding: "8px 15px", border: "none", borderRadius: 6 }}
          >
            ➕ Add Parameter
          </button>

          <button
            onClick={saveParameters}
            style={{ marginTop: 20, marginLeft: 10, backgroundColor: "#005a2f", color: "white", padding: "8px 15px", border: "none", borderRadius: 6 }}
          >
            💾 Save
          </button>
        </div>
      </div>
    </>
  );
};

export default DeveloperModelParameters;
