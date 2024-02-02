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

  const [isSaveConfirmationModalVisible, setIsSaveConfirmationModalVisible] =
    useState(false);

  // Add this useEffect hook
  // EditForm.jsx

  const checkUserExistence = async (email) => {
    try {
      // Check if the user with the specified email exists
      const response = await axios.get(`http://127.0.0.1:8000/get-user/${email}`);
  
      if (response.status === 200) {
        console.log("User exists:", response.data);
        return true;
      } else {
        console.log("User does not exist. Handle accordingly.");
        return false;
      }
    } catch (error) {
      // Handle errors (e.g., network issues, server errors)
      console.error("Error checking user existence:", error.message);
      return false;
    }
  };
   
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

// ...

const handleSave = async () => {
  console.log("Save button clicked.");

  // Check if an alert is currently displayed
  if (showAlert) {
    console.log("Alert is displayed. Form will not close.");
    // Do not close the form if an alert is displayed
    return;
  }

  console.log("Checking user existence...");
  const userExists = await checkUserExistence(editedModerator.email);

  if (!userExists) {
    console.log("User does not exist. Handle accordingly.");
    // Handle the case when the user does not exist (e.g., display an error)
    setEditedModerator((prevModerator) => ({
      ...prevModerator,
      showAlert: true,
    }));
    return;
  }

  console.log("Attempting to save...");
  try {
    await axios.put(`http://127.0.0.1:8000/modify-user/${editedModerator.email}`, {
      email: editedModerator.email,
      nom: editedModerator.nom,
      prenom: editedModerator.prenom,
      hashed_password: editedModerator.hashed_password,
    });

    console.log("Update successful.");

    // Fetch the updated user data after modification
    const response = await axios.get(`http://127.0.0.1:8000/get-user/${editedModerator.email}`);
    const updatedUserData = response.data;

    // Update the state with the latest data
    setEditedModerator(updatedUserData);

    // Close the form after saving within the onUpdate callback
    onClose();
  } catch (error) {
    console.error("Update failed. Handle the error:", error.message);
    setEditedModerator((prevModerator) => ({
      ...prevModerator,
      showAlert: true,
    }));
  }
};

// ...

  

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
            name="hashed_password"
            placeholder={selectedModerator.hashed_password}
            value={editedModerator.hashed_password}
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

