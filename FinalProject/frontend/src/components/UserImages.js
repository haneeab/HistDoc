import React, { Component } from "react";
import Navbar from "./Navbar";
import { Link } from "react-router-dom";

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

export default class UserImages extends Component {
  constructor(props) {
    super(props);
    this.state = {
      uploadedImages: [],
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
  }

  handleFullText = (text) => {
    alert(`Full Text: ${text || "No text available"}`);
  };

  handleFeedback = (extractionId) => {
  if (!extractionId) {
    alert("⚠ No extraction found for this image.");
    return;
  }

  this.props.history.push(`/feedback/${extractionId}`);
};


  render() {
    const { uploadedImages } = this.state;

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
              maxWidth: "1000px",
              width: "90%",
              backgroundColor: "white",
              borderRadius: "15px",
              padding: "30px",
              boxShadow: "0 4px 10px rgba(0, 0, 0, 0.2)",
              marginTop: "80px",
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
              My Uploaded Images
            </h2>

            <div
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
                gap: "15px",
                maxHeight: "500px",
                overflowY: "auto",
                padding: "10px",
                border: "1px solid #ddd",
                borderRadius: "10px",
                backgroundColor: "#f7f9fc",
              }}
            >
              {uploadedImages.length > 0 ? (
                uploadedImages.map((image) => (
                    <div
                        key={image.id}
                        style={{
                            display: "flex",
                            flexDirection: "column",
                            alignItems: "center",
                            padding: "15px",
                            border: "1px solid #ccc",
                            borderRadius: "10px",
                            backgroundColor: "#fff",
                            boxShadow: "0 2px 5px rgba(0, 0, 0, 0.1)",
                            textAlign: "center",
                        }}
                    >
                        <img
                            src={image.file}
                            alt={`Uploaded ${image.id}`}
                            style={{
                                width: "100px",
                                height: "100px",
                                borderRadius: "10px",
                                objectFit: "cover",
                                marginBottom: "10px",
                            }}
                        />
                        <p style={{margin: 0, fontWeight: "bold", color: "#333"}}>
                            Extracted Text:
                        </p>
                       <p style={{ margin: "5px 0", color: "#666" }}>
  {(image.extracted_text && image.extracted_text.split(" ").slice(0, 3).join(" ") + "...") || "Processing..."}
</p>

{image.model_used && (
  <p style={{ fontSize: "0.75rem", color: "#999", margin: "5px 0" }}>
    Model used: {image.model_used}
  </p>
)}


                        <div style={{display: "flex", gap: "10px", marginTop: "10px"}}>
                            <button
                                onClick={() => this.handleFullText(image.extracted_text)}
                                style={{
                                    backgroundColor: "#007f3f",
                                    color: "white",
                                    padding: "5px 10px",
                                    borderRadius: "5px",
                                    border: "none",
                                    cursor: "pointer",
                                    fontSize: "0.8rem",
                                }}
                            >
                                Full Text
                            </button>
<Link to={`/feedback/${image.extraction_id}`}>
  <button
    style={{
      backgroundColor: "#007f3f",
      color: "white",
      padding: "5px 10px",
      borderRadius: "5px",
      border: "none",
      cursor: "pointer",
      fontSize: "0.8rem",
    }}
  >
    Feedback
  </button>
</Link>


                        </div>
                    </div>
                ))
              ) : (
                  <p style={{textAlign: "center", color: "#666" }}>
                  No uploaded images found.
                </p>
              )}
            </div>
          </div>
        </div>
      </>
    );
  }
}
