import React, { useEffect, useState } from "react";
import { useLocation ,Link } from "react-router-dom";

import Navbar from "./Navbar";

function useQuery() {
  return new URLSearchParams(useLocation().search);
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + "=")) {
        return decodeURIComponent(cookie.substring(name.length + 1));
      }
    }
  }
  return cookieValue;
}

const ManuscriptFilesPage = () => {
  const query = useQuery();
  const manuscriptId = query.get("id");
  const [files, setFiles] = useState([]);
  const [file, setFile] = useState(null);
  const [fileType, setFileType] = useState("image");
  const [previewImage, setPreviewImage] = useState(null);
  const [zoom, setZoom] = useState(1);
  const [outputImageMap, setOutputImageMap] = useState({});

  useEffect(() => {
    if (!manuscriptId) return;
    fetch(`http://127.0.0.1:8000/api/manuscript/${manuscriptId}/files/`, {
      credentials: "include",
      headers: { "X-CSRFToken": getCookie("csrftoken") },
    })
      .then((res) => res.json())
      .then((data) => {
        setFiles(data);
        const initialMap = {};
        data.forEach(file => {
          if (file.result_image) {
            initialMap[file.id] = file.result_image;
          }
        });
        setOutputImageMap(initialMap);
      });
  }, [manuscriptId]);

  const handleUpload = () => {
    if (!file || !manuscriptId) return alert("Choose a file!");

    const formData = new FormData();
    formData.append("file", file);
    formData.append("file_type", fileType);

    fetch(`http://127.0.0.1:8000/api/manuscript/${manuscriptId}/files/`, {
      method: "POST",
      credentials: "include",
      headers: { "X-CSRFToken": getCookie("csrftoken") },
      body: formData,
    })
      .then((res) => res.json())
      .then((data) => {
        setFiles((prev) => [...prev, data]);
        setFile(null);
      })
      .catch((err) => console.error("Upload failed:", err));
  };

  const handleDelete = (fileId) => {
    if (!window.confirm("Delete this file?")) return;

    fetch(`http://127.0.0.1:8000/api/delete-manuscript-file/${fileId}/`, {
      method: "DELETE",
      credentials: "include",
      headers: { "X-CSRFToken": getCookie("csrftoken") },
    })
      .then(() => setFiles(files.filter((f) => f.id !== fileId)))
      .catch((err) => console.error("Delete failed:", err));
  };

  const handleRename = (fileId) => {
    const newName = prompt("Enter new name for the file:");
    if (!newName) return;

    fetch(`http://127.0.0.1:8000/api/rename-manuscript-file/${fileId}/`, {
      method: "PATCH",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({ new_name: newName }),
    })
      .then((res) => res.json())
      .then((updatedFile) => {
        setFiles((prev) =>
          prev.map((file) => (file.id === fileId ? updatedFile : file))
        );
      });
  };

  return (
    <>
      <Navbar />
      <div
        style={{
          minHeight: "100vh",
          padding: "80px 20px",
          background: "linear-gradient(to bottom right, #007f3f, #8b8b8b)",
        }}>
        <h2 style={{ color: "white", textAlign: "center" }}>📁 Manuscript Files</h2>

        <div style={{ margin: "20px 0" }}>
          <input type="file" onChange={(e) => setFile(e.target.files[0])} />
          <select value={fileType} onChange={(e) => setFileType(e.target.value)}>
            <option value="image">Image</option>
            <option value="ground_truth">Ground Truth</option>
          </select>
          <button
            onClick={handleUpload}
            style={{
              marginLeft: "10px",
              backgroundColor: "#007f3f",
              color: "white",
              padding: "5px 15px",
              border: "none",
              borderRadius: "5px",
            }}>
            Upload
          </button>
            <Link
              to={`/ManuscriptListPage`}
              style={{ textDecoration: "none", color: "white", fontWeight: "bold",marginLeft:"500px" }}>
              ← Back to Manuscript
            </Link>
        </div>

        <ul style={{ listStyle: "none", padding: 0 }}>
          {files.map((file) => {
            const fileName = file.file?.split("/").pop();
            const imageUrl = `http://127.0.0.1:8000/api/media/${fileName}?t=${new Date().getTime()}`;
const outputUrl = file.result_image;

            return (
                <li
                    key={file.id}
                    style={{
                        background: "white",
                        padding: "15px",
                        margin: "10px 0",
                        borderRadius: "10px",
                        boxShadow: "0 2px 5px rgba(0,0,0,0.1)",
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "center",
                    }}>
                    <img
                        src={imageUrl}
                        alt="preview"
                        style={{
                            width: "80px",
                            height: "80px",
                            objectFit: "cover",
                            borderRadius: "10px",
                            cursor: "pointer",
                        }}
                        onClick={() => {
                            setPreviewImage(imageUrl);
                            setZoom(1);
                        }}
                    />

                    <span style={{
                        fontSize: "16px",
                        color: "#555",
                        maxWidth: "190px",
                        textAlign: "right",
                        paddingRight: "150px",
                    }}>{fileName}</span>
                    <div style={{display: "flex", gap: "10px"}}>
                        <button onClick={() => {
                            setPreviewImage(imageUrl);
                            setZoom(1);
                        }}
                                style={{
                                    backgroundColor: "#007f3f",
                                    color: "white",
                                    border: "none",
                                    padding: "5px 10px",
                                    borderRadius: "5px"
                                }}>
                            🔍 View
                        </button>
                        <button onClick={() => handleRename(file.id)}
                                style={{
                                    backgroundColor: "#ffa500",
                                    color: "white",
                                    border: "none",
                                    padding: "5px 10px",
                                    borderRadius: "5px"
                                }}>
                            ✏ Rename
                        </button>
                       <Link
                              to={`/select-model?file_id=${file.id}&manuscript_id=${manuscriptId}`}
                              style={{
                                backgroundColor: "#2c7",
                                color: "white",
                                padding: "5px 10px",
                                borderRadius: "5px",
                                marginLeft: "8px",
                                textDecoration: "none",
                                display: "inline-block"
                              }}
                            >
                              ⚙️ Run Model
                            </Link>

                        <button onClick={() => handleDelete(file.id)}
                                style={{
                                    backgroundColor: "#ff4d4d",
                                    color: "white",
                                    border: "none",
                                    padding: "5px 10px",
                                    borderRadius: "5px"
                                }}>
                            ❌ Delete
                        </button>
                        <button
                            onClick={() => {
                                if (file.result_image) {
                                    const fullResultURL = `http://127.0.0.1:8000/api/media/processed/${file.result_image}`;
                                    console.log("👁 View Result URL:", fullResultURL);
                                    setPreviewImage(fullResultURL);
                                    setZoom(1);
                                } else {
                                    alert("❌ You haven't run the model yet for this file.");
                                }
                            }}
                            style={{
                                backgroundColor: "#007f3f",
                                color: "white",
                                border: "none",
                                padding: "5px 10px",
                                borderRadius: "5px",
                                marginLeft: "8px"
                            }}
                        >
                            👁 View Result
                        </button>


                    </div>
                </li>
            );
          })}
        </ul>

          {previewImage && (
              <div style={{
                  position: "fixed",
                  top: 0,
                  left: 0,
                  width: "100%",
                  height: "100%",
                  backgroundColor: "rgba(0, 0, 0, 0.8)",
                  display: "flex",
                  justifyContent: "center",
                  alignItems: "center",
                  zIndex: 9999,
                  flexDirection: "column",
              }}
            onClick={() => setPreviewImage(null)}>
            <img src={previewImage} alt="Preview" style={{
              maxHeight: "80%",
              maxWidth: "80%",
              transform: `scale(${zoom})`,
              transition: "transform 0.2s",
              border: "5px solid white",
              borderRadius: "10px",
            }} />
            <div style={{ marginTop: "20px", display: "flex", gap: "10px" }}>
              <button onClick={(e) => { e.stopPropagation(); setZoom(z => z + 0.1); }}>➕ Zoom In</button>
              <button onClick={(e) => { e.stopPropagation(); setZoom(z => Math.max(0.1, z - 0.1)); }}>➖ Zoom Out</button>
              <button onClick={(e) => { e.stopPropagation(); setPreviewImage(null); }}>❌ Close</button>
            </div>
          </div>
        )}
      </div>
    </>
  );
};

export default ManuscriptFilesPage;
