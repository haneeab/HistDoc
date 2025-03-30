import React from "react";
import Navbar from "./Navbar"; // Import Navbar

const AboutUs = () => {
  return (
    <>
      {/* Add Navbar */}
      <Navbar />

      {/* Main Content */}
      <div
        style={{
          height: "100vh",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          background: "linear-gradient(to bottom right, #007f3f, #8b8b8b)",
        }}
      >
        <div
          style={{
            maxWidth: "800px",
            width: "100%",
            backgroundColor: "white",
            borderRadius: "15px",
            padding: "20px",
            boxShadow: "0 4px 10px rgba(0, 0, 0, 0.2)",
            fontFamily: "'Open Sans', sans-serif",
          }}
        >
          <h2
            style={{
              textAlign: "center",
              color: "#007f3f",
              marginBottom: "20px",
              fontFamily: "'Handlee', cursive",
            }}
          >
            About Us
          </h2>
          <p
            style={{
              color: "#333",
              lineHeight: "1.6",
              textAlign: "justify",
              fontSize: "1rem",
              padding: "10px",
            }}
          >
            Welcome to <strong>ImageTextReader</strong>! We are dedicated to
            making your life easier by providing a powerful and intuitive
            platform for extracting text from images. Whether you’re dealing
            with scanned documents, handwritten notes, or any other image-based
            text, our platform is here to help.
          </p>
          <p
            style={{
              color: "#333",
              lineHeight: "1.6",
              textAlign: "justify",
              fontSize: "1rem",
              padding: "10px",
            }}
          >
            Our mission is to bridge the gap between visual information and
            digital text, enabling users to access, edit, and store content
            effortlessly. We strive to deliver accurate results with a
            user-friendly interface, ensuring a seamless experience for
            everyone.
          </p>
          <p
            style={{
              color: "#007f3f",
              fontWeight: "bold",
              textAlign: "center",
              marginTop: "20px",
            }}
          >
            Thank you for choosing ImageTextReader. Let us turn your images into
            words!
          </p>
        </div>
      </div>
    </>
  );
};

export default AboutUs;
