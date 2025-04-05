import React, { Component } from "react";
import { withRouter } from "react-router-dom";
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

class FeedbackPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      feedback: "",
      rating: "",
      message: "",
    };
  }



handleSubmit = async (e) => {
  e.preventDefault();

  const extractionId = this.props.match.params.extractionId;
  const { feedback, rating } = this.state;

  try {
    const response = await fetch("http://127.0.0.1:8000/api/submit-feedback/", {
      method: "POST",
      credentials: "include",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
        "Content-Type": "application/json",
      },
   body: JSON.stringify({
  extraction_id: this.props.match.params.extraction_id,  // ✅ fix here
  rating: rating,
  feedback: feedback,
}),


    });

    const data = await response.json();

    if (!response.ok) throw new Error(data.error || "Failed to submit feedback");

this.props.history.push("/user-images");
  } catch (err) {
    this.setState({ message: "❌ Error: " + err.message });
  }
};

  render() {
    const { feedback, rating, message } = this.state;

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
              width: "100%",
              maxWidth: "600px",
              backgroundColor: "white",
              borderRadius: "15px",
              padding: "30px",
                marginTop:"20px",
              boxShadow: "0 4px 10px rgba(0, 0, 0, 0.2)",
            }}
          >
            <h2 style={{ textAlign: "center", marginBottom: "20px", color: "#007f3f" }}>
              Leave Feedback for a better model
            </h2>

            {message && (
              <p style={{ textAlign: "center", color: message.includes("✅") ? "green" : "red" }}>
                {message}
              </p>
            )}

              <form onSubmit={this.handleSubmit}>
                  <div style={{marginBottom: "15px"}}>
                      <label style={{fontWeight: "bold"}}>Feedback:</label>
                      <textarea
                          required
                          value={feedback}
                          onChange={(e) => this.setState({feedback: e.target.value})}
                          style={{
                              width: "100%",
                              minHeight: "100px",
                              padding: "10px",
                              borderRadius: "5px",
                              border: "1px solid #ccc",
                          }}
                      />
                  </div>

                  <div style={{marginBottom: "15px"}}>
                      <label style={{fontWeight: "bold"}}>Rating (1-5):</label>
                      <input
                          type="number"
                          required
                          min="1"
                          max="5"
                          value={rating}
                          onChange={(e) => this.setState({rating: e.target.value})}
                          style={{
                              width: "100%",
                              padding: "10px",
                              borderRadius: "5px",
                              border: "1px solid #ccc",
                          }}
                      />
                  </div>

                  <button
                      type="submit"
                      style={{
                          width: "100%",
                          padding: "10px",
                          backgroundColor: "#007f3f",
                          color: "white",
                          border: "none",
                          borderRadius: "5px",
                          fontWeight: "bold",
                          cursor: "pointer",
                      }}
                  >
                      Submit Feedback
                  </button>

              </form>
          </div>
        </div>
      </>
    );
  }
}

export default withRouter(FeedbackPage);
