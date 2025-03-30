import React, { Component } from "react";
import Navbar from "./Navbar";
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
    };
  }

  handleFileChange = (e) => {
    this.setState({ file: e.target.files[0] });
  };
handleImageUpload = () => {
  const { file } = this.state;
  if (!file) {
    alert("🚨 No file selected!");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);
  formData.append("file_type", "image");

  // ✅ Log to verify values are being appended
  for (let pair of formData.entries()) {
    console.log("📝 FormData:", pair[0], pair[1]);
  }

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
      if (!res.ok) {
        throw new Error(data.error || "Upload failed");
      }

      alert("✅ File uploaded!");
      console.log(data);

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
  this.setState({ message: "🔄 Running inference..." });

  try {
    const response = await fetch(`http://127.0.0.1:8000/api/run-inference/${imageId}/`, {
      method: "POST",
      credentials: "include",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Inference failed");
    }

    // ✅ Update that specific image in state
    this.setState((prevState) => ({
      uploadedImages: prevState.uploadedImages.map((img) =>
        img.id === imageId
          ? {
              ...img,
              src: data.original_image,
              text: "✔ Text extracted!",
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
            height: "100vh",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            background: "linear-gradient(to bottom right, #007f3f, #8b8b8b)",
          }}
        >
            <div
                style={{
                    marginTop: "80px",
                    maxWidth: "800px",
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

                <div>
                    <div
                        style={{
                            display: "flex",
                            alignItems: "center",
                            justifyContent: "space-between",
                            marginBottom: "15px",
                        }}
                    >
                        <h3 style={{color: "#333"}}>My Image Historcdcsdcy</h3>
                        <input
                            type="file"
                            accept="image/*"
                            onChange={(e) => this.setState({file: e.target.files[0]})}
                        />
                        <button
                            onClick={this.handleImageUpload}
                            disabled={!this.state.file}
                        >
                            Upload
                        </button>


                        {uploadedImages.map((image) => (
                            <div key={image.id}>
                                <button
                                    onClick={() => this.handleExtractText(image.id)}
                                    style={{
                                        padding: "5px 10px",
                                        border: "none",
                                        borderRadius: "5px",
                                        backgroundColor: "#007f3f",
                                        color: "white",
                                        fontWeight: "bold",
                                        cursor: "pointer",
                                        marginTop: "10px",
                                    }}
                                >
                                    Extract Text
                                </button>
                            </div>
                        ))}

                    </div>
                </div>
                <p style={{margin: 0, color: "#666"}}>{image.text}</p>
                {image.output && (
                  <img
                    src={image.output}
                    alt="Output"
                    style={{
                      width: "100px",
                      marginTop: "10px",
                      borderRadius: "10px",
                      border: "1px solid #aaa",
                    }}
                  />
                )}

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
                    {uploadedImages.map((image) => (
                        <div
                            key={image.id}
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
                            <div style={{display: "flex", alignItems: "center"}}>
                                <img
                                    src={image.src}
                                    alt={`Uploaded ${image.id}`}
                                    style={{
                                        width: "80px",
                                        height: "80px",
                                        borderRadius: "10px",
                                        objectFit: "cover",
                                        marginRight: "15px",
                                    }}
                                />
                                <div>
                                    <p style={{margin: 0, fontWeight: "bold", color: "#333"}}>
                                        Extracted Text:
                                    </p>
                                    <p style={{margin: 0, color: "#666"}}>{image.text}</p>
                                </div>
                            </div>
                            <button
                                onClick={() => this.handleFullText(image.text)}
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
                                Full Textttt
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