import React, { Component } from "react";
import { withRouter } from "react-router-dom";

import { Link } from "react-router-dom";
import {
  MDBCard,
  MDBCardBody,
  MDBInput,
  MDBBtn,
} from "mdb-react-ui-kit";

class LogIn extends Component {
  constructor(props) {
    super(props);
    this.state = {
      identifier: "", // Accepts either email or username
      password: "",
      message: "",
      error: "",
    };

    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleLoginButtonPressed = this.handleLoginButtonPressed.bind(this);
    this.getCookie = this.getCookie.bind(this); // Bind the getCookie function
  }



  // Moved getCookie function outside the constructor
  getCookie(name) {
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

  handleInputChange(e) {
    const { name, value } = e.target;
    this.setState({ [name]: value });
  }

 handleLoginButtonPressed(e) {
  e.preventDefault(); // prevent default behavior
  console.log("🔹 Login button clicked");

  const { identifier, password } = this.state;

  if (!identifier || !password) {
    this.setState({
      error: "Username/Email and password are required.",
      message: "",
    });
    return;
  }

  const csrfToken = this.getCookie("csrftoken");
  console.log("🔹 CSRF Token:", csrfToken);

  const requestOptions = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    credentials: "include", // needed for session authentication
    body: JSON.stringify({ identifier, password }),
  };

 fetch("http://127.0.0.1:8000/api/login/", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
"X-CSRFToken": this.getCookie("csrftoken"),
  },
  credentials: "include",
  body: JSON.stringify({
    identifier: this.state.identifier,
    password: this.state.password,
  }),
})
  .then((res) => res.json())
  .then((data) => {
      if (data.redirect === "researcher-homepage") {
          window.location.href = "/researcher-homepage"; // ✅ Correct path
      } else if (data.redirect === "homepage-user") {
          window.location.href = "/homepage-user";
      } else {
          alert("❌ Login failed or unknown redirect");
      }
  })

    .catch((error) => {
      console.error("❌ Login error:", error);
      this.setState({ error: error.message, message: "" });
    });
  }

  render() {
    const { identifier, password, message, error } = this.state;

    return (
        <div
            style={{
                height: "100vh",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                background: "linear-gradient(to bottom right, #007f3f, #8b8b8b)",
            }}
        >
            <link
                href="https://fonts.googleapis.com/css2?family=Pacifico&family=Lobster&family=Handlee&display=swap"
                rel="stylesheet"/>
            {/* ***** Header Area Start ***** */}
            <header className="header-area header-sticky">
                <div className="container">
                    <div className="row">
                        <div className="col-12">
                            <nav className="main-nav">
                                <Link to="/" style={{fontSize: "65px", fontFamily: "'Lobster', cursive"}}
                                   className="logo">
                                    HIST DOC
                                </Link>
                                {/* ***** Logo End ***** */}
                                {/* ***** Menu Start ***** */}
                                <ul className="nav">
                                    <li className="scroll-to-section">
                                        <Link to="/" style={{fontSize: "40px", fontFamily: "'Roboto', sans-serif"}}
                                           className="active">
                                            Home
                                        </Link>
                                    </li>
                                    <li className="scroll-to-section">
                                        <Link to="/" style={{fontSize: "40px", fontFamily: "'Roboto', sans-serif"}}>
                                            About
                                        </Link>
                                    </li>
                                    <li className="submenu">
                                        <a href="#" style={{fontSize: "40px", fontFamily: "'Roboto', sans-serif"}}>
                                            Sign In/Up
                                        </a>
                                        <ul style={{backgroundColor: "transparent"}}>
                                            <li>
                                                                <Link to="/Register"
                                                  style={{fontSize: "40px",backgroundColor: "rgba(255, 255, 255, 0.5)", color: "black", fontFamily: "'Roboto', sans-serif"}}>
                                              Sign Up
                                            </Link>
                                            <Link to="/LogIn"
                                                  style={{fontSize: "40px", color: "black",backgroundColor: "rgba(255, 255, 255, 0.5)", fontFamily: "'Roboto', sans-serif"}}>
                                              Sing In
                                            </Link>
                                            </li>
                                        </ul>
                                    </li>
                                </ul>
                                <a className="menu-trigger">
                                    <span>Menu</span>
                                </a>
                                {/* ***** Menu End ***** */}
                            </nav>
                        </div>
                    </div>
                </div>
            </header>
            {/* ***** Header Area End ***** */}
            <MDBCard
                className="p-4 shadow-5"
                style={{
                    marginTop: "50px",
                    width: "450px",
                    backgroundColor: "white",
                    border: "2px solid black",
                    borderRadius: "15px",
                }}
            >
                <MDBCardBody className="p-5 text-center">
                    <h2
                        className="fw-bold mb-4"
                        style={{
                            color: "#007f3f",
                                            fontFamily: "'Handlee', cursive",

                        }}
                    >
                        Log In Now
                    </h2>

                    {/* Success or Error Message */}
                    {message && (
                        <p style={{color: "#007f3f", marginBottom: "20px"}}>
                            {message}
                        </p>
                    )}
                    {error && (
                        <p style={{color: "red", marginBottom: "20px"}}>{error}</p>
                    )}

                    {/* Form Inputs */}
                    <MDBInput
                        wrapperClass="mb-3"
                        placeholder="Username or Email"
                        id="form1"
                        type="text"
                        name="identifier"
                        value={identifier}
                        onChange={this.handleInputChange}
                        style={{fontSize: "16px", border: "1px solid #ccc"}}
                    />
                    <MDBInput
                        wrapperClass="mb-3"
                        placeholder="Password"
                        id="form2"
                        type="password"
                        name="password"
                        value={password}
                        onChange={this.handleInputChange}
                        style={{fontSize: "16px", border: "1px solid #ccc"}}
                    />

                    {/* Log In Button */}
                   <MDBBtn
                  className="w-100 mb-3"
                  size="md"
                  onClick={(e) => this.handleLoginButtonPressed(e)}
                  style={{
                    backgroundColor: "#007f3f",
                    color: "white",
                    fontWeight: "bold",
                    fontSize: "16px",
                      height:"40px",
                      width:"60px",
                    border: "none",
                    transition: "background-color 0.3s ease",
                  }}
                  onMouseOver={(e) => {
                    e.target.style.backgroundColor = "#005f30";
                  }}
                  onMouseOut={(e) => {
                    e.target.style.backgroundColor = "#007f3f";
                  }}
                    >
                      Log In
                    </MDBBtn>




                    {/* Link to Sign Up */}
                    <p style={{fontSize: "14px", marginTop: "20px"}}>
                        Don't have an account?{" "}
                        <Link
                            to="/Register"
                            style={{color: "#007f3f", fontWeight: "bold"}}
                        >
                            Sign Up
                        </Link>
                    </p>
                </MDBCardBody>
            </MDBCard>
        </div>
    );
  }
}
// ...your LogIn class
export default withRouter(LogIn);

