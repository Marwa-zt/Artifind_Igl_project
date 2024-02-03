import React, { useState } from "react";
import "./addForm.css";
import addIcon from "../../assets/addIcon.png";
import axios from "axios";

const AddForm = ({ onAdd, onClose }) => {
  const [newModerator, setNewModerator] = useState({
    nom: "",
    prenom: "",
    email: "",
    hashed_password: "",
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewModerator((prevModerator) => ({ ...prevModerator, [name]: value }));
  };

  const handleAddClick = async () => {
    try {
      // Check if all fields are filled
      if (
        newModerator.nom &&
        newModerator.prenom &&
        newModerator.email &&
        newModerator.hashed_password
      ) {
        // Attempt to get user data (will result in a 404 if the user does not exist)
        await axios.get(`http://127.0.0.1:8000/get-user/${newModerator.email}`);
  
        // If no error occurred, the user already exists
        alert("Email already exists. Please use a different email.");
        return;
      }
  
      // Send a POST request to add a new moderator
      const response = await axios.post(
        "http://127.0.0.1:8000/admin/create_user",
        newModerator,
        { withCredentials: true }
      );
  
      // Check the response for success
      if (response.status === 201) {
        onAdd(newModerator);
        onClose();
      } else {
        alert("Failed to add moderator. Please try again.");
      }
    } catch (error) {
      if (error.response) {
        if (error.response.status === 404) {
          // Handle the 404 status (user does not exist), proceed with creating the new user
          const createResponse = await axios.post(
            "http://127.0.0.1:8000/admin/create_user",
            newModerator,
            { withCredentials: true }
          );
  
          // Check the response for success
          if (createResponse.status === 201) {
            onAdd(newModerator);
            onClose();
          } else {
            alert("Failed to add moderator. Please try again.");
          }
        } else if (error.response.status === 422) {
          // Handle the 422 status (Unprocessable Entity - missing fields)
          alert("All fields are required. Please fill in all the fields.");
        } else {
          // Handle other errors
          console.error("Error adding moderator:", error.message);
  
          // Log the error response for further investigation
          console.error("Error response:", error.response);
  
          // Handle other error scenarios if needed
        }
      } else {
        // Handle other errors
        console.error("Error adding moderator:", error.message);
      }
    }
  };
  
  

  return (
    <div className="add-form">
      <div className="form-title">
        <img src={addIcon} alt="Add Icon" className="buttonIcon" />
        <span>Ajouter un nouveau modérateur</span>
      </div>
      <div className="form-label">
        <label>Nom</label>
        <input
          type="text"
          placeholder="Nom"
          name="nom"
          value={newModerator.nom}
          onChange={handleInputChange}
        />
      </div>
      <div className="form-label">
        <label>Prenom</label>
        <input
          type="text"
          placeholder="Prenom"
          name="prenom"
          value={newModerator.prenom}
          onChange={handleInputChange}
        />
      </div>
      <div className="form-label">
        <label>E-mail</label>
        <input
          type="email"
          placeholder="E-mail"
          name="email"
          value={newModerator.email}
          onChange={handleInputChange}
        />
      </div>
      <div className="form-label">
        <label>Mot de passe</label>
        <input
          type="password"
          placeholder="Mot de passe"
          name="hashed_password"
          value={newModerator.hashed_password}
          onChange={handleInputChange}
        />
      </div>
      <div className="form-buttons">
        <button className="save-button" onClick={handleAddClick}>
          Enregistrer
        </button>
        <button className="cancel-button" onClick={onClose}>
          Annuler
        </button>
      </div>
    </div>
  );
};

export default AddForm;
