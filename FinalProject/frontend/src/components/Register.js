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
  .then((response) =>
    response.json().then((data) => {
      if (!response.ok) {
        throw new Error(data.error || Object.values(data.details).flat().join(" ") || "Registration failed.");
      }
      return data;
    })
  )
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

    setTimeout(() => {
      this.props.history.push("/LogIn");
    }, 1500);
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
                marginTop: "15px",
                width: "460px",
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
                    fontFamily: "'Open Sans', 'Roboto', sans-serif",

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
                      style={{fontSize: "16px", border: "1px solid #ccc"}}
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
                      style={{fontSize: "16px", border: "1px solid #ccc"}}
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
                  style={{fontSize: "16px", border: "1px solid #ccc"}}
              />
              <MDBInput
                  wrapperClass="mb-3"
                  placeholder="Username"
                  id="form4"
                  type="text"
                  name="username"
                  value={username}
                  onChange={this.handleInputChange}
                  style={{fontSize: "16px", border: "1px solid #ccc"}}
              />
              <MDBInput
                  wrapperClass="mb-3"
                  placeholder="Password"
                  id="form5"
                  type="password"
                  name="password"
                  value={password}
                  onChange={this.handleInputChange}
                  style={{fontSize: "16px", border: "1px solid #ccc"}}
              />
              <MDBInput
                  wrapperClass="mb-3"
                  placeholder="Re-enter Password"
                  id="form6"
                  type="password"
                  name="rePassword"
                  value={rePassword}
                  onChange={this.handleInputChange}
                  style={{fontSize: "16px", border: "1px solid #ccc"}}
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
              <p style={{fontSize: "16px", marginTop: "5px"}}>
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
