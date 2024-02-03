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
       
             <div className='fixed w-full bold-text text-white flex justify-between items-center h-20 max-w-full rounded-3xl mx-auto px-4 z-20 bg-[#142832] border-b-2 border-b-gray-700'>
                        <img  className='fixed h-auto max-w-xs px-8 ' src={logo} alt="logo" />
                        <RiMenu3Line className="fixed right-12 text-[#D5DD18] cursor-pointer" size={30} onClick={handleMenu}/>
                         {menu && <MenuNot/>}
             </div>
       
     );
}
 
export default NavMenu;