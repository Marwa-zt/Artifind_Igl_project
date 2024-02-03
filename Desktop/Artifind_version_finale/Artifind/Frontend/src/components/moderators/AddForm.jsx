// AddForm.jsx
import React, { useState, useEffect } from "react";
import "./addForm.css";
import addIcon from "../../assets/addIcon.png";

const AddForm = ({ onAdd, onClose, allModerators }) => {
  const [newModerator, setNewModerator] = useState({
    nom: "",
    prenom: "",
    email: "",
    password: "",
    id: "",
  });

  const [isIdUnique, setIsIdUnique] = useState(true);

  useEffect(() => {
    // Check if the entered ID is unique across all moderators
    setIsIdUnique(
        !allModerators.some((moderator) => String(moderator.id) === String(newModerator.id))
        );
  }, [newModerator.id, allModerators]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewModerator((prevModerator) => ({ ...prevModerator, [name]: value }));
  };

  const handleAddClick = () => {
    // Check if all fields are filled
    if (
      newModerator.nom &&
      newModerator.prenom &&
      newModerator.email &&
      newModerator.password &&
      newModerator.id
    ) {
      // Ensure ID contains only numbers
      if (!isNaN(newModerator.id)) {
        // Ensure ID is unique across all moderators
        if (isIdUnique) {
          onAdd(newModerator);
          onClose(); // Close the form only when the ID is unique
        } else {
          alert("ID must be unique. Please choose a different ID.");
        }
      } else {
        alert("ID must contain only numbers.");
      }
    } else {
      alert("All fields are required. Please fill in all the fields.");
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
          name="password"
          value={newModerator.password}
          onChange={handleInputChange}
        />
      </div>
      <div className="form-label">
        <label>Id</label>
        <input
          type="text"
          placeholder="Id"
          name="id"
          value={newModerator.id}
          onChange={handleInputChange}
        />
        {!isIdUnique && <p className="error-message">ID must be unique</p>}
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


/*
// AddForm.jsx
import React, { useState, useEffect } from "react";
import "./addForm.css";
import addIcon from "../../assets/addIcon.png";
import axios from "axios";

const AddForm = ({ onAdd, onClose, allModerators }) => {
  const [newModerator, setNewModerator] = useState({
    nom: "",
    prenom: "",
    email: "",
    password: "",
    id: "",
  });

  const [isIdUnique, setIsIdUnique] = useState(true);

  useEffect(() => {
    // Check if the entered ID is unique across all moderators
    setIsIdUnique(
      !allModerators.some(
        (moderator) => String(moderator.id) === String(newModerator.id)
      )
    );
  }, [newModerator.id, allModerators]);

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
        newModerator.password &&
        newModerator.id
      ) {
        // Ensure ID contains only numbers
        if (!isNaN(newModerator.id)) {
          // Ensure ID is unique across all moderators
          if (isIdUnique) {
            // Send a POST request to add a new moderator
            const response = await axios.post(
              "your_api_endpoint/moderators",
              newModerator
            );

            // Check the response for success
            if (response.data.success) {
              onAdd(newModerator);
              onClose(); // Close the form only when the ID is unique
            } else {
              alert("Failed to add moderator. Please try again.");
            }
          } else {
            alert("ID must be unique. Please choose a different ID.");
          }
        } else {
          alert("ID must contain only numbers.");
        }
      } else {
        alert("All fields are required. Please fill in all the fields.");
      }
    } catch (error) {
      console.error("Error adding moderator:", error.message);
    }
  };

  return (
    <div className="add-form">
      {/* ... (rest of the component remains unchanged) */
      /*</div>
      );
    };
    
    export default AddForm;
    
*/
