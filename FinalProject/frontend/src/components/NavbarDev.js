import React, { useEffect, useState } from "react";

import { Link } from "react-router-dom";
import { FiLogOut } from "react-icons/fi";
import {FaUpload ,FaCubes,FaComments,} from "react-icons/fa";
const getCookie = (name) => {
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
};

const NavbarDev = () => {
     const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => {
      setScrolled(window.scrollY > 100); // you can change 100 to 50 or any number
    };

    window.addEventListener("scroll", onScroll);

    return () => window.removeEventListener("scroll", onScroll);
  }, []);
  const handleLogout = async () => {
  try {
    const response = await fetch("/api/logout/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),  // ✅ CSRF token added
      },
      credentials: "include", // ✅ include session cookie
    });

    const data = await response.json();

    if (response.ok) {
      localStorage.removeItem("authToken");
      window.location.href = data.redirect || "/";
    } else {
      console.error("Failed to log out");
    }
  } catch (error) {
    console.error("Logout error:", error);
  }
};

  return (
      <header className="header-area header-sticky" style={{        backgroundColor: scrolled ? "white" : "transparent",
 padding: "10px 0"}}>
          <link
              href="https://fonts.googleapis.com/css2?family=Pacifico&family=Lobster&family=Handlee&display=swap"
              rel="stylesheet"
          />
          <div className="container" style={{maxWidth: "1200px", margin: "5 auto"}}>
              <div className="row">
                  <div className="col-12">
                      <nav className="main-nav"
                           style={{display: "flex", justifyContent: "space-between", alignItems: "center"}}>
                          {/* Logo */}
                          <a
                              href="/researcher-homepage"
                              className="logo"
                              style={{
                                  fontSize: "60px",
                                  fontFamily: "'Lobster', cursive",
                                   color: scrolled ? "#007f3f" : "white",
                                  textDecoration: "none",
                              }}
                          >
                              HIST DOC
                          </a>

                          {/* Nav Links */}
                          <ul
                              className="nav"
                              style={{
                                  listStyle: "none",
                                  display: "flex",
                                  gap: "28px",
                                  margin: 0,
                                  padding: 0,
                                  alignItems: "center",
                              }}
                          >
                              <li>
                                  <Link
                                      to="/researcher-homepage"
                                      style={{
                                          fontSize: "26px",
                                          fontFamily: "'Roboto', sans-serif",
                                          color: scrolled ? "black" : "white",
                                          textDecoration: "none",
                                      }}
                                  >
                                     <FaUpload /> Uploading
                                  </Link>

                              </li>
                              <li>
                                   <Link
                                      to="/developer-models"
                                      style={{
                                          fontSize: "26px",
                                          fontFamily: "'Roboto', sans-serif",
                                          color: scrolled ? "black" : "white",
                                          textDecoration: "none",

                                      }}
                                  >
                                   <FaCubes/> Models
                                  </Link>
                              </li>
                              <li>
                                  <Link
                                      to="/AllModelsFeedbackSummary"
                                      style={{
                                          fontSize: "26px",
                                          fontFamily: "'Roboto', sans-serif",
                                          color: scrolled ? "black" : "white",
                                          textDecoration: "none",
                                      }}
                                  >
                                    <FaComments /> Feedback
                                  </Link>
                              </li>
                              <li>
                                  <button
                                      onClick={handleLogout}
                                      style={{
                                          fontSize: "26px",
                                          fontFamily: "'Roboto', sans-serif",
                                          background: "transparent",
                                          border: "none",
                                 color: scrolled ? "black" : "white",
                                          cursor: "pointer",
                                          textDecoration: "none",
                                          padding: 0,
                                      }}
                                  >
                              <FiLogOut /> Logout
                                  </button>
                              </li>
                          </ul>
                      </nav>
                  </div>
              </div>
          </div>
      </header>
  );
};

export default NavbarDev;
