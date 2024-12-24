import React from "react";
import { Link } from "react-router-dom";

const HomePage = () => {
  return (
    <div>
      <h1>Welcome to the Home Page</h1>
      {/* Link to the Sign-Up page */}
      <Link to="/register" style={{ fontSize: "40px", color: "black", backgroundColor: "transparent" }}>
        Sign Up
      </Link>
    </div>
  );
};

export default HomePage;
