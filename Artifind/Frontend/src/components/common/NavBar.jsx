import React, { useState,useEffect,useRef } from 'react';
import Menu from './Menu';
import logo from '../../assets/logoArtifind.png';
import menuIcon from '../../assets/menuIcon.png';
import './NavBar.css';

const NavBar = () => {
  const [isMenuVisible, setMenuVisible] = useState(false);

  const menuRef = useRef(null);


  const toggleMenu = () => {
    setMenuVisible(!isMenuVisible);
  };


  const handleOutsideClick = (event) => {
    if (menuRef.current && !menuRef.current.contains(event.target)) {
      setMenuVisible(false);
    }
  };

  useEffect(() => {
    document.addEventListener('click', handleOutsideClick);

    return () => {
      document.removeEventListener('click', handleOutsideClick);
    };
  }, []);


  return (
    <div className="navbar">
      <img className="logo" src={logo} alt="Website Logo" />
      <img ref={menuRef}
        className="menu-icon"
        src={menuIcon}
        alt="Menu Icon"
        onClick={toggleMenu}
      />
      {isMenuVisible && <Menu />}
    </div>
  );
};

export default NavBar;
