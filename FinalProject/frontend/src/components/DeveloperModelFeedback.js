import React, { Component } from "react";
import NavbarDev from "./NavbarDev";

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

export default class DeveloperModelFeedback extends Component {
  state = {
    feedbacks: [],
    averageRating: null,
    modelName: "",
  };

  componentDidMount() {
    const queryParams = new URLSearchParams(this.props.location.search);
    const model_id = queryParams.get("model_id");

    fetch(`http://127.0.0.1:8000/api/model-feedbacks/?model_id=${model_id}`, {
      credentials: "include",
      headers: { "X-CSRFToken": getCookie("csrftoken") },
    })
      .then((res) => res.json())
      .then((data) => {
        this.setState({
          feedbacks: data.feedbacks,
          averageRating: data.average_rating,
          modelName: data.model_name,
        });
      });
  }

  render() {
    const { feedbacks, averageRating, modelName } = this.state;

    return (
      <>
        <NavbarDev />
          <div
              style={{
                  border: "1px solid #007f3f",
                  borderRadius: "10px",
                  padding: "15px",
                  marginBottom: "15px",
                  background: "linear-gradient(to bottom right, #007f3f, #8b8b8b)", // light green background
                  boxShadow: "0 2px 6px rgba(0, 0, 0, 0.1)",
              }}



              // minHeight: "100vh",
              // display: "flex",
              // justifyContent: "center",
              // alignItems: "center",
              // background: "linear-gradient(to bottom top, #007f3f, #8b8b8b)",
              // padding: "2rem",
              // paddingTop:"90px",

              >
              <h2 style={{color: "tan", textAlign: "left", marginTop: "75px"}}>
                  Feedback for Model: <span style={{fontWeight: "normal"}}>{modelName}</span>
              </h2>
              {averageRating && (
                  <h4 style={{textAlign: "center", color: "tan"}}>
                      ⭐ Average Rating: <strong>{averageRating}</strong> / 5
                  </h4>
              )}
              <div style={{marginTop: "30px"}}>
                  {feedbacks.length === 0 ? (
                      <p>No feedback submitted yet.</p>
                  ) : (
                      feedbacks.map((fb) => (
                          <div
                              key={fb.id}
                              style={{
                                  border: "1px solid #ccc",
                                  borderRadius: "10px",
                                  padding: "15px",
                                  marginBottom: "15px",
                                  backgroundColor: "#f9f9f9",
                              }}
                          >
                              <p><strong>User:</strong> {fb.username}</p>
                              <p style={{color: "#ffc107", fontWeight: "bold"}}>
                                  {"⭐".repeat(fb.rating)} ({fb.rating})
                              </p>
                              <p><strong>Feedback:</strong> {fb.feedback}</p>
                              <p style={{fontSize: "0.8rem", color: "#888"}}>
                                  Submitted on {new Date(fb.created_at).toLocaleString()}
                              </p>
                          </div>
                      ))
                  )}
              </div>
          </div>
      </>
    );
  }
}
