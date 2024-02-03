import React from "react";
import { useState } from "react";
import logo from "../logo.svg";
import { RiMenu3Line } from "react-icons/ri";
import MenuNot from "./MenuNot";

const NavMenu = () => {
    
  const [menu, setMenu] = useState(false)
  const handleMenu = () => {
    setMenu(!menu)
  }
    return ( 
       
             <div className='absolute w-full bold-text text-white flex justify-between items-center h-24 max-w-[1240px] mx-auto px-4 z-20'>
                        <img  className='h-auto max-w-xs px-8 ' src={logo} alt="logo" />
                        <RiMenu3Line className="fixed right-12 text-[#D5DD18] cursor-pointer" size={30} onClick={handleMenu}/>
                         {menu && <MenuNot/>}
             </div>
       
     );
}
 
export default NavMenu;