import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Navbar from "./Navbar";
import { FaFolderPlus, FaTrash, FaFolderOpen } from "react-icons/fa";

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

export default function ManuscriptListPage() {
  const [manuscripts, setManuscripts] = useState([]);
  const [newFolderName, setNewFolderName] = useState("");

 useEffect(() => {
  fetch("http://127.0.0.1:8000/api/manuscripts/", {
    credentials: "include",
  })
    .then((res) => res.json())
    .then((data) => {
      setManuscripts(data);
    })
    .catch((err) => console.error("Error fetching manuscripts:", err));
}, []);
const handleRename = (id) => {
  const newName = prompt("Enter the new folder name:");
  if (!newName) return;

  fetch(`/api/manuscripts/${id}/rename/`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    credentials: "include",
    body: JSON.stringify({ new_name: newName }),
  })
    .then((res) => res.json())
    .then((data) => {
      setManuscripts(
        manuscripts.map((m) =>
          m.id === id ? { ...m, name: data.new_name } : m
        )
      );
    })
    .catch((err) => console.error("Rename failed:", err));
};


  const handleCreateFolder = () => {
    if (!newFolderName.trim()) return;
    fetch("http://127.0.0.1:8000/api/manuscripts/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      credentials: "include",
      body: JSON.stringify({ name: newFolderName }),
    })
      .then((res) => res.json())
      .then((folder) => {
        setManuscripts([...manuscripts, folder]);
        setNewFolderName("");
      });
  };

  const handleDelete = (id) => {
    if (!window.confirm("Are you sure you want to delete this folder?")) return;
    fetch(`/api/manuscripts/${id}/delete/`, {
  method: "DELETE",
  credentials: "include",
  headers: {
    "X-CSRFToken": getCookie("csrftoken"),
  },
})
.then(() => {
  setManuscripts(manuscripts.filter((m) => m.id !== id));
});

  };

  return (
      <>
          <Navbar/>
          <div
              style={{
                  minHeight: "100vh",
                  padding: "80px 20px",
                  background: "linear-gradient(to bottom right, #007f3f, #8b8b8b)",
              }}
          >
              <div
                  style={{
                      maxWidth: "800px",
                      backgroundColor: "white",
                      margin: "0 auto",
                      padding: "30px",
                      borderRadius: "15px",
                      boxShadow: "0 4px 10px rgba(0, 0, 0, 0.2)",
                  }}
              >
                  <h2 style={{textAlign: "center", color: "#007f3f"}}>📁 My Manuscripts</h2>

                  <div style={{display: "flex", gap: "10px", marginBottom: "20px"}}>
                      <input
                          type="text"
                          placeholder="New Folder Name"
                          value={newFolderName}
                          onChange={(e) => setNewFolderName(e.target.value)}
                          style={{flex: 1, padding: "8px", borderRadius: "5px"}}
                      />
                      <button
                          onClick={handleCreateFolder}
                          style={{
                              backgroundColor: "#007f3f",
                              color: "white",
                              border: "none",
                              padding: "8px 12px",
                              borderRadius: "5px",
                          }}
                      >
                          <FaFolderPlus/>
                      </button>

                  </div>

                  {manuscripts.map((m) => (
                      <div
                          key={m.id}
                          style={{
                              display: "flex",
                              justifyContent: "space-between",
                              alignItems: "center",
                              border: "1px solid #ccc",
                              borderRadius: "10px",
                              padding: "10px 15px",
                              marginBottom: "10px",
                          }}
                      >
                          <Link
                              to={`/ManuscriptFilesPage?id=${m.id}`}
                              style={{textDecoration: "none", color: "#007f3f", fontWeight: "bold"}}
                          >
                              <FaFolderOpen style={{marginRight: "8px"}}/> {m.name}
                          </Link>
                          <div style={{display: "flex", gap: "10px"}}>

                              <button
                                  onClick={() => handleRename(m.id)}
                                  style={{
                                      backgroundColor: "#ffa500",
                                      color: "white",
                                      border: "none",
                                      borderRadius: "5px",
                                      padding: "5px 10px",
                                      marginRight: "8px",
                                  }}
                              >
                                  ✏ Rename
                              </button>
                              <button
                                  onClick={() => handleDelete(m.id)}
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
                <Link
                  to={`/GroundFoldersPage?id=${m.id}`}
                  style={{
                    backgroundColor: "#555",
                    color: "white",
                    padding: "5px 10px",
                    borderRadius: "5px",
                    textDecoration: "none"
                  }}
                >
                  📄 Grounds
                </Link>

                          </div>
                      </div>
                  ))}
              </div>
          </div>

      </>
  );
}
