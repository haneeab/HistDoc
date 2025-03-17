import React, { Component } from "react";
import { Link } from "react-router-dom";
import {
  MDBCard,
  MDBCardBody,
  MDBRow,
  MDBCol,
  MDBInput,
  MDBBtn,
} from "mdb-react-ui-kit";

export default class Register extends Component {
  constructor(props) {
    super(props);
    this.state = {
      username: "",
      firstName: "",
      lastName: "",
      email: "",
      password: "",
      rePassword: "",
      message: "",
      error: "",
      isSquare: false,
    };

    this.handleRegisterButtonPressed = this.handleRegisterButtonPressed.bind(this);
    this.handleInputChange = this.handleInputChange.bind(this);
    this.toggleButtonShape = this.toggleButtonShape.bind(this);
  }

  // Moved getCookie function outside constructor
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
    this.setState({
      [name]: value,
    });
  }

  toggleButtonShape(isSquare) {
    this.setState({ isSquare });
  }

  handleRegisterButtonPressed() {
    const { username, firstName, lastName, email, password, rePassword } = this.state;

    // Client-side validation for password match
    if (password !== rePassword) {
      this.setState({
        error: "Passwords do not match.",
        message: "",
      });
      return;
    }

    // API request for registration
    const requestOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": this.getCookie("csrftoken"), // Fixed reference to getCookie
      },
      body: JSON.stringify({
        username,
        first_name: firstName,
        last_name: lastName,
        email,
        password,
      }),
    };

    fetch("/api/register/", requestOptions)
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
        return response.json().then((err) => {
          throw new Error(err.error || "Failed to register user.");
        });
      })
      .then((data) => {
        this.setState({
          message: data.message || "User registered successfully!",
          error: "",
          username: "",
          firstName: "",
          lastName: "",
          email: "",
          password: "",
          rePassword: "",
        });
      })
      .catch((error) => {
        this.setState({
          message: "",
          error: error.message,
        });
      });
  }

  render() {
    const { username, firstName, lastName, email, password, rePassword, message, error } =
      this.state;

    return (
        <div
            style={{
              height: "110vh",
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
                        <Link to="/#about" style={{fontSize: "40px", fontFamily: "'Roboto', sans-serif"}}>
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
                                  style={{
                                    fontSize: "40px",
                                    backgroundColor: "rgba(255, 255, 255, 0.5)",
                                    color: "black",
                                    fontFamily: "'Roboto', sans-serif"
                                  }}>
                              Sign Up
                            </Link>
                            <Link to="/LogIn"
                                  style={{
                                    fontSize: "40px",
                                    color: "black",
                                    backgroundColor: "rgba(255, 255, 255, 0.5)",
                                    fontFamily: "'Roboto', sans-serif"
                                  }}>
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
                borderRadius: "10px",
                height: "480px",
              }}
          >
            <MDBCardBody className="p-4 text-center">
              <h2
                  className="fw-bold mb-4"
                  style={{
                    color: "#007f3f",
                    fontFamily: "'Handlee', cursive",

                  }}
              >
                Sign Up Now
              </h2>

              {/* Success or Error Message */}
              {error && <p style={{color: "red", marginTop: "10px"}}>{error}</p>}
              {message && <p style={{color: "green", marginTop: "10px"}}>{message}</p>}

              {/* Form Inputs */}
              <MDBRow>
                <MDBCol col="6">
                  <MDBInput
                      wrapperClass="mb-3"
                      placeholder="First Name"
                      id="form1"
                      type="text"
                      name="firstName"
                      value={firstName}
                      onChange={this.handleInputChange}
                      style={{fontSize: "14px", border: "1px solid #ccc"}}
                  />
                </MDBCol>

                <MDBCol col="6">
                  <MDBInput
                      wrapperClass="mb-3"
                      placeholder="Last Name"
                      id="form2"
                      type="text"
                      name="lastName"
                      value={lastName}
                      onChange={this.handleInputChange}
                      style={{fontSize: "14px", border: "1px solid #ccc"}}
                  />
                </MDBCol>
              </MDBRow>

              <MDBInput
                  wrapperClass="mb-3"
                  placeholder="Email"
                  id="form3"
                  type="email"
                  name="email"
                  value={email}
                  onChange={this.handleInputChange}
                  style={{fontSize: "14px", border: "1px solid #ccc"}}
              />
              <MDBInput
                  wrapperClass="mb-3"
                  placeholder="Username"
                  id="form4"
                  type="text"
                  name="username"
                  value={username}
                  onChange={this.handleInputChange}
                  style={{fontSize: "14px", border: "1px solid #ccc"}}
              />
              <MDBInput
                  wrapperClass="mb-3"
                  placeholder="Password"
                  id="form5"
                  type="password"
                  name="password"
                  value={password}
                  onChange={this.handleInputChange}
                  style={{fontSize: "14px", border: "1px solid #ccc"}}
              />
              <MDBInput
                  wrapperClass="mb-3"
                  placeholder="Re-enter Password"
                  id="form6"
                  type="password"
                  name="rePassword"
                  value={rePassword}
                  onChange={this.handleInputChange}
                  style={{fontSize: "14px", border: "1px solid #ccc"}}
              />

              {/* Sign Up Button */}
              <MDBBtn
                  className="w-100 mb-3"
                  size="md"
                  onClick={this.handleRegisterButtonPressed}
                  style={{
                    backgroundColor: "#007f3f",
                    color: "white",
                    fontWeight: "bold",
                    height: "45px",
                    border: "none",
                  }}
              >
                Sign Up
              </MDBBtn>

              {/* Link to Log In */}
              <p style={{fontSize: "14px", marginTop: "10px"}}>
                Already have an account?{" "}
                <Link to="/LogIn" style={{color: "#007f3f", fontWeight: "bold"}}>
                  Log In
                </Link>
              </p>
            </MDBCardBody>
          </MDBCard>
        </div>
    );
  }
}
