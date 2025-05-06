import React, { Component } from "react";
import Navbar from "./Navbar";

export default class SortedModelsPage extends Component {
  state = {
    models: [],
  };

  componentDidMount() {
    fetch("http://127.0.0.1:8000/api/sorted-models/", {
      credentials: "include",
    })
      .then((res) => res.json())
      .then((data) => this.setState({ models: data }));
  }

  render() {
    const { models } = this.state;

    return (
      <>
        <Navbar />
        <div
          style={{
            minHeight: "100vh",
            paddingTop: "100px",
            background: "linear-gradient(to bottom right, #007f3f, #e6ffe6)",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <h2
            style={{
              color: "#fff",
              marginBottom: "30px",
              fontFamily: "'Handlee', cursive",
              fontSize: "2rem",
              textShadow: "1px 1px 3px rgba(0,0,0,0.2)",
            }}
          >
            📊 Top Rated Models
          </h2>

          {models.map((model, index) => (
            <div
              key={model.id}
              style={{
                backgroundColor: "white",
                width: "90%",
                maxWidth: "600px",
                padding: "20px",
                borderRadius: "15px",
                marginBottom: "20px",
                boxShadow: "0 8px 16px rgba(0,0,0,0.1)",
                transition: "transform 0.2s ease",
              }}
              onMouseEnter={(e) =>
                (e.currentTarget.style.transform = "scale(1.02)")
              }
              onMouseLeave={(e) =>
                (e.currentTarget.style.transform = "scale(1)")
              }
            >
              <h3
                style={{
                  marginBottom: "10px",
                  color: "#007f3f",
                  fontSize: "20px",
                }}
              >
                {index + 1}. {model.name.split("/").pop()}
              </h3>
              <p style={{ margin: 0, fontSize: "16px", color: "#333" }}>
                <span style={{ fontSize: "18px", color: "#ffc107" }}>
                  {"⭐".repeat(Math.round(model.average_rating))}
                </span>{" "}
                ({model.average_rating})
              </p>
            </div>
          ))}
        </div>
      </>
    );
  }
}
