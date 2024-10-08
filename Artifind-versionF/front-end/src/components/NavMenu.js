import React from "react";
import { useState } from "react";
import logo from "../logo.svg";
import { RiMenu3Line } from "react-icons/ri";
import MenuNot from "./MenuNot";

const NavMenu = ({value})  => {
    
  const [menu, setMenu] = useState(false)
  const handleMenu = () => {
    setMenu(!menu)
  }
    return ( 
       
             <div className='fixed w-full bold-text text-white flex justify-between items-center h-16 max-w-full mx-auto px-8 z-20 rounded-full bg-black/30'>
                        <img  className='fixed h-auto max-w-xs px-8 ' src={logo} alt="logo" />
                        <RiMenu3Line className="fixed right-12 text-[#D5DD18] cursor-pointer" size={30} onClick={handleMenu}/>
                         {menu && <MenuNot value={value}/>}
             </div>
       
     );
}
 
export default NavMenu;