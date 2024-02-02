// ConfirmationModal.jsx

import React from "react";
import "./confirmationModal.css";

const ConfirmationModal = ({ onCancel, onConfirm }) => {
  return (
    <div className="confirmation-modal">
      <div className="modal-content">
        <p>Are you sure you want to delete this moderator?</p>
        <div className="buttons">
          <button onClick={onCancel}>Cancel</button>
          <button onClick={onConfirm}>Confirm</button>
        </div>
      </div>
    </div>
  );
};

export default ConfirmationModal;
