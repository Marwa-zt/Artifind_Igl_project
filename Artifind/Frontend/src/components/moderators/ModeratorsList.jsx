// ModeratorsList.jsx

import React, { useState } from "react";
import "./moderatorsList.css";
import modifyIcon from "../../assets/modifyIcon.png";
import deleteIcon2 from "../../assets/deleteIcon2.png";
import EditForm from "./EditForm"; // Import the EditForm component
import ConfirmationModal from "./ConfirmationModal";

const ModeratorsList = ({ moderators, setModerators }) => {
  const [selectedModerator, setSelectedModerator] = useState(null);
  const [isConfirmationModalVisible, setIsConfirmationModalVisible] =
    useState(false); // Add this line

  const handleModifier = (id) => {
    // Find the selected moderator based on the id
    const selected = moderators.find((moderator) => moderator.id === id);
    setSelectedModerator(selected);
  };

  const handleSupprimer = (id) => {
    setSelectedModerator(moderators.find((moderator) => moderator.id === id));
    setIsConfirmationModalVisible(true);
  };

  const handleConfirmDelete = () => {
    const updatedModerators = moderators.filter(
      (moderator) => moderator.id !== selectedModerator.id
    );
    setModerators(updatedModerators);
    setIsConfirmationModalVisible(false);
    setSelectedModerator(null);
  };

  const handleCancelDelete = () => {
    setIsConfirmationModalVisible(false);
  };

  const [shouldCloseForm, setShouldCloseForm] = useState(false);
  const [showAlert, setShowAlert] = useState(false); // Add this line

  const handleUpdateModerator = (updatedModerator, onUpdateCallback) => {
    console.log("Handling update...");
    const isIdUnique = !moderators.some(
      (moderator) =>
        String(moderator.id) === String(updatedModerator.id) &&
        moderator.id !== selectedModerator.id
    );

    if (!isIdUnique) {
      console.log("ID not unique. Update failed.");
      // Pass false to the callback to indicate that the update failed
      onUpdateCallback(false);
      // Use the callback form of setShowAlert to ensure the state update is completed
      setShowAlert((prevShowAlert) => {
        if (!prevShowAlert) {
          alert(
            "The new id already exists in the list. Please choose a different ID."
          );
          console.error("Error: The new id already exists in the list.");
        }
        return ; // Set showAlert to true after alert is shown
      });
      // Do not close the form if there's an error
    } else {
      console.log("ID is unique. Updating moderator...");
      setModerators((prevModerators) => {
        const updatedModerators = prevModerators.map((moderator) =>
          moderator.id === selectedModerator.id
            ? { ...updatedModerator }
            : { ...moderator }
        );
        return updatedModerators;
      });
      // Set showAlert to false after a successful update
      setShowAlert(false);

      // Pass true to the callback to indicate that the update was successful
      onUpdateCallback(true);

      // Close the form after updating moderator (now handled in handleSave)
      // onClose();
    }
  };

  const handleCloseForm = () => {
    setSelectedModerator(null);
    // Close the form only if shouldCloseForm is true
    if (shouldCloseForm) {
      setShouldCloseForm(false); // Reset the state for the next time
    }
  };

  return (
    <div className="moderators-list">
      <div className="titles-mods">
        <div>Nom</div>
        <div>Prenom</div>
        <div>E-mail</div>
        <div>Id</div>
        <div></div>
      </div>
      <div className="separator"></div>
      <div className="mods-container">
        {moderators.map((moderator) => (
          <div key={moderator.id} className="moderator">
            <div>{moderator.nom}</div>
            <div>{moderator.prenom}</div>
            <div>{moderator.email}</div>
            <div>{moderator.id}</div>
            <div className="buttons">
              <button onClick={() => handleModifier(moderator.id)}>
                <img
                  src={modifyIcon}
                  alt="Modify Icon"
                  className="buttonIcon"
                />
                Modifier
              </button>
              <button onClick={() => handleSupprimer(moderator.id)}>
                <img
                  src={deleteIcon2}
                  alt="Delete Icon"
                  className="buttonIcon"
                />
                Supprimer
              </button>
            </div>
          </div>
        ))}
      </div>
      {selectedModerator && !isConfirmationModalVisible && (
        <EditForm
          selectedModerator={selectedModerator}
          onUpdate={handleUpdateModerator}
          onClose={handleCloseForm}
          showAlert={showAlert} // Pass showAlert as a prop
          setShowAlert={setShowAlert}
        />
      )}

      {isConfirmationModalVisible && (
        <ConfirmationModal
          onConfirm={handleConfirmDelete}
          onCancel={() => {
            handleCloseForm(); // Close the EditForm when cancel is clicked
            handleCancelDelete(); // Cancel the deletion
          }}
        />
      )}
    </div>
  );
};

export default ModeratorsList;

/*
 // ModeratorsList.jsx
import React, { useState, useEffect } from "react";
import "./moderatorsList.css";
import modifyIcon from "../../assets/modifyIcon.png";
import deleteIcon2 from "../../assets/deleteIcon2.png";
import EditForm from "./EditForm";
import ConfirmationModal from "./ConfirmationModal";
import axios from "axios";

const ModeratorsList = ({ moderators, setModerators }) => {
  const [selectedModerator, setSelectedModerator] = useState(null);
  const [isConfirmationModalVisible, setIsConfirmationModalVisible] =
    useState(false);

  const handleModifier = (id) => {
    const selected = moderators.find((moderator) => moderator.id === id);
    setSelectedModerator(selected);
  };

  const handleSupprimer = (id) => {
    setSelectedModerator(moderators.find((moderator) => moderator.id === id));
    setIsConfirmationModalVisible(true);
  };

  const handleConfirmDelete = async () => {
    try {
      // Send a DELETE request to delete the moderator
      const response = await axios.delete(
        `your_api_endpoint/moderators/${selectedModerator.id}`
      );

      // Check the response for success
      if (response.data.success) {
        const updatedModerators = moderators.filter(
          (moderator) => moderator.id !== selectedModerator.id
        );
        setModerators(updatedModerators);
        setIsConfirmationModalVisible(false);
        setSelectedModerator(null);
      } else {
        console.error("Error deleting moderator:", response.data.error);
      }
    } catch (error) {
      console.error("Error deleting moderator:", error.message);
    }
  };

  const handleCancelDelete = () => {
    setIsConfirmationModalVisible(false);
  };

  const [shouldCloseForm, setShouldCloseForm] = useState(false);
  const [showAlert, setShowAlert] = useState(false);

  const handleUpdateModerator = async (updatedModerator, onUpdateCallback) => {
    try {
      const response = await axios.put(
        `your_api_endpoint/moderators/${updatedModerator.id}`,
        updatedModerator
      );

      if (response.data.success) {
        setModerators((prevModerators) => {
          const updatedModerators = prevModerators.map((moderator) =>
            moderator.id === selectedModerator.id
              ? { ...updatedModerator }
              : { ...moderator }
          );
          return updatedModerators;
        });
        setShowAlert(false);
        onUpdateCallback(true);
      } else {
        onUpdateCallback(false);
        setShowAlert(true);
        alert(
          "The new id already exists in the list. Please choose a different ID."
        );
        console.error("Error: The new id already exists in the list.");
      }
    } catch (error) {
      console.error("Error updating moderator:", error.message);
    }
  };

  const handleCloseForm = () => {
    setSelectedModerator(null);
    if (shouldCloseForm) {
      setShouldCloseForm(false);
    }
  };

  return (
    <div className="moderators-list">
      {/* ... (rest of the component remains unchanged) */
      /*</div>
      );
    };
    
    export default ModeratorsList;
    
*/