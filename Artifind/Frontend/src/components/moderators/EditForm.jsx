// EditForm.jsx
import React, { useEffect, useState } from "react";
import "./editForm.css";
import modifyIcon from "../../assets/modifyIcon.png";

const EditForm = ({
  selectedModerator,
  onUpdate,
  onClose,
  showAlert,
  setShowAlert,
}) => {
  const [editedModerator, setEditedModerator] = useState({
    nom: selectedModerator.nom,
    prenom: selectedModerator.prenom,
    email: selectedModerator.email,
    id: selectedModerator.id,
  });

  const [isSaveConfirmationModalVisible, setIsSaveConfirmationModalVisible] =
    useState(false);

  // Add this useEffect hook
  // EditForm.jsx
  useEffect(() => {
    if (!showAlert) {
      // Reset the showAlert state when it changes externally
      setEditedModerator((prevModerator) => ({
        ...prevModerator,
        showAlert: false,
      }));
    }
  }, [showAlert]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;

    // Check if the field is 'id' and the value is a valid number or an empty string
    const newValue =
      name === "id"
        ? value === "" || !isNaN(value)
          ? String(value)
          : editedModerator.id
        : value;

    console.log(`name: ${name}, value after check: ${newValue}`);

    setEditedModerator((prevModerator) => ({
      ...prevModerator,
      [name]: newValue,
    }));
  };

  const handleSave = () => {
    console.log("Save button clicked.");

    // Check if an alert is currently displayed
    if (showAlert) {
      console.log("Alert is displayed. Form will not close.");
      // Do not close the form if an alert is displayed
      return;
    }

    console.log("Attempting to save...");
    onUpdate(editedModerator, (success) => {
      if (success) {
        console.log("Update successful. Closing form.");
        // Close the form after saving within the onUpdate callback
        onClose();
      } else {
        console.log("Update failed. Alert is already displayed.");
        // Handle the case when the update fails (e.g., duplicate id)
        setEditedModerator((prevModerator) => ({
          ...prevModerator,
          showAlert: true,
        }));
      }
    });
  };

  return (
    <div className="modal-overlay">
      <div className="edit-form">
        <div className="form-title">
          <img src={modifyIcon} alt="Edit Icon" className="buttonIcon" />
          <span>Modifier les informations</span>
        </div>
        <div className="form-label">
          <label>Nom</label>
          <input
            type="text"
            name="nom"
            placeholder={selectedModerator.nom}
            value={editedModerator.nom}
            onChange={handleInputChange}
          />
        </div>
        <div className="form-label">
          <label>Prenom</label>
          <input
            type="text"
            name="prenom"
            placeholder={selectedModerator.prenom}
            value={editedModerator.prenom}
            onChange={handleInputChange}
          />
        </div>
        <div className="form-label">
          <label>E-mail</label>
          <input
            type="email"
            name="email"
            placeholder={selectedModerator.email}
            value={editedModerator.email}
            onChange={handleInputChange}
          />
        </div>
        <div className="form-label">
          <label>Mot de passe</label>
          <input
            type="password"
            name="password"
            placeholder={selectedModerator.password}
            value={editedModerator.password}
            onChange={handleInputChange}
          />
        </div>
        <div className="form-label">
          <label>Id</label>
          <input
            type="text"
            name="id"
            placeholder={selectedModerator.id}
            value={editedModerator.id}
            onChange={handleInputChange}
          />
        </div>
        <div className="form-buttons">
          <button className="save-button" onClick={handleSave}>
            Enregister
          </button>
          <button className="cancel-button" onClick={onClose}>
            Annuler
          </button>
        </div>
      </div>
    </div>
  );
};

export default EditForm;

/* 
// EditForm.jsx
import React, { useEffect, useState } from "react";
import "./editForm.css";
import modifyIcon from "../../assets/modifyIcon.png";
import axios from "axios";

const EditForm = ({
  selectedModerator,
  onUpdate,
  onClose,
  showAlert,
  setShowAlert,
}) => {
  const [editedModerator, setEditedModerator] = useState({
    nom: selectedModerator.nom,
    prenom: selectedModerator.prenom,
    email: selectedModerator.email,
    id: selectedModerator.id,
  });

  const [isSaveConfirmationModalVisible, setIsSaveConfirmationModalVisible] = useState(false);

  useEffect(() => {
    if (!showAlert) {
      // Reset the showAlert state when it changes externally
      setEditedModerator((prevModerator) => ({
        ...prevModerator,
        showAlert: false,
      }));
    }
  }, [showAlert]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;

    // Check if the field is 'id' and the value is a valid number or an empty string
    const newValue =
      name === "id"
        ? value === "" || !isNaN(value)
          ? String(value)
          : editedModerator.id
        : value;

    setEditedModerator((prevModerator) => ({
      ...prevModerator,
      [name]: newValue,
    }));
  };

  const handleSave = async () => {
    try {
      // Check if an alert is currently displayed
      if (showAlert) {
        // Do not close the form if an alert is displayed
        return;
      }

      // Send a PUT request to update the moderator
      const response = await axios.put(
        `your_api_endpoint/moderators/${editedModerator.id}`,
        editedModerator
      );

      // Check the response for success
      if (response.data.success) {
        // Close the form after saving
        onUpdate(editedModerator, true);
        onClose();
      } else {
        // Handle the case when the update fails (e.g., duplicate id)
        onUpdate(editedModerator, false);
        setEditedModerator((prevModerator) => ({
          ...prevModerator,
          showAlert: true,
        }));
      }
    } catch (error) {
      console.error("Error updating moderator:", error.message);
    }
  };

  return (
    <div className="edit-form">
      {/* ... (rest of the component remains unchanged) */
/* </div>
      );
    };
    
    export default EditForm;
    
*/
