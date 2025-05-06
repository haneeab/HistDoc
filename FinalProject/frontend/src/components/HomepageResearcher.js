import React, { Component } from "react";
import NavbarDev from "./NavbarDev";
import { Link } from "react-router-dom";
import { FaUpload } from "react-icons/fa";

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
      name: "",
      description: "",
      message: "",
        parameters: [],

    };
  }
handleParamChange = (index, field, value) => {
  const updated = [...this.state.parameters];
  updated[index][field] = value;
  this.setState({ parameters: updated });
};

addParameter = () => {
  this.setState((prev) => ({
    parameters: [...prev.parameters, { name: "", type: "", choices: "" }],
  }));
};

removeParameter = (index) => {
  const updated = [...this.state.parameters];
  updated.splice(index, 1);
  this.setState({ parameters: updated });
};

  handleFileChange = (e) => {
    this.setState({ file: e.target.files[0] });
  };

  handleInputChange = (e) => {
    this.setState({ [e.target.name]: e.target.value });
  };

  handleModelUpload = () => {
    const { file, name, description } = this.state;
    if (!file) {
      alert("🚨 No file selected!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("name", name);
    formData.append("description", description);
    formData.append("parameters", JSON.stringify(this.state.parameters));  // 🆕


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
              name: name,
              description: description,
              fileName: file.name,
              message: "✔ Ready to use!",
            },
          ],
          file: null,
          name: "",
          description: "",
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
          const isValid = this.state.parameters.every(p => p.name && p.type);
if (!isValid) {
  alert("❌ Please fill in all parameter names and types.");
  return;
}

        const models = data.map((item) => ({
          id: item.id,
          name: item.name || item.file.split("/").pop(),
          description: item.description || "No description provided.",
          fileName: item.file.split("/").pop(),
          message: "✔ File uploaded!",
        }));
        this.setState({ uploadedModels: models });
      })
      .catch((err) => {
        console.error("Error fetching models:", err);
      });
  }

  render() {
    const { uploadedModels, file, name, description, message } = this.state;

    return (
      <>
        <NavbarDev />
        <div
          style={{
            minHeight: "100vh",
            background: "linear-gradient(to bottom right, #007f3f, #8b8b8b)",
            padding: "90px 2rem 2rem",
            display: "flex",
            justifyContent: "center",
            alignItems: "start",
          }}
        >
            <div
                style={{
                    maxWidth: "900px",
                    width: "100%",
                    backgroundColor: "white",
                    borderRadius: "15px",
                    padding: "30px",
                    boxShadow: "0 4px 12px rgba(0,0,0,0.15)",
                }}
            >
                <h2 style={{textAlign: "center", color: "#007f3f", fontFamily: "Segoe UI", marginBottom: "20px"}}>
                    Welcome Developer
                </h2>

                <div style={{marginBottom: "30px"}}>
                    <label style={{fontWeight: "bold"}}>Model Name:</label>
                    <input
                        type="text"
                        name="name"
                        value={name}
                        onChange={this.handleInputChange}
                        placeholder="Enter model name..."
                        style={{
                            width: "100%",
                            padding: "10px",
                            marginBottom: "15px",
                            borderRadius: "8px",
                            border: "1px solid #ccc"
                        }}
                    />
                    <label style={{fontWeight: "bold"}}>Model Description:</label>
                    <textarea
                        name="description"
                        value={description}
                        onChange={this.handleInputChange}
                        placeholder="Write a brief description..."
                        style={{
                            width: "100%",
                            padding: "10px",
                            borderRadius: "8px",
                            border: "1px solid #ccc",
                            minHeight: "100px"
                        }}
                    ></textarea>
                </div>
                <h3 style={{color: "#333"}}>⚙️ Model Parameters</h3>
                {this.state.parameters.map((param, index) => (
                    <div key={index} style={{
                        marginBottom: "10px",
                        padding: "10px",
                        border: "1px dashed #ccc",
                        borderRadius: "8px"
                    }}>
                        <input
                            type="text"
                            placeholder="Parameter Name"
                            value={param.name}
                            onChange={(e) => this.handleParamChange(index, "name", e.target.value)}
                            style={{marginRight: "10px", padding: "6px", width: "30%"}}
                        />
                        <select
                            value={param.type}
                            onChange={(e) => this.handleParamChange(index, "type", e.target.value)}
                            style={{marginRight: "10px", padding: "6px", width: "20%"}}
                        >
                            <option value="">Type</option>
                            <option value="str">str</option>
                            <option value="int">int</option>
                            <option value="float">float</option>
                            <option value="bool">bool</option>
                        </select>

                        <input
                            type="text"
                            placeholder="Choices (comma-separated)"
                            value={param.choices}
                            onChange={(e) => this.handleParamChange(index, "choices", e.target.value)}
                            style={{padding: "6px", width: "30%"}}
                        />
                        <button
                            onClick={() => this.removeParameter(index)}
                            style={{
                                marginLeft: "10px",
                                padding: "5px",
                                backgroundColor: "#ff4d4d",
                                color: "white",
                                border: "none",
                                borderRadius: "5px"
                            }}
                        >
                            ❌
                        </button>
                    </div>
                ))}
                <button
                    type="button"
                    onClick={this.addParameter}
                    style={{
                        padding: "8px 15px",
                        backgroundColor: "#007f3f",
                        color: "white",
                        border: "none",
                        borderRadius: "6px",
                        marginBottom: "20px"
                    }}
                >
                    ➕ Add Parameter
                </button>

                <div style={{display: "flex", alignItems: "center", gap: "10px", marginBottom: "30px"}}>
                    <input type="file" accept=".pt,.py" onChange={this.handleFileChange}/>
                    <button
                        onClick={this.handleModelUpload}
                        disabled={!file}
                        style={{
                            padding: "10px 15px",
                            backgroundColor: "#007f3f",
                            color: "white",
                            borderRadius: "8px",
                            border: "none",
                            fontWeight: "bold",
                            display: "flex",
                            alignItems: "center",
                            gap: "5px",
                        }}
                    >
                        <FaUpload/> Upload
                    </button>
                </div>

                <h3 style={{color: "#333", marginBottom: "20px"}}>📁 Uploaded Models</h3>
                <div style={{display: "flex", flexDirection: "column", gap: "15px"}}>
                    {uploadedModels.map((model) => (
                        <div
                            key={model.id}
                            style={{
                                background: "#f8f9fa",
                                padding: "15px 20px",
                                borderRadius: "10px",
                                border: "1px solid #ddd",
                                boxShadow: "0 2px 5px rgba(0,0,0,0.05)",
                            }}
                        >
                            <p style={{margin: 0, fontWeight: "bold", color: "#007f3f", fontSize: "16px"}}>
                                📝 {model.name}
                            </p>
                            {model.description && (
                                <p style={{margin: "5px 0", color: "#555"}}>{model.description}</p>
                            )}
                            <p style={{margin: "5px 0", color: "#888", fontStyle: "italic"}}>
                                File: {model.fileName}
                            </p>
                           <Link
                      to={`/developer-test-model?model_id=${model.id}`}
                      style={{
                        marginTop: "10px",
                        display: "inline-block",
                        padding: "6px 12px",
                        backgroundColor: "#007f3f",
                        color: "white",
                        border: "none",
                        borderRadius: "5px",
                        fontSize: "14px",
                        textDecoration: "none",
                        textAlign: "center",
                      }}
                    >
                      ✅ Use Model
                    </Link>

                        </div>
                    ))}
                </div>
            </div>
        </div>
      </>
    );
  }
}
