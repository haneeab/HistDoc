import React, { Component } from "react";
import NavbarDev from "./NavbarDev";
import { Link } from "react-router-dom";

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
  return null;
}

export default class DeveloperModelsPage extends Component {
  state = {
    models: [],
  };

  componentDidMount() {
    fetch("http://127.0.0.1:8000/api/developer-models/", {
      method: "GET",
      credentials: "include",
      headers: { "X-CSRFToken": getCookie("csrftoken") },
    })
      .then((res) => res.json())
      .then((data) => {
        const models = data.map((item) => ({
          id: item.id,
          name: item.file.split("/").pop(),
        }));
        this.setState({ models });
      });
  }

  handleDelete = (id) => {
    if (!window.confirm("Are you sure you want to delete this model?")) return;

    fetch(`http://127.0.0.1:8000/api/delete-developer-model/${id}/`, {
      method: "DELETE",
      credentials: "include",
      headers: { "X-CSRFToken": getCookie("csrftoken") },
    })
      .then((res) => res.json())
      .then(() => {
        this.setState((prev) => ({
          models: prev.models.filter((model) => model.id !== id),
        }));
      });
  };

  render() {
    const { models } = this.state;

    return (
      <>
        <NavbarDev />
          <div
              style={{

                  minHeight: "100vh",
                  background: "linear-gradient(to bottom right, #007f3f, #8b8b8b)", // light green background
                  paddingBottom: "100px",
                  position: "relative",
              }}
          >
              {/* Green wave effect */}
              {/* Green wave at bottom */}
              <svg
                  style={{
                      position: "absolute",
                      bottom: 0,
                      left: 0,
                      width: "100%",
                      height: "180px",
                  }}
                  viewBox="0 0 1440 320"
                  preserveAspectRatio="none"
              >
                  <defs>
                      <linearGradient id="greenToWhite" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="0%" stopColor="#007f3f"/>
                          <stop offset="50%" stopColor="#cceedd"/>
                          <stop offset="100%" stopColor="#ffffff"/>
                      </linearGradient>
                  </defs>
                  <path
                      fill="url(#greenToWhite)"
                      d="M0,160L60,144C120,128,240,96,360,90.7C480,85,600,107,720,128C840,149,960,171,1080,176C1200,181,1320,171,1380,165.3L1440,160L1440,320L1380,320C1320,320,1200,320,1080,320C960,320,840,320,720,320C600,320,480,320,360,320C240,320,120,320,60,320L0,320Z"
                  ></path>
              </svg>


              <div style={{padding: "100px 2rem 2rem",}}>


                  <div style={{maxWidth: "800px", margin: "0 auto",marginTop:"50px",
}}>
                      {models.map((model) => (
                          <div
                              key={model.id}
                              style={{
                                  background: "white",
                                  padding: "15px",
                                  marginBottom: "15px",
                                  borderRadius: "10px",
                                  boxShadow: "0 2px 5px rgba(0,0,0,0.1)",
                                  display: "flex",
                                  justifyContent: "space-between",
                                  alignItems: "center",
                              }}
                          >
                              <div>
                                  <p style={{fontWeight: "bold", marginBottom: "5px", color: "#007f3f"}}>
                                      {model.name}
                                  </p>
                                  <div style={{display: "flex", gap: "10px"}}>
                                      <Link
                                          to={`/developer-feedbacks?model_id=${model.id}`}
                                          style={{
                                              textDecoration: "none",
                                              backgroundColor: "#007f3f",
                                              color: "white",
                                              padding: "5px 10px",
                                              borderRadius: "5px",
                                              fontSize: "14px",
                                              fontWeight: "bold",
                                          }}
                                      >
                                          🔍 View Feedback
                                      </Link>
                                      <Link
                                          to={`/developer-test-model?model_id=${model.id}`}
                                          style={{
                                              textDecoration: "none",
                                              backgroundColor: "#005a2f",
                                              color: "white",
                                              padding: "5px 10px",
                                              borderRadius: "5px",
                                              fontSize: "14px",
                                              fontWeight: "bold",
                                          }}
                                      >
                                          🧪 Test Model
                                      </Link>
                                  </div>
                              </div>

                              <button
                                  onClick={() => this.handleDelete(model.id)}
                                  style={{
                                      padding: "5px 10px",
                                      backgroundColor: "#ff4d4d",
                                      color: "white",
                                      border: "none",
                                      borderRadius: "5px",
                                      cursor: "pointer",
                                  }}
                              >
                                  🗑 Delete
                              </button>
                          </div>
                      ))}
                  </div>
              </div>

              {/* Upload Icon Button (Bottom Right) */}
              <Link
                  to="/researcher-homepage"
                  title="Upload New Model"
                  style={{
                      position: "fixed",
                      bottom: "30px",
                      right: "30px",
                      backgroundColor: "#007f3f",
                      color: "white",
                      fontSize: "30px",
                      padding: "15px",
                      borderRadius: "50%",
                      textAlign: "center",
                      textDecoration: "none",
                      boxShadow: "0 4px 10px rgba(0,0,0,0.3)",
                  }}
              >
                  ⬆
              </Link>
          </div>
      </>
    );
  }
}
