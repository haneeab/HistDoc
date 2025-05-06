import React, { useEffect, useState } from "react";
import { useLocation, Link } from "react-router-dom";
import Navbar from "./Navbar";
import { FaFolderOpen, FaFolderPlus, FaTrash } from "react-icons/fa";

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

const GroundFoldersPage = () => {
  const query = useQuery();
  const manuscriptId = query.get("id");
  const [folders, setFolders] = useState([]);
  const [folderName, setFolderName] = useState("");
useEffect(() => {
  console.log("📡 Fetching ground folders for manuscript", manuscriptId); // add this
 fetch(`http://127.0.0.1:8000/api/manuscript/${manuscriptId}/grounds/?t=${Date.now()}`, {
  credentials: "include",
})
  .then((res) => res.json())
  .then(setFolders);

}, [manuscriptId]);


  const handleCreate = () => {
    if (!folderName.trim()) return;

    fetch(`http://127.0.0.1:8000/api/manuscript/${manuscriptId}/grounds/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      credentials: "include",
      body: JSON.stringify({ name: folderName }),
    })
       .then((res) => res.json())
  .then((data) => {
    console.log("📦 Created folder:", data);
    fetch(`http://127.0.0.1:8000/api/manuscript/${manuscriptId}/grounds/?t=${Date.now()}`, {
      credentials: "include",
    })
      .then((res) => res.json())
      .then(setFolders);
    setFolderName("");
  });

  };

  const handleDelete = (folderId) => {
    if (!window.confirm("Delete this folder and its XMLs?")) return;
    fetch(`http://127.0.0.1:8000/api/ground-folder/${folderId}/delete/`, {
      method: "DELETE",
      headers: { "X-CSRFToken": getCookie("csrftoken") },
      credentials: "include",
    }).then(() => {
      setFolders(folders.filter((f) => f.id !== folderId));
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
        <div style={{ maxWidth: "800px", margin: "0 auto", background: "white", padding: "30px", borderRadius: "10px" }}>
          <h2 style={{ color: "#007f3f", textAlign: "center" }}>🗂 Ground Folders</h2>

          <div style={{ display: "flex", marginBottom: "20px" }}>
            <input
              type="text"
              value={folderName}
              placeholder="New Folder Name"
              onChange={(e) => setFolderName(e.target.value)}
              style={{ flex: 1, padding: "8px", borderRadius: "5px" }}
            />
            <button
              onClick={handleCreate}
              style={{ backgroundColor: "#007f3f", color: "white", border: "none", padding: "8px 12px", borderRadius: "5px", marginLeft: "10px" }}
            >
              <FaFolderPlus />
            </button>
          </div>

          {folders.map((folder) => (
              <div key={folder.id} style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                border: "1px solid #ccc",
                borderRadius: "10px",
                padding: "10px 15px",
                marginBottom: "10px",
              }}>
                <Link to={`/GroundXMLFilesPage?folder_id=${folder.id}`}
                      style={{color: "#007f3f", fontWeight: "bold", textDecoration: "none"}}>
                  <FaFolderOpen style={{marginRight: "8px"}}/>
                  {folder.name}
                </Link>
                <div style={{display: "flex", gap: "10px"}}>

                  <button
                      onClick={() => {
                        const newName = prompt("Enter new name for folder:");
                        if (!newName) return;

                        fetch(`/api/ground-folder/${folder.id}/rename/`, {
                          method: "PATCH",
                          headers: {
                            "Content-Type": "application/json",
                            "X-CSRFToken": getCookie("csrftoken"),
                          },
                          credentials: "include",
                          body: JSON.stringify({new_name: newName}),
                        })
                            .then((res) => res.json())
                            .then((updated) => {
                              setFolders(folders.map((f) => f.id === folder.id ? updated : f));
                            });
                      }}
                      style={{
                        backgroundColor: "#ffa500",
                        color: "white",
                        border: "none",
                        padding: "5px 10px",
                        borderRadius: "5px",
                        marginLeft: "10px"
                      }}
                  >
                    ✏ Rename
                  </button>

                  <button onClick={() => handleDelete(folder.id)} style={{
                    backgroundColor: "#ff4d4d",
                    border: "none",
                    color: "white",
                    borderRadius: "5px",
                    padding: "5px 10px"
                  }}>
                    <FaTrash/>
                  </button>
                </div>
              </div>
                ))}
              </div>
            </div>
            </>
            );
          };

          export default GroundFoldersPage;
