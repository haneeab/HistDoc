import React, { useState, useEffect } from "react";
import NavbarDev from "./NavbarDev";
import { useLocation } from "react-router-dom";

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

function useQuery() {
  return new URLSearchParams(useLocation().search);
}

const DeveloperTestModelPage = () => {
  const query = useQuery();
  const modelId = query.get("model_id");
  const [model, setModel] = useState(null);
  const [parameters, setParameters] = useState([]);
  const [parameterValues, setParameterValues] = useState({});
  const [image, setImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [resultImage, setResultImage] = useState(null);

  useEffect(() => {
    if (modelId) {
      fetch(`http://127.0.0.1:8000/api/developer-model/${modelId}/`, { credentials: "include" })
        .then(res => res.json())
        .then(data => setModel(data));

      fetch(`http://127.0.0.1:8000/api/model-parameters/${modelId}/`, { credentials: "include" })
        .then(res => res.json())
        .then(data => {
          setParameters(data);
          const defaults = {};
          data.forEach(param => {
            defaults[param.name] = param.default || "";
          });
          setParameterValues(defaults);
        });
    }
  }, [modelId]);

  const handleRunTest = () => {
    if (!image) {
      alert("Please upload an image.");
      return;
    }

    const formData = new FormData();
    formData.append("model_id", modelId);
    formData.append("image", image);
    formData.append("parameters", JSON.stringify(parameterValues));

    fetch("http://127.0.0.1:8000/api/developer-test-model/", {
      method: "POST",
      credentials: "include",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: formData,
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          setResultImage(data.result_image);
          setImagePreview(data.input_image);
        } else {
          alert("❌ Error: " + data.error);
        }
      });
  };

  return (
    <>
      <NavbarDev />
<div style={{
  minHeight: "100vh",
  background: "linear-gradient(to bottom right, #007f3f, #8b8b8b)",
  paddingTop: "100px",
  paddingBottom: "60px",
  display: "flex",
  justifyContent: "center",
  alignItems: "flex-start"
}}>
  <div style={{
    maxWidth: "850px",
    width: "100%",
    backgroundColor: "white",
    borderRadius: "15px",
    padding: "30px",
    boxShadow: "0 4px 10px rgba(0,0,0,0.2)"
  }}>
        <h2 style={{ color: "#007f3f" }}>🧪 Test Model: {model?.name}</h2>

        {model && (
          <p style={{ fontStyle: "italic", color: "#555" }}>
            <strong>Description:</strong> {model.description || "No description provided."}
          </p>
        )}

        {parameters.map((param, index) => (
          <div key={index} style={{ marginBottom: 10 }}>
            <label>{param.name}:</label>
            {Array.isArray(param.choices) && param.choices.length > 0 ? (
              <select
                value={parameterValues[param.name] || ""}
                onChange={(e) =>
                  setParameterValues({ ...parameterValues, [param.name]: e.target.value })
                }
                style={{ marginLeft: 10 }}
              >
                <option value="">-- Select --</option>
                {param.choices.map((choice, idx) => (
                  <option key={idx} value={choice}>{choice}</option>
                ))}
              </select>
            ) : (
              <input
                type="text"
                value={parameterValues[param.name] || ""}
                onChange={(e) =>
                  setParameterValues({ ...parameterValues, [param.name]: e.target.value })
                }
                style={{ marginLeft: 10 }}
              />
            )}
          </div>
        ))}

        <label>Upload Test Image:</label>
        <input
          type="file"
          accept="image/*"
          onChange={(e) => setImage(e.target.files[0])}
          style={{ display: "block", marginBottom: "20px" }}
        />

        <button
          onClick={handleRunTest}
          style={{ padding: "10px 20px", backgroundColor: "#007f3f", color: "white", border: "none", borderRadius: "5px" }}
        >
          ⚙️ Run Test
        </button>

        {(imagePreview || resultImage) && (
          <div style={{ marginTop: "30px", display: "flex", gap: "20px" }}>
            {imagePreview && (
              <div>
                <h4>📥 Uploaded Image:</h4>
                <img
                  src={imagePreview}
                  alt="Uploaded"
                  style={{ maxWidth: "100%", border: "2px solid #aaa", borderRadius: "10px" }}
                />
              </div>
            )}
            {resultImage && (
              <div>
                <h4>🖼 Result Image:</h4>
                <img
                  src={resultImage}
                  alt="Result"
                  style={{ maxWidth: "100%", border: "2px solid #007f3f", borderRadius: "10px" }}
                />
              </div>
            )}
          </div>
        )}
      </div>
</div>
    </>
  );
};

export default DeveloperTestModelPage;
