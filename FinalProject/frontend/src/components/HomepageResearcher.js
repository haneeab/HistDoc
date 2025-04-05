import React, { Component } from "react";
import NavbarDev from "./NavbarDev";
import {FaUpload} from "react-icons/fa";

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

export default class HomepageResearcher extends Component {
  constructor(props) {
    super(props);
    this.state = {
      uploadedModels: [],
      file: null,
      message: "",
    };
  }

  handleFileChange = (e) => {
    this.setState({ file: e.target.files[0] });
  };

  handleModelUpload = () => {
    const { file } = this.state;
    if (!file) {
      alert("🚨 No file selected!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("file_type", "model");

    fetch("http://127.0.0.1:8000/api/upload-developer-file/", {
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

        alert("✅ Model uploaded!");

        this.setState((prev) => ({
          uploadedModels: [
            ...prev.uploadedModels,
            {
              id: data.id,
              name: file.name,
              message: "✔ Ready to use!",
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
componentDidMount() {
  fetch("http://127.0.0.1:8000/api/developer-models/", {
    method: "GET",
    credentials: "include",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
    },
  })
    .then((res) => res.json())
    .then((data) => {
      const models = data.map((item) => ({
        id: item.id,
        name: item.file.split("/").pop(), // get just the filename
        message: `✔ File uploaded!`,       // ✅ safe default message
      }));
      this.setState({ uploadedModels: models });
    })
    .catch((err) => {
      console.error("Error fetching models:", err);
    });
}

  render() {
    const { uploadedModels, file, message } = this.state;

    return (
      <>
        <NavbarDev />
        <div
          style={{
            minHeight: "100vh",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            background: "linear-gradient(to bottom right, #007f3f, #8b8b8b)",
            padding: "2rem",
              paddingTop:"90px",
          }}
        >
          <div
            style={{
              maxWidth: "1000px",
              width: "100%",
              backgroundColor: "white",
              borderRadius: "15px",
              padding: "20px",
              boxShadow: "0 4px 10px rgba(0, 0, 0, 0.2)",
              position: "relative",
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
              Welcome Developer
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
                marginBottom: "15px",
              }}
            >
              <h3 style={{ color: "#333" }}>My Uploaded Models</h3>
              <input
                type="file"
                accept=".pt,.py"
                onChange={this.handleFileChange}
              />
              <button
                onClick={this.handleModelUpload}
                disabled={!file}
                style={{
                  padding: "5px 10px",
                  border: "none",
                  borderRadius: "5px",
                  backgroundColor: "#007f3f",
                  color: "white",
                  fontWeight: "bold",
                  cursor: "pointer",
                }}
              >
                  <FaUpload />
                Upload
              </button>
            </div>

            <div
              style={{
                maxHeight: "300px",
                overflowY: "auto",
                padding: "10px",
                border: "1px solid #ddd",
                borderRadius: "10px",
                backgroundColor: "#f7f9fc",
              }}
            >
              {uploadedModels.map((model) => (
                <div
                  key={model.id}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                    marginBottom: "10px",
                    padding: "10px",
                    border: "1px solid #ccc",
                    borderRadius: "10px",
                    backgroundColor: "#fff",
                    boxShadow: "0 2px 5px rgba(0, 0, 0, 0.1)",
                  }}
                >
                  <div>
                    <p style={{ margin: 0, fontWeight: "bold", color: "#333" }}>
                      Model File:
                    </p>
                    <p style={{ margin: 0, color: "#666" }}>{model.name}</p>
                    <p style={{ margin: 0, color: "green" }}>{model.message}</p>
                  </div>
                  <button
                    style={{
                      padding: "5px 10px",
                      border: "none",
                      borderRadius: "5px",
                      backgroundColor: "#007f3f",
                      color: "white",
                      fontWeight: "bold",
                      cursor: "pointer",
                    }}
                    onClick={() =>
                      alert(`Model ${model.name} is ready to use!`)
                    }
                  >
                    Use Model
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      </>
    );
  }
}
