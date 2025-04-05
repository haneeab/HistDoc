import React from "react";
import { Link } from "react-router-dom";
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
const Navbar = () => {
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
    <header className="header-area header-sticky">
      <link
        href="https://fonts.googleapis.com/css2?family=Pacifico&family=Lobster&family=Handlee&family=Open+Sans&display=swap"
        rel="stylesheet"
      />
      <div className="container">
        <div className="row">
          <div className="col-12">
            <nav className="main-nav">
              {/* Logo */}
              <
                Link to="/homepage-user"
                style={{
                  fontSize: "65px",
                  fontFamily: "'Lobster', cursive",
                  color: "white",
                  textDecoration: "none",
                }}
                className="logo"
              >
                HIST DOC
              </Link>

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
                        fontFamily: "'Open Sans', 'Roboto', sans-serif",
                        alignItems: "center",
                    }}
                >

                    <li className="scroll-to-section">
                        <Link to="/user-images" style={{fontSize: "25px", color: "white"}}>
                            My Images
                        </Link>
                    </li>
                    <li className="scroll-to-section">
                        <Link to="/SortedModelsPage" style={{fontSize: "25px", color: "white"}}>
                            TopModels
                        </Link>
                    </li>
                    <li className="scroll-to-section">
                        <Link to="/about-us" style={{fontSize: "25px", color: "white"}}>
                            About Us
                        </Link>
                    </li>
                    <li className="scroll-to-section">
                        <button
                            onClick={handleLogout}
                            style={{
                                fontSize: "25px",
                                fontFamily: "'Roboto', sans-serif",
                                background: "transparent",
                                border: "none",
                                color: "white",
                                cursor: "pointer",
                                textDecoration: "none",
                                padding: 0,
                            }}
                        >
                            🧾 Logout
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

export default Navbar;
