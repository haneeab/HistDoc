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
                                        <a
                                            href="#"
                                            style={{fontSize: "37px", fontFamily: "'Roboto', sans-serif"}}
                                        >
                                            👤My Account
                                        </a>

                                        <ul
                                            style={{
                                                position: "absolute",

                                                top: "100%",
                                                left: "60px", // shifted to the left
                                                backgroundColor: "rgba(255, 255, 255, 0.1)", // light transparent white
                                                backdropFilter: "blur(10px)", // frost effect
                                                WebkitBackdropFilter: "blur(10px)", // Safari support
                                                padding: "10px",
                                                borderRadius: "12px",
                                                listStyle: "none",
                                                margin: 0,
                                                minWidth: "180px",
                                                boxShadow: "0 8px 20px rgba(0, 0, 0, 0.2)",
                                                border: "1px solid rgba(255, 255, 255, 0.3)",
                                            }}
                                        >
                                            <li>
                                                <Link
                                                    to="/Register"
                                                    style={{
                                                        display: "flex",
                                                        alignItems: "center",
                                                        gap: "10px",
                                                        fontSize: "25px",
                                                        backgroundColor: "rgba(255, 255, 255, 0.1)", // light transparent white
                                                        backdropFilter: "blur(10px)", // frost effect
                                                        WebkitBackdropFilter: "blur(10px)", // Safari support
                                                        padding: "10px 15px",
                                                        fontFamily: "'Roboto', sans-serif",
                                                        color: "#007f3f",
                                                        textDecoration: "none",
                                                        borderRadius: "8px",
                                                    }}
                                                >
                                                    📝 Sign Up
                                                </Link>
                                            </li>
                                            <li>
                                                <Link
                                                    to="/LogIn"
                                                    style={{
                                                        display: "flex",
                                                        alignItems: "center",
                                                        gap: "10px",
                                                        fontSize: "25px",
                                                        padding: "10px 15px",
                                                        backgroundColor: "rgba(255, 255, 255, 0.1)", // light transparent white
                                                        backdropFilter: "blur(10px)", // frost effect
                                                        WebkitBackdropFilter: "blur(10px)", // Safari support
                                                        fontFamily: "'Roboto', sans-serif",
                                                        color: "#007f3f",
                                                        textDecoration: "none",
                                                        borderRadius: "8px",
                                                    }}
                                                >
                                                    🔐 Sign In
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
                    fontFamily: "'Open Sans', 'Roboto', sans-serif",
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
                        style={{fontSize: "18px", border: "1px solid #ccc"}}
                    />
                    <MDBInput
                        wrapperClass="mb-3"
                        placeholder="Password"
                        id="form2"
                        type="password"
                        name="password"
                        value={password}
                        onChange={this.handleInputChange}
                        style={{fontSize: "18px", border: "1px solid #ccc"}}
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
                            fontSize: "19px",
                            height: "40px",
                            width: "60px",
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
                    <p style={{fontSize: "18px", marginTop: "20px"}}>
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

