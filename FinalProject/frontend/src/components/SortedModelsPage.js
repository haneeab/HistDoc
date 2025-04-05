// SortedModelsPage.js
import React, { Component } from "react";
import NavbarDev from "./NavbarDev";

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
    return (
      <>
        <NavbarDev />
        <div style={{ padding: "80px 20px", background: "linear-gradient(to bottom right, #007f3f, #8b8b8b)", minHeight: "100vh" }}>
          <h2 style={{ textAlign: "left", color: "tan",marginTop:"10px" }}>
            📊 Models Ordered by Average Rating
          </h2>
          {this.state.models.map((model, index) => (
            <div
              key={model.id}
              style={{
                background: "white",
                padding: "15px",
                margin: "20px auto",
                maxWidth: "600px",
                borderRadius: "10px",
                boxShadow: "0 2px 5px rgba(0,0,0,0.1)",
              }}
            >
              <h3 style={{ color: "#007f3f" }}>{index + 1}. {model.name}</h3>
<p>
  {Array(Math.round(model.average_rating)).fill("⭐").join("")}
  {" "}
  ({model.average_rating})
</p>
            </div>
          ))}
        </div>
      </>
    );
  }
}
