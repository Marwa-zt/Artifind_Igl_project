// ModeratorsList.jsx

import React, { useState } from "react";
import "./moderatorsList.css";
import modifyIcon from "../../assets/modifyIcon.png";
import deleteIcon2 from "../../assets/deleteIcon2.png";
import EditForm from "./EditForm"; // Import the EditForm component
import ConfirmationModal from "./ConfirmationModal";
import axios from "axios";

const ModeratorsList = ({ moderators, setModerators }) => {
  const [selectedModerator, setSelectedModerator] = useState(null);
  const [isConfirmationModalVisible, setIsConfirmationModalVisible] =
    useState(false); // Add this line

  const handleModifier = (id) => {
    // Find the selected moderator based on the id
    const selected = moderators.find((moderator) => moderator.id === id);
    setSelectedModerator(selected);
  };

  const handleSupprimer = (email) => {
    setSelectedModerator(moderators.find((moderator) => moderator.email === email));
    setIsConfirmationModalVisible(true);
  };
  
  const handleConfirmDelete = async () => {
    try {
      const response = await axios.delete(
        `http://127.0.0.1:8000/delete-user/${selectedModerator.email}`
      );
  
      if (response.status === 200) {
        // If the deletion is successful, update the state to remove the selected moderator
        setModerators((prevModerators) =>
          prevModerators.filter((moderator) => moderator.email !== selectedModerator.email)
        );
      } else {
        console.error("Failed to delete moderator");
      }
    } catch (error) {
      console.error("Error deleting moderator:", error);
    } finally {
      setIsConfirmationModalVisible(false);
      setSelectedModerator(null);
    }
  };
  
  const handleCancelDelete = () => {
    setIsConfirmationModalVisible(false);
  };
  

  const [shouldCloseForm, setShouldCloseForm] = useState(false);
  const [showAlert, setShowAlert] = useState(false); // Add this line

  const checkUserExistence = async (email) => {
    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/get-user/${email}`
      );

      if (response.status === 200) {
        console.log(`User with email ${email} exists. Details:`, response.data);
        return true;
      } else {
        console.log(`Unexpected response status: ${response.status}`);
      }
    } catch (error) {
      if (error.response && error.response.status === 404) {
        console.log(`User with email ${email} does not exist.`);
        return false;
      }
      console.error(`Error checking user existence: ${error.message}`);
    }

    return false; // Default to false if there's an error or unexpected status
  };

  const handleUpdateModerator = async (updatedModerator, onUpdateCallback) => {
    try {
      console.log("Handling update...");
      const userExists = await checkUserExistence(updatedModerator.email);

      if (!userExists) {
        // Handle the case where the user does not exist
        console.log("User does not exist. Handle accordingly.");
        return;
      }

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
          return; // Set showAlert to true after alert is shown
        });
        // Do not close the form if there's an error
      } else {
        console.log("ID is unique. Updating moderator...");

        const response = await fetch(
          `http://127.0.0.1:8000/modify-user/${updatedModerator.email}`,
          {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(updatedModerator),
          }
        );

        if (response.ok) {
          // Update React state after successful API request
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
        } else {
          // Pass false to the callback to indicate that the update failed
          onUpdateCallback(false);
          console.error("Failed to update moderator");
        }
      }
    } catch (error) {
      console.error("Error updating moderator:", error);
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
              <button onClick={() => handleSupprimer(moderator.email)}>
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
          key={selectedModerator.id} // Add this line
          selectedModerator={selectedModerator}
          onUpdate={handleUpdateModerator}
          onClose={handleCloseForm}
          showAlert={showAlert}
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
