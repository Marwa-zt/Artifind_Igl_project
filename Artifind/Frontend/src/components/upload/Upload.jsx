// Upload.js
import React, { useState } from "react";
import NavBar from "../common/NavBar";
import "./upload.css";
import axios from "axios";
import uploadIcon from "../../assets/uploadIcon.png";
import UploadState from "../state_of_upload/UploadState";


const Upload = () => {
  const [url, setUrl] = useState("");
  const [uploading, setUploading] = useState(false);
  const [uploadState, setUploadState] = useState("current");
  const [progress, setProgress] = useState(0);

  const handleUrlChange = (event) => {
    setUrl(event.target.value);
  };

  const handleUpload = async () => {
    try {
      setUploading(true);

      // Simulating upload progress
      for (let i = 0; i <= 100; i += 10) {
        setProgress(i);
        await new Promise((resolve) => setTimeout(resolve, 1000));
      }

      // Simulating successful upload
      setUploadState("success");
      console.log("Upload successful!");
    } catch (error) {
      // Simulating failed upload
      setUploadState("fail");
      console.error("Upload failed:", error.message);
    } finally {
      // Don't set uploadState to "success" here
      setUploading(false);
    }
  };

  const handleCancel = () => {
    // Implement cancel logic if needed
    console.log("Upload canceled!");
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

        {/* Render the UploadState component */}
        <UploadState uploadState={uploadState} progress={progress} fileName="example.pdf" onCancel={handleCancel} />
        <UploadState uploadState="fail" fileName="example.pdf" />
        <UploadState uploadState="success" fileName="example.pdf" />
        {/* Render the UploadStateCurrent component for the "current" state */}
      </div>
    </div>
  );
};

export default Upload



/*
// Upload.js
import React, { useState } from "react";
import axios from "axios";
import NavBar from "../common/NavBar";
import "./upload.css";
import uploadIcon from "../../assets/uploadIcon.png";
import UploadState from "../state_of_upload/UploadState";

const Upload = () => {
  const [url, setUrl] = useState("");
  const [uploading, setUploading] = useState(false);
  const [uploadState, setUploadState] = useState("current");
  const [progress, setProgress] = useState(0);

  const handleUrlChange = (event) => {
    setUrl(event.target.value);
  };

  const handleUpload = async () => {
    try {
      setUploading(true);

      // Send a POST request to the server for file upload
      const response = await axios.post("your_upload_api_endpoint", { url });

      // Check the response for success
      if (response.data.success) {
        setUploadState("success");
        console.log("Upload successful!");
      } else {
        setUploadState("fail");
        console.error("Upload failed:", response.data.error);
      }
    } catch (error) {
      setUploadState("fail");
      console.error("Upload failed:", error.message);
    } finally {
      setProgress(0);
      setUploading(false);
    }
  };

  const handleCancel = () => {
    // Implement cancel logic if needed
    console.log("Upload canceled!");
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

        {/* Render the UploadState component */
        /*<UploadState uploadState={uploadState} progress={progress} fileName="example.pdf" onCancel={handleCancel} />
      </div>
    </div>
  );
};

export default Upload;

*/