import React from "react";
import { Link } from "react-router-dom";

const Navbar = () => {
  const handleLogout = async () => {
    try {
      const response = await fetch("/api/logout/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (response.ok) {
        localStorage.removeItem("authToken"); // Clear local storage
        window.location.href = ""; // Redirect to login page
      } else {
        console.error("Failed to log out");
      }
    } catch (error) {
      console.error("Logout error:", error);
    }
  };

  return (
    <header className="header-area header-sticky">
      <link
        href="https://fonts.googleapis.com/css2?family=Pacifico&family=Lobster&family=Handlee&display=swap"
        rel="stylesheet"
      />
      <div className="container">
        <div className="row">
          <div className="col-12">
            <nav className="main-nav">
              {/* Logo */}
              <a
                href=""
                style={{
                  fontSize: "65px",
                  fontFamily: "'Lobster', cursive",
                  color: "white",
                  textDecoration: "none",
                }}
                className="logo"
              >
                HIST DOC
              </a>

              {/* Menu Items */}
              <ul
                className="nav"
                style={{
                  listStyle: "none",
                  display: "flex",
                  gap: "30px",
                  margin: 0,
                  padding: 0,
                  fontSize: "40px",
                }}
              >
                <li className="scroll-to-section">
                  <Link
                    to="/homepage-user"
                    style={{ fontSize: "30px", fontFamily: "'Roboto', sans-serif" }}
                  >
                    Home
                  </Link>
                </li>
                <li className="scroll-to-section">
                  <Link
                    to="/user-images"
                    style={{ fontSize: "30px", fontFamily: "'Roboto', sans-serif" }}
                  >
                    My Images
                  </Link>
                </li>
                <li className="scroll-to-section">
                  <Link
                    to="/about-us"
                    style={{ fontSize: "30px", fontFamily: "'Roboto', sans-serif" }}
                  >
                    About Us
                  </Link>
                </li>
                {/*<li>*/}
                {/*  <button*/}
                {/*    onClick={handleLogout}*/}
                {/*    style={{*/}
                {/*      fontSize: "30px",*/}
                {/*      fontFamily: "'Roboto', sans-serif",*/}
                {/*      background: "transparent",*/}
                {/*      border: "none",*/}
                {/*      color: "white",*/}
                {/*      cursor: "pointer",*/}
                {/*    }}*/}
                {/*  >*/}
                {/*    Logout*/}
                {/*  </button>*/}
                {/*</li>*/}
              </ul>
            </nav>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Navbar;
