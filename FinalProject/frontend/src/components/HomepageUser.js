import React, { Component } from "react";
import Navbar from "./Navbar";
import { FaUpload } from "react-icons/fa"; //

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

export default class HomepageUser extends Component {
  constructor(props) {
    super(props);
   this.state = {
  uploadedImages: [],
  file: null,
  message: "",
  availableModels: [],
  selectedModels: {},
};

  }

 componentDidMount() {
  fetch("http://127.0.0.1:8000/api/user-images/", {
    method: "GET",
    credentials: "include",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
    },
  })
    .then((res) => res.json())
    .then((data) => {
      this.setState({ uploadedImages: data });
    })
    .catch((err) => {
      console.error("Error loading images:", err);
    });
fetch("http://127.0.0.1:8000/api/all-developer-models/", {
  method: "GET",
  credentials: "include",
  headers: {
    "X-CSRFToken": getCookie("csrftoken"),
  },
})
  .then((res) => res.json())
  .then((models) => {
    this.setState({ availableModels: models });
  })
  .catch((err) => console.error("Error loading models:", err));

}


  handleFileChange = (e) => {
    this.setState({ file: e.target.files[0] });
  };

  handleImageUpload = () => {
    const { file } = this.state;
    if (!file) {
      alert(" No file selected!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("file_type", "image");

    fetch("http://127.0.0.1:8000/api/upload-file/", {
      method: "POST",
      credentials: "include",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: formData,
    })
      .then(async (res) => {
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || "Upload failed");

        alert("✅ File uploaded!");

        this.setState((prev) => ({
          uploadedImages: [
            ...prev.uploadedImages,
            {
              id: data.id,
              src: data.file_url,
              text: "Processing...",
            },
          ],
          file: null,
        }));
      })
      .catch((err) => {
        alert("❌ Upload failed: " + err.message);
        console.error(err);
      });
  };

  handleExtractText = async (imageId) => {
  const modelId = this.state.selectedModels?.[imageId];

  if (!modelId) {
    alert("⚠ Please select a model before extracting text.");
    return;
  }

  this.setState({ message: "🔄 Running inference..." });

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/api/run-inference/${imageId}/`,
      {
        method: "POST",
        credentials: "include",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ model_id: modelId }),
      }
    );

    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Inference failed");

    this.setState((prevState) => ({
      uploadedImages: prevState.uploadedImages.map((img) =>
        img.id === imageId
          ? {
              ...img,
              extracted_text: data.extracted_text,
              output: data.output_image,
            }
          : img
      ),
      message: "✅ Inference completed!",
    }));
  } catch (err) {
    console.error("❌ Inference error:", err);
    this.setState({ message: "❌ Inference failed: " + err.message });
  }
};


  handleFullText = (text) => {
    alert(`Full Text: ${text}`);
  };

  render() {
    const { uploadedImages, file, message } = this.state;

    return (
      <>
        <Navbar />
        <div
          style={{
            minHeight: "100vh",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            background: "linear-gradient(to bottom right, #007f3f, #8b8b8b)",
            padding: "2rem",
          }}
        >
          <div
            style={{
                              marginTop:"60px",

              maxWidth: "850px",
              width: "100%",
              backgroundColor: "white",
              borderRadius: "15px",
              padding: "30px",
              boxShadow: "0 4px 10px rgba(0, 0, 0, 0.2)",
            }}
          >
            <h2
              style={{
                textAlign: "center",
                color: "#007f3f",
                fontFamily: "'Handlee', cursive",
                marginBottom: "20px",
              }}
            >
              Welcome to Your Dashboard
            </h2>

            {message && (
              <p
                style={{
                  color: "green",
                  textAlign: "center",
                  marginBottom: "20px",
                }}
              >
                {message}
              </p>
            )}

            <div
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                marginBottom: "20px",
              }}
            >
              <h3 style={{ color: "#333" }}>My Image History</h3>
              <input
                type="file"
                accept="image/*"
                onChange={this.handleFileChange}
              />
              <button
                onClick={this.handleImageUpload}
                disabled={!file}
                style={{
                  padding: "8px 15px",
                  border: "none",
                  borderRadius: "5px",
                  backgroundColor: "#007f3f",
                  color: "white",
                  fontWeight: "bold",
                  fontSize: "15px",
                  cursor: "pointer",
                  display: "flex",
                  alignItems: "center",
                  gap: "5px",
                }}
              >
                <FaUpload />
                Upload
              </button>
            </div>

            <div
              style={{
                maxHeight: "400px",
                overflowY: "auto",
                border: "1px solid #ddd",
                borderRadius: "10px",
                padding: "15px",
                backgroundColor: "#f9f9f9",
              }}
            >
              {uploadedImages.map((image) => (
  <div
    key={image.id}
    style={{
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      marginBottom: "15px",
      padding: "10px",
      border: "1px solid #ccc",
      borderRadius: "10px",
      backgroundColor: "#fff",
      boxShadow: "0 2px 5px rgba(0,0,0,0.1)",
    }}
  >
    <div style={{ display: "flex", alignItems: "center" }}>
      <img
        src={image.file}
        alt={`Uploaded ${image.id}`}
        style={{
          width: "80px",
          height: "80px",
          objectFit: "cover",
          borderRadius: "10px",
          marginRight: "15px",
        }}
      />
      <div>
        <p style={{ margin: 0, fontWeight: "bold" }}>Text:</p>
        <p style={{ margin: 0 }}>{image.extracted_text || "No text extracted yet"}</p>
      </div>
    </div>

    <div style={{ display: "flex", flexDirection: "column", gap: "8px", alignItems: "flex-end" }}>
      <select
        value={this.state.selectedModels?.[image.id] || ""}
        onChange={(e) =>
          this.setState((prev) => ({
            selectedModels: {
              ...prev.selectedModels,
              [image.id]: e.target.value,
            },
          }))
        }
        style={{
          padding: "5px",
          borderRadius: "5px",
          width: "150px",
        }}
      >
        <option value="">Select Model</option>
        {(this.state.availableModels || []).map((model) => (
          <option key={model.id} value={model.id}>
            {model.file.split("/").pop()}
          </option>
        ))}
      </select>

      <button
        onClick={() => this.handleExtractText(image.id)}
        style={{
          backgroundColor: "#007f3f",
          color: "white",
          padding: "5px 10px",
          borderRadius: "5px",
          border: "none",
          cursor: "pointer",
        }}
      >
        Extract Text
      </button>

      <button
        onClick={() => this.handleFullText(image.extracted_text)}
        style={{
          backgroundColor: "#007f3f",
          color: "white",
          padding: "5px 10px",
          borderRadius: "5px",
          border: "none",
          cursor: "pointer",
        }}
      >
        Full Text
      </button>
    </div>
  </div>
))}

            </div>
          </div>
        </div>
      </>
    );
  }
}
