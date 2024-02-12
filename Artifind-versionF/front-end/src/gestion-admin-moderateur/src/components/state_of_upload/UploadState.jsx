import React, { useState, useEffect } from "react";
import cancelIcon from "../../assets/cancelIcon.png";
import pdfIcon from "../../assets/pdfIcon.png";
import deleteIcon from "../../assets/deleteIcon.png";
import warningIcon from "../../assets/warningIcon.png";
import "./UploadState.css"; // Add your CSS file for styling

{}

// ... (other imports)

const UploadState = ({
  uploadState,
  progress,
  fileName,
  timeLeft,
  onCancel,
}) => {
  const [isCanceled, setCanceled] = useState(false);
  const [isProgressComplete, setProgressComplete] = useState(false);
  const [isDeleteClicked, setDeleteClicked] = useState(false);

  useEffect(() => {
    if (progress === 100) {
      setProgressComplete(true);
    }
  }, [progress]);

  const handleCancelClick = () => {
    setCanceled(true);
    onCancel();
  };

  const handleDeleteClick = () => {
    setDeleteClicked(true);
    // Add logic for any other actions you want to perform on delete
  };

  if (isDeleteClicked) {
    return null;
  }

  return (
    <div>
      {uploadState === "current" && (
        <div
          className={`upload-state-current ${isDeleteClicked ? "hidden" : ""}`}
        >
          <div className="file-info">
            <img className="pdf-icon" src={pdfIcon} alt="PDF Icon" />
            <span className="file-name">{fileName}</span>
          </div>

          {!isCanceled && !isProgressComplete ? (
            <div className="progress-bar">
              <div className="progress" style={{ width: `${progress}%` }}></div>
              <div className="progress-info">
                <span>{progress}% completed</span>
                <span>{timeLeft} left</span>
              </div>
            </div>
          ) : isCanceled ? (
            <div className="upload-canceled-message">
              <p>Upload Canceled</p>
              <div className="delete-info">
                <img
                  className="delete-icon"
                  src={deleteIcon}
                  alt="Delete Icon"
                  onClick={handleDeleteClick}
                />
              </div>
            </div>
          ) : null}

          {!isCanceled && !isProgressComplete && (
            <div className="cancel-info">
              <img
                className="cancel-icon"
                src={cancelIcon}
                alt="Cancel Icon"
                onClick={handleCancelClick}
              />
            </div>
          )}
        </div>
      )}

      {uploadState === "success" && (
        <div className={`success ${isDeleteClicked ? "hidden" : ""}`}>
          {isDeleteClicked ? null : (
            <div className="success-info">
              <img className="pdf-icon" src={pdfIcon} alt="PDF Icon" />
              <span className="file-name">{fileName}</span>
              <span className="file-size">File Size</span>
              {/* Add any other success state information here */}
            </div>
          )}

          {!isDeleteClicked && (
            <div className="delete-info">
              <img
                className="delete-icon"
                src={deleteIcon}
                alt="Delete Icon"
                onClick={handleDeleteClick}
              />
            </div>
          )}
        </div>
      )}

      {uploadState === "fail" && (
        <div
          className={`upload-fail-message ${isDeleteClicked ? "hidden" : ""}`}
        >
          <img className="pdf-icon" src={pdfIcon} alt="PDF Icon" />
          <span className="file-name">{fileName}</span>
          <p>Upload Failed</p>
          <img className="warning-icon" src={warningIcon} alt="Warning Icon" />
          <div className="delete-info">
            <img
              className="delete-icon"
              src={deleteIcon}
              alt="Delete Icon"
              onClick={handleDeleteClick}
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default UploadState;


