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
                 backgroundColor: "white",
                 borderRadius: "15px",
                 boxShadow: "0 4px 10px rgba(0, 0, 0, 0.2)",
                 fontFamily: "'Open Sans', sans-serif",
                 padding: "20px",
                 marginTop: "100px"
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
                 As a researcher on HIST DOC, your journey begins by creating folders
                 to organize manuscript images. Once uploaded, these images can be
                 browsed in a clean, book-like view. To ensure accurate analysis,
                 you can upload XML ground truth files — each XML must match the
                 name of an image to maintain a clear connection. You can also rename
                 and delete both images and XML files with full control. When testing models,
                 simply select one from the available list, configure its parameters, and run it.
                 The platform will display the original image and the processed result side by side.
                 After testing, you’re invited to submit feedback and rate the model to help
                 guide future improvements. Everything is built to give you full flexibility
                 with an intuitive experience.
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
