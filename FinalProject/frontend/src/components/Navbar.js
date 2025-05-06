import React, { useEffect, useState } from "react";

import { Link } from "react-router-dom";
import { FiLogOut } from "react-icons/fi";
import { FaImages, FaChartBar, FaInfoCircle } from "react-icons/fa";

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
    <header className="header-area header-sticky"
      style={{
        backgroundColor: scrolled ? "white" : "transparent",

      }}>
      <link
        href="https://fonts.googleapis.com/css2?family=Pacifico&family=Lobster&family=Handlee&family=Open+Sans&display=swap"
        rel="stylesheet"
      />
      <div className="container"  style={{maxWidth: "1200px", margin: "5 auto"}}>
        <div className="row">
          <div className="col-12">
            <nav className="main-nav"
           style={{display: "flex", justifyContent: "space-between", alignItems: "center"}}>


              {/* Logo */}
              <
                Link to="/ManuscriptListPage"
                style={{
                  fontSize: "62px",
                  fontFamily: "'Lobster', cursive",
                  color: scrolled ? "#007f3f" : "white",
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
                        gap: "24px",
                        margin: 0,
                        padding: 3,
                        alignItems: "center",
                    }}
                >

                    <li className="scroll-to-section">
                        <Link to="/ManuscriptListPage" style={{fontSize: "23px", color: scrolled ? "black" : "white" }}>
                            <FaImages /> My Folders
                        </Link>
                    </li>
                    <li className="scroll-to-section">
                        <Link to="/SortedModelsPage" style={{fontSize: "23px", color: scrolled ? "black" : "white" }}>
                           <FaChartBar /> TopModels
                        </Link>
                    </li>
                    <li className="scroll-to-section">
                        <Link to="/about-us" style={{fontSize: "23px", color: scrolled ? "black" : "white" }}>
                           <FaInfoCircle /> About Us
                        </Link>
                    </li>
                    <li className="scroll-to-section">
                        <button
                            onClick={handleLogout}
                            style={{
                                fontSize: "22px",
                                fontFamily: "'Roboto', sans-serif",
                                background: "transparent",
                                border: "none",
                                 color: scrolled ? "black" : "white",
                                cursor: "pointer",
                                textDecoration: "none",
                                padding: 0,
                                marginBottom:"0px",
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

export default Navbar;
