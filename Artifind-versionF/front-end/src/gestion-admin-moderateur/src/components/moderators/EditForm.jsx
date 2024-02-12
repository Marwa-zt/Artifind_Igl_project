// EditForm.jsx
import React, { useEffect, useState } from "react";
import "./EditForm.css";
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
    hashed_password: selectedModerator.hashed_password,
    id: selectedModerator.id,
  });

  const [isSaveConfirmationModalVisible, setIsSaveConfirmationModalVisible] =
    useState(false);

  const checkUserExistence = async (email) => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/get-user/${email}`);
      if (response.ok) {
        const data = await response.json();
        console.log("User exists:", data);
        return true;
      } else {
        console.log("User does not exist. Handle accordingly.");
        return false;
      }
    } catch (error) {
      console.error("Error checking user existence:", error.message);
      return false;
    }
  };

  useEffect(() => {
    if (!showAlert) {
      setEditedModerator((prevModerator) => ({
        ...prevModerator,
        showAlert: false,
      }));
    }
  }, [showAlert]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
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

  const handleSave = async () => {
    console.log("Save button clicked.");

    if (showAlert) {
        console.log("Alert is displayed. Form will not close.");
        return;
    }

    console.log("Checking user existence...");
    const userExists = await checkUserExistence(editedModerator.email);

    if (!userExists) {
        console.log("User does not exist. Handle accordingly.");
        setEditedModerator((prevModerator) => ({
            ...prevModerator,
            showAlert: true,
        }));
        return;
    }

    console.log("Attempting to save...");

    try {
        await fetch(`http://127.0.0.1:8000/modify-user/${editedModerator.email}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: editedModerator.email,
                nom: editedModerator.nom,
                prenom: editedModerator.prenom,
                hashed_password: editedModerator.hashed_password,
            })
        });

        console.log("Update successful.");

        const response = await fetch(`http://127.0.0.1:8000/get-user/${editedModerator.email}`);
        const updatedUserData = await response.json();

        setEditedModerator(updatedUserData);
        onClose();
    } catch (error) {
        console.error("Update failed. Handle the error:", error.message);
        setEditedModerator((prevModerator) => ({
            ...prevModerator,
            showAlert: true,
        }));
    }
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
          <label>Prénom</label>
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
            type="text"
            name="hashed_password"
            placeholder={selectedModerator.hashed_password}
            value={editedModerator.hashed_password}
            onChange={handleInputChange}
          />
        </div>

        <div className="form-buttons">
          <button className="save-button" onClick={handleSave}>
            Enregistrer
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