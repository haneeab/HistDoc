import React from "react";
import Navbar from "./Navbar"; // Import the Navbar component

const ImageCard = ({ src, text }) => {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        padding: "10px",
        border: "1px solid #ccc",
        borderRadius: "10px",
        backgroundColor: "#fff",
        boxShadow: "0 2px 5px rgba(0, 0, 0, 0.1)",
        textAlign: "center",
      }}
    >
      <img
        src={src}
        alt="Uploaded"
        style={{
          width: "100px",
          height: "100px",
          borderRadius: "10px",
          objectFit: "cover",
          marginBottom: "10px",
        }}
      />
      <p
        style={{
          margin: 0,
          fontWeight: "bold",
          color: "#333",
          fontSize: "0.9rem",
        }}
      >
        Extracted Text:
      </p>
      <p
        style={{
          margin: "5px 0 0",
          color: "#666",
          fontSize: "0.8rem",
        }}
      >
        {text}
      </p>
    </div>
  );
};

const UserImages = () => {
  const uploadedImages = [
    { id: 1, src: "static/images/img.png", text: "Lorem ipsum dolor sit amet." },
    { id: 2, src: "static/images/img_2.png", text: "Nullam id dolor id nibh ultricies vehicula." },
    { id: 3, src: "static/images/img.png", text: "Lorem ipsum dolor sit amet." },
    { id: 4, src: "static/images/img_2.png", text: "Nullam id dolor id nibh ultricies vehicula." },
    { id: 5, src: "static/images/img.png", text: "Lorem ipsum dolor sit amet." },
    { id: 6, src: "static/images/img_2.png", text: "Nullam id dolor id nibh ultricies vehicula." },
       { id: 7, src: "static/images/img.png", text: "Lorem ipsum dolor sit amet." },
    { id: 8, src: "static/images/img_2.png", text: "Nullam id dolor id nibh ultricies vehicula." },
    { id: 9, src: "static/images/img.png", text: "Lorem ipsum dolor sit amet." },
    { id: 10, src: "static/images/img_2.png", text: "Nullam id dolor id nibh ultricies vehicula." },
    { id: 11, src: "static/images/img.png", text: "Lorem ipsum dolor sit amet." },
    { id: 12, src: "static/images/img_2.png", text: "Nullam id dolor id nibh ultricies vehicula." },
  ];

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
            maxWidth: "1000px",
            width: "90%",
            backgroundColor: "white",
            borderRadius: "15px",
            padding: "10px",
            boxShadow: "0 4px 10px rgba(0, 0, 0, 0.2)",
            overflow: "hidden",
              marginTop:"80px",
          }}
        >
          <h2
            style={{
              textAlign: "center",
              color: "#007f3f",
              fontFamily: "'Handlee', cursive",
              marginBottom: "20px",
            }}
          >
            My Uploaded Images
          </h2>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(150px, 1fr))",
              gap: "15px",
              maxHeight: "400px",
              overflowY: "auto",
              padding: "10px",
              border: "1px solid #ddd",
              borderRadius: "10px",
              backgroundColor: "#f7f9fc",
            }}
          >
            {uploadedImages.length > 0 ? (
              uploadedImages.map((image) => (
                <ImageCard key={image.id} src={image.src} text={image.text} />
              ))
            ) : (
              <p style={{ textAlign: "center", color: "#666" }}>
                No uploaded images found.
              </p>
            )}
          </div>
        </div>
      </div>
    </>
  );
};

export default UserImages;
