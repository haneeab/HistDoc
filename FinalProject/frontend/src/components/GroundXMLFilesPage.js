import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { Link } from "react-router-dom";

import Navbar from "./Navbar";
import { FaTrash } from "react-icons/fa";

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

const GroundXMLFilesPage = () => {
  const query = useQuery();
  const folderId = query.get("folder_id");
  const [files, setFiles] = useState([]);
  const [newFile, setNewFile] = useState(null);

  useEffect(() => {
    fetch(`/api/ground-folder/${folderId}/xmls/`, {
      credentials: "include",
    })
      .then((res) => res.json())
      .then(setFiles);
  }, [folderId]);

 const handleUpload = () => {
  if (!newFile) return alert("Please select an XML file.");
if (!newFile.name.endsWith(".xml")) {
  return alert("Only .xml files are allowed!");
}

 const fileName = newFile.name.split(".")[0];  // e.g. "page_001"
const formData = new FormData();
formData.append("file", newFile);
formData.append("base_name", fileName);


 fetch(`/api/ground-folder/${folderId}/xmls/`, {
  method: "POST",
  credentials: "include",
  headers: {
    "X-CSRFToken": getCookie("csrftoken"),
  },
  body: formData,
})
  .then(async (res) => {
    const data = await res.json();
    if (!res.ok) {
      alert("❌ Upload failed: " + (data.error || "Unknown error"));
      return;
    }
    setFiles([...files, data]);
    setNewFile(null);
  })
  .catch((err) => {
    alert("❌ Network or server error: " + err.message);
    console.error(err);
  });

};

  const handleDelete = (fileId) => {
    if (!window.confirm("Delete this XML file?")) return;

    fetch(`/api/ground-xml/${fileId}/delete/`, {
      method: "DELETE",
      credentials: "include",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
    }).then(() => {
      setFiles(files.filter((f) => f.id !== fileId));
    });
  };

  return (
    <>
      <Navbar />
      <div style={{
        minHeight: "100vh",
        padding: "80px 20px",
        background: "linear-gradient(to bottom right, #007f3f, #8b8b8b)",
      }}>
        <div style={{ maxWidth: "900px", margin: "auto", background: "#fff", padding: "30px", borderRadius: "10px" }}>
          <h2 style={{ textAlign: "center", color: "#007f3f" }}>📄 XML Files in Folder</h2>

          <div style={{ margin: "20px 0", display: "flex", gap: "10px" }}>
            <input type="file" onChange={(e) => setNewFile(e.target.files[0])} />
            <button
              onClick={handleUpload}
              style={{
                backgroundColor: "#007f3f",
                color: "white",
                padding: "6px 14px",
                border: "none",
                borderRadius: "5px",
              }}
            >
              Upload XML
            </button>
          </div>

          <ul style={{ listStyle: "none", padding: 0 }}>
            {files.map((file) => (
                <li
                    key={file.id}
                    style={{
                      background: "white",
                      marginBottom: "10px",
                      padding: "15px",
                      borderRadius: "8px",
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center",
                      boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
                    }}
                >
                  <p style={{color: file.linked_image_name ? "#007f3f" : "red"}}>
                    Linked image: {file.linked_image_name || "❌ Not linked"}
                  </p>


                  <a href={file.file} target="_blank" rel="noreferrer" style={{color: "#007f3f", fontWeight: "bold"}}>
                    {file.file.split("/").pop()}
                  </a>
                  <div style={{display: "flex", gap: "10px"}}>

                    <button
                        onClick={() => {
                          const newName = prompt("Enter new name for XML file:");
                          if (!newName) return;

                          fetch(`/api/ground-xml/${file.id}/rename/`, {
                            method: "PATCH",
                            headers: {
                              "Content-Type": "application/json",
                              "X-CSRFToken": getCookie("csrftoken"),
                            },
                            credentials: "include",
                            body: JSON.stringify({new_name: newName}),
                          })
                              .then(async (res) => {
                                const data = await res.json();
                                if (!res.ok) {
                                  alert("❌ Rename failed: " + (data.error || "Unknown error"));
                                  return;
                                }
                                setFiles(files.map(f => f.id === file.id ? data : f));
                              })
                              .catch((err) => {
                                alert("❌ Request failed: " + err.message);
                                console.error(err);
                              });
                        }}
                        style={{
                          backgroundColor: "#ffa500",
                          color: "white",
                          border: "none",
                          padding: "5px 10px",
                          borderRadius: "5px",
                          marginLeft: "8px",

                        }}
                    >
                      ✏ Rename
                    </button>

                    <Link
                        to={`/XMLAnnotatorPage?xml_id=${file.id}`}
                        style={{
                          backgroundColor: "#007f3f",
                          color: "white",
                          padding: "5px 10px",
                          borderRadius: "5px",
                          textDecoration: "none",
                          marginLeft: "8px"
                        }}
                    >
                      ✍ Annotate
                    </Link>
                    <a
                        href={file.file}
                        download
                        style={{
                          backgroundColor: "#6c63ff",
                          color: "white",
                          padding: "5px 10px",
                          borderRadius: "5px",
                          textDecoration: "none",
                          marginLeft: "8px"
                        }}
                    >
                      📥 Download
                    </a>

                    <button
                        onClick={() => handleDelete(file.id)}
                        style={{
                          backgroundColor: "#ff4d4d",
                          color: "white",
                          border: "none",
                          borderRadius: "5px",
                          padding: "5px 10px",
                        }}
                    >
                      <FaTrash/>
                    </button>
                  </div>
                </li>
            ))}
          </ul>
        </div>
      </div>
    </>
  );
};

export default GroundXMLFilesPage;
