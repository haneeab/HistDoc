import React, { useEffect, useState } from "react";
import { useLocation, Link } from "react-router-dom";
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

const ModelSelectionPage = () => {
  const query = useQuery();
  const fileId = query.get("file_id");
  const manuscriptId = query.get("manuscript_id");
  const [models, setModels] = useState([]);
  const [selectedModelId, setSelectedModelId] = useState(null);
  const [selectedModel, setSelectedModel] = useState(null);

  const [parameters, setParameters] = useState([]);
  const [parameterValues, setParameterValues] = useState({});
  const [imagePreview, setImagePreview] = useState(null);
  const [resultImage, setResultImage] = useState(null);
  const [zoomInput, setZoomInput] = useState(1);
  const [zoomOutput, setZoomOutput] = useState(1);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/list_all_developer_models/", { credentials: "include" })
      .then((res) => res.json())
      .then((data) => setModels(data));

    fetch(`http://127.0.0.1:8000/api/get-manuscript-file/${fileId}/`, { credentials: "include" })
      .then((res) => res.json())
      .then((data) => {
        if (data.file) {
          const fileName = data.file.split("/").pop();
          const imageUrl = `http://127.0.0.1:8000/api/media/${fileName}`;
          setImagePreview(imageUrl);

          const resultPath = `http://127.0.0.1:8000/api/media/processed/image_${fileId}_bin.png`;
          fetch(resultPath, { method: "HEAD" })
            .then((res) => {
              if (res.status === 200) {
                setResultImage(resultPath);
              } else {
                setResultImage(null);
              }
            })
            .catch((err) => console.error("HEAD check failed:", err));
        }
      });
  }, [fileId]);

 useEffect(() => {
  if (selectedModelId) {
    const model = models.find((m) => m.id === parseInt(selectedModelId));
    setSelectedModel(model);  // ✅ save full model (to access description)

    fetch(`http://127.0.0.1:8000/api/model-parameters/${selectedModelId}/`, {
      credentials: "include",
    })
      .then((res) => res.json())
      .then((data) => {
        setParameters(data);
        const initialValues = {};
        data.forEach((param) => {
          initialValues[param.name] = param.default || "";
        });
        setParameterValues(initialValues);
      });
  } else {
    setSelectedModel(null);  // clear if no model selected
    setParameters([]);
  }
}, [selectedModelId, models]);



const handleRunModel = () => {
  if (!selectedModelId) return alert("Please select a model first!");

  const payload = {
    model_id: selectedModelId,
    parameters: parameterValues,  // ✅ correct format
  };

  fetch(`http://127.0.0.1:8000/api/run-model/${fileId}/`, {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify(payload),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {
        alert("✅ Model ran successfully!");
        setResultImage(data.output_image);
      } else {
        alert("Error: " + data.error);
      }
    });


};


  return (
    <>
      <Navbar />
      <div
        style={{
          padding: "80px 20px",
          fontFamily: "Arial",
          background: "linear-gradient(to bottom right, #007f3f, #8b8b8b)",
        }}>
        <div
          style={{
            maxWidth: "900px",
            backgroundColor: "white",
            margin: "0 auto",
            padding: "30px",
            borderRadius: "15px",
            boxShadow: "0 4px 10px rgba(0, 0, 0, 0.2)",
          }}>
          <h2 style={{ color: "#007f3f" }}>🧠 Select Model to Run on File #{fileId}</h2>

          <div style={{ marginBottom: "30px" }}>
            <label style={{ fontWeight: "bold" }}>Choose a Model:</label><br />
            <select
              onChange={(e) => setSelectedModelId(e.target.value)}
              value={selectedModelId || ""}
              style={{ marginBottom: "20px", padding: "10px", width: "300px" }}>
              <option value="">-- Choose a Model --</option>
              {models.map((model) => (
                <option key={model.id} value={model.id}>
                  {model.file.split("/").pop()}
                </option>
              ))}
            </select>
{selectedModel && (
    <p style={{ fontStyle: "italic", color: "#444", marginBottom: "20px" }}>
      <strong>Description:</strong> {selectedModel.description || "No description provided."}
    </p>
  )}

            {parameters.length > 0 && (
              <div style={{ marginBottom: 20 }}>
                <h4 style={{ marginBottom: 10 }}>🔧 Parameters:</h4>
                {parameters.map((param) => (
                  <div key={param.name} style={{ marginBottom: 10 }}>
                    <label>{param.name}:</label>
                {Array.isArray(param.choices) && param.choices.length > 0 ? (
                      <select
                        value={parameterValues[param.name] || ""}
                        onChange={(e) =>
                          setParameterValues({
                            ...parameterValues,
                            [param.name]: e.target.value,
                          })
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
                          setParameterValues({
                            ...parameterValues,
                            [param.name]: e.target.value,
                          })
                        }
                        style={{ marginLeft: 10 }}
                      />
                    )}
                  </div>
                ))}
              </div>
            )}

            <button
              onClick={handleRunModel}
              style={{ padding: "10px 20px", backgroundColor: "#007f3f", color: "white", border: "none", borderRadius: "5px" }}>
              ⚙️ Run Model
            </button>
          </div>

          <div style={{ display: "flex", gap: "40px", flexWrap: "wrap" }}>
            {imagePreview && (
              <div>
                <p><strong>📄 Original Image:</strong></p>
                <img
                  src={imagePreview}
                  alt="Original"
                  style={{ maxWidth: `${300 * zoomInput}px`, borderRadius: "8px" }}
                /><br />
                <button onClick={() => setZoomInput((z) => Math.min(z + 0.1, 3))}>➕ Zoom In</button>
                <button onClick={() => setZoomInput((z) => Math.max(z - 0.1, 0.5))}>➖ Zoom Out</button>
              </div>
            )}

            {resultImage && (
              <div>
                <p><strong>🖼 Result Image:</strong></p>
                <img
                  src={resultImage}
                  alt="Result"
                  style={{ maxWidth: `${300 * zoomOutput}px`, border: "2px solid green", borderRadius: "8px" }}
                /><br />
                <button onClick={() => setZoomOutput((z) => Math.min(z + 0.1, 3))}>➕ Zoom In</button>
                <button onClick={() => setZoomOutput((z) => Math.max(z - 0.1, 0.5))}>➖ Zoom Out</button>
              </div>
            )}
          </div>

          <div style={{ marginTop: "40px" }}>
            <Link
              to={`/ManuscriptFilesPage?id=${manuscriptId}`}
              style={{ textDecoration: "none", color: "#007f3f", fontWeight: "bold" }}>
              ← Back to Manuscript Files
            </Link>
          </div>
           <Link to={`/feedback/${selectedModelId}`}>
  <button style={{ backgroundColor: "#007f3f", color: "white", padding: "5px 10px", borderRadius: "5px", border: "none", cursor: "pointer", fontSize: "0.8rem" }}>
    Feedback
  </button>
</Link>



        </div>
      </div>
    </>
  );
};

export default ModelSelectionPage;
