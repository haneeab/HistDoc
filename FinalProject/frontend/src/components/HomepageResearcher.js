import React, { useState } from "react";

function DeveloperUpload() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

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

  const handleUpload = (e) => {
    e.preventDefault();
    if (!file) {
      setMessage("❌ Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    fetch("http://127.0.0.1:8000/api/upload-developer-file/", {
      method: "POST",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
      credentials: "include",
      body: formData,
    })
      .then((res) => res.json())
      .then((data) => setMessage(data.message || data.error))
      .catch((err) => {
        console.error("❌ Upload error:", err);
        setMessage("❌ Upload failed.");
      });
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h2>Upload .pt or .py File</h2>
      <form onSubmit={handleUpload}>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button type="submit">Upload</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
}

export default DeveloperUpload;
