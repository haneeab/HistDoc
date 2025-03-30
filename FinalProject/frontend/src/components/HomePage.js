import React, { Component } from "react";
import Register from "./Register";
import LogIn from "./LogIn";
import Navbar from "./Navbar";
import HomepageUser from "./HomepageUser";
import UserImages from "./UserImages";
import AboutUs from "./AboutUs";
import { BrowserRouter as Router, Switch, Route, Link, Redirect } from "react-router-dom";
import HomepageResearcher from "./HomepageResearcher";

export default class HomePage extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (

            <div id="main">
              <div id="app">
                <link
                    href="https://fonts.googleapis.com/css2?family=Pacifico&family=Lobster&family=Handlee&display=swap"
                    rel="stylesheet"/>
                {/* ***** Header Area Start ***** */}
                <header className="header-area header-sticky">
                  <div className="container">
                    <div className="row">
                      <div className="col-12">
                        <nav className="main-nav">
                          <a href="#top" style={{fontSize: "65px", fontFamily: "'Lobster', cursive"}} className="logo">
                            HIST DOC
                          </a>
                          {/* ***** Logo End ***** */}
                          {/* ***** Menu Start ***** */}
                          <ul className="nav">
                            <li className="scroll-to-section">
                              <a href="#top" style={{fontSize: "40px", fontFamily: "'Roboto', sans-serif"}}
                                 className="active">
                                Home
                              </a>
                            </li>
                            <li className="scroll-to-section">
                              <a href="#about" style={{fontSize: "40px", fontFamily: "'Roboto', sans-serif"}}>
                                About
                              </a>
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
                              Sing Inhhh
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
                {/* ***** Main Banner Area Start ***** */}
                <div className="main-banner header-text" id="top">
                  <div className="Modern-Slider">
                    {/* Item */}
                    <div className="item">
                      <div className="img-fill">
                        <img src="static/images/slide-01.jpg" alt=""/>
                        <div className="text-content">
                          <h3 style={{fontSize: "35px"}}>For Users</h3>
                          <h5 style={{fontSize: "30px"}}>Upload your historical documents with ease.</h5>
                          <a href="#about" className="main-stroked-button">
                            Explore More
                          </a>
                        </div>
                      </div>
                    </div>
                    {/* Item */}
                    <div className="item">
                      <div className="img-fill">
                        <img src="static/images/slide-02.jpg" alt=""/>
                        <div className="text-content">
                          <h3 style={{fontSize: "35px"}}>For Researchers</h3>
                          <h5 style={{fontSize: "30px"}}>
                            Submit your algorithms to analyze historical texts.
                          </h5>
                          <a href="#about" className="main-filled-button">
                            Learn More
                          </a>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                {/* ***** Main Banner Area End ***** */}
                {/* ***** About Area Starts ***** */}
                <section className="section" id="about">
                  <div className="container">
                    <div className="row">
                      <div className="col-lg-6">
                        <div className="left-text-content">
                          <div className="section-heading">
                            <h6 style={{fontSize: "35px"}}>About Us</h6>
                            <h2 style={{fontSize: "30px"}}>
                              Preserving History with Technology
                            </h2>
                          </div>
                          <p style={{fontSize: "20px"}}>
                            Our platform connects users who want to upload historical documents with
                            researchers who provide advanced algorithms to read and analyze these
                            texts. Together, we are preserving history for future generations.
                          </p>
                        </div>
                      </div>
                      <div className="col-lg-6">
                        <div className="right-text-content">
                          <img
                              src="static/images/Historical-Paper-Documents-Whats-Made-Them-Last-1536x861.jpg"
                              alt="Historical Documents"
                              style={{width: "100%", height: "auto"}}
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                </section>
              </div>
            </div>

    );
  }
}
