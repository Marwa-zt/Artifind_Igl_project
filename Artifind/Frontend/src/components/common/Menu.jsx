// Menu.jsx
import React from "react";
import { Link } from "react-router-dom";
import "./Menu.css";
import menuIcon from "../../assets/cancel.png";
import profileIcon from "../../assets/profileIcon.png";
import icon1 from "../../assets/icon1.svg";
import icon2 from "../../assets/icon2.svg";
import icon3 from "../../assets/icon3.svg";
import icon4 from "../../assets/icon4.svg";

const Menu = () => {
  return (
    <div className="menu show">
      <div className="menu-header">
        <img className="menu--icon" src={menuIcon} alt="Menu Icon" />
      </div>
      <div className="menu-content">
        <div className="profile-info">
          <img className="profile-icon" src={profileIcon} alt="Profile Icon" />
          <div className="profile-text">
            <p>Administrateur</p>
          </div>
        </div>
        <div className="menu--content">
          {/* Use Link components to create navigation links */}
          <Link to="/liste-des-articles" className="menu-item">
            <img className="menu-item-icon" src={icon1} alt="Icon 1" />
            <p className="menu-text">Liste des articles</p>
          </Link>
          <Link to="/gestion-des-moderateurs" className="menu-item">
            <img className="menu-item-icon" src={icon2} alt="Icon 2" />
            <p className="menu-text">Gestion des modérateurs</p>
          </Link>
          <Link to="/importation-des-articles" className="menu-item">
            <img className="menu-item-icon" src={icon3} alt="Icon 3" />
            <p className="menu-text">Importation des articles scientifiques</p>
          </Link>
          <Link to="/deconnecter" className="menu-item">
            <img className="menu-item-icon" src={icon4} alt="Icon 4" />
            <p className="menu-text">Déconnecter</p>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Menu;
