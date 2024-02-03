// Moderators.jsx
import React, { useState, useEffect } from "react";
import "./moderators.css";
import addIcon from "../../assets/addIcon.png";
import searchIcon from "../../assets/searchIcon.png";
import ModeratorsList from "./ModeratorsList";
import AddForm from "./AddForm";
import axios from "axios";

const Moderators = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [isAddFormVisible, setIsAddFormVisible] = useState(false);
  const [moderators, setModerators] = useState([]);

  const filteredModerators = moderators.filter(
    (moderator) =>
      moderator.nom.toLowerCase().includes(searchQuery.toLowerCase()) ||
      moderator.prenom.toLowerCase().includes(searchQuery.toLowerCase()) ||
      moderator.email.toLowerCase().includes(searchQuery.toLowerCase()) ||
      String(moderator.id).includes(searchQuery)
  );

  useEffect(() => {
    const fetchModerators = async () => {
      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/admin/get_moderators"
        );

        setModerators(response.data);
      } catch (error) {
        console.error("Error fetching moderators:", error.message);
      }
    };

    fetchModerators();
  }, []);
  
  const handleAddClick = async (newModerator) => {
    try {
      // Send a POST request to add a new moderator
      console.log("New Moderator Object:", newModerator);
      const response = await axios.post(
        "http://127.0.0.1:8000/admin/create_user",
        newModerator
      );
  
      // Check the response for success
      if (response.status === 201) {
        setModerators((prevModerators) => [...prevModerators, response.data]);
        setIsAddFormVisible(false);
      } else {
        alert("Failed to add moderator. Please try again.");
      }
    } catch (error) {
      console.error("Error adding moderator:", error.message);
      console.log("Error response:", error.response); // Add this line for debugging
    }
  };
  

  return (
    <>
      <div className="moderators-container">
        <div className="centered-text">
          <h1>Gérer les modérateurs</h1>
        </div>
        <div className="moderator-info">
          <div className="moderator-count">
            <div className="rectangle">
              <p>{filteredModerators.length} mods</p>
            </div>
            <button
              className="add-mod-button"
              onClick={() => setIsAddFormVisible(true)}
            >
              <img src={addIcon} alt="Add Icon" />
              Add Mod
            </button>
          </div>

          <div className="search-bar">
            <img src={searchIcon} alt="Search Icon" />
            <input
              type="text"
              placeholder="Rechercher un mod"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
        </div>
      </div>

      {isAddFormVisible ? (
        <div className="modal-overlay">
          <AddForm
            onAdd={handleAddClick}
            onClose={() => setIsAddFormVisible(false)}
            allModerators={moderators}
          />
        </div>
      ) : (
        <ModeratorsList
          moderators={filteredModerators}
          setModerators={setModerators}
        />
      )}
    </>
  );
};

export default Moderators;