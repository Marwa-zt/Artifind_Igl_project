// Moderators.jsx
import React, { useState } from "react";
import "./moderators.css";
import addIcon from "../../assets/addIcon.png";
import searchIcon from "../../assets/searchIcon.png";
import ModeratorsList from "./ModeratorsList";
import AddForm from "./AddForm";

const Moderators = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [isAddFormVisible, setIsAddFormVisible] = useState(false);
  const [moderators, setModerators] = useState([
    {
      id: 1,
      nom: "John",
      prenom: "Doe",
      email: "john@example.com",
      password: "password123",
    },
    {
      id: 2,
      nom: "Jane",
      prenom: "Doe",
      email: "jane@example.com",
      password: "password456",
    },
    // Add more moderators as needed
  ]);

  const filteredModerators = moderators.filter(
    (moderator) =>
      moderator.nom.toLowerCase().includes(searchQuery.toLowerCase()) ||
      moderator.prenom.toLowerCase().includes(searchQuery.toLowerCase()) ||
      moderator.email.toLowerCase().includes(searchQuery.toLowerCase()) ||
      String(moderator.id).includes(searchQuery)
  );

  const handleAddClick = (newModerator) => {
    if (!moderators.some((moderator) => moderator.id === newModerator.id)) {
      setModerators((prevModerators) => [...prevModerators, newModerator]);
    } else {
      alert("ID must be unique. Please choose a different ID.");
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

/* 
// Moderators.jsx
import React, { useState, useEffect } from "react";
import NavBar from "../common/NavBar";
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

  useEffect(() => {
    // Fetch moderators data from the API on component mount
    const fetchModerators = async () => {
      try {
        const response = await axios.get("your_api_endpoint/moderators");
        setModerators(response.data);
      } catch (error) {
        console.error("Error fetching moderators:", error.message);
      }
    };

    fetchModerators();
  }, []); // Empty dependency array to ensure the effect runs only once on mount

  const filteredModerators = moderators.filter(
    (moderator) =>
      moderator.nom.toLowerCase().includes(searchQuery.toLowerCase()) ||
      moderator.prenom.toLowerCase().includes(searchQuery.toLowerCase()) ||
      moderator.email.toLowerCase().includes(searchQuery.toLowerCase()) ||
      String(moderator.id).includes(searchQuery)
  );

  const handleAddClick = async (newModerator) => {
    try {
      // Send a POST request to add a new moderator
      const response = await axios.post(
        "your_api_endpoint/moderators",
        newModerator
      );

      // Check the response for success
      if (response.data.success) {
        setModerators((prevModerators) => [...prevModerators, newModerator]);
        setIsAddFormVisible(false);
      } else {
        alert("Failed to add moderator. Please try again.");
      }
    } catch (error) {
      console.error("Error adding moderator:", error.message);
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
              <p>{moderators.length} mods</p>
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
        <AddForm onAdd={handleAddClick} onClose={() => setIsAddFormVisible(false)} />
      ) : (
        <ModeratorsList moderators={filteredModerators} setModerators={setModerators} />
      )}
    </>
  );
};

export default Moderators;

*/
