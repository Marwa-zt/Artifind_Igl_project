import React, { useState } from "react";
import axios from "axios";
import NavBar from "../common/NavBar";
import "./upload.css";
import uploadIcon from "../../assets/uploadIcon.png";

const Upload = () => {
  const [url, setUrl] = useState("");
  const [uploading, setUploading] = useState(false);

  const handleUrlChange = (event) => {
    setUrl(event.target.value);
  };

  const handleUpload = async () => {
    try {
      setUploading(true);
      const response = await axios.post("/extract/articles/upload", { url });
      console.log(url);
      if (response.data && response.data.data) {
        console.log("Upload successful!");
        console.log("Extracted Data:", response.data.data);
      } else {
        console.error("Upload failed:", response.data.detail);
      }
    } catch (error) {
      console.error("Upload failed:", error.message);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <h1 className="title">Importer des articles scientifiques</h1>
      <div className="upload-form">
        <input
          className="upload-input"
          type="text"
          value={url}
          onChange={handleUrlChange}
          placeholder="Entrer l’URL ici"
        />
        <button className="upload-button" onClick={handleUpload} disabled={uploading}>
          <img className="upload-icon" src={uploadIcon} alt="Icon" />
          {uploading ? "Importation..." : "Importer"}
        </button>
      </div>
    </div>
  );
};

export default Upload;
