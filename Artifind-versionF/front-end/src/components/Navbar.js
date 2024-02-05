import React,{useState} from "react";
import logo from "../logo.svg";
import LogIn from "./Login";
import {AiOutlineClose,AiOutlineMenu} from 'react-icons/ai'
import { Link } from 'react-router-dom';

const Navbar = () => {
  const [nav, setNav] = useState(true)
  const handleNav = () => {
    setNav(!nav)
  }
  const [menuleft, setmenuleft] = useState(false)
    const handlemenu = () => {
      setmenuleft(!menuleft)
    }
  const [log, setLog] = useState(false)
    const handleLog = () => {
      setLog(!log)
    }
    return (
        <div>
        {log && <LogIn/>}
        <div className='fixed w-full bold-text text-white flex justify-between items-center h-16 max-w-full mx-auto px-8 z-20 rounded-full bg-black/30'>
          
          <img  className='h-auto max-w-xs px-8 ' src={logo} alt="logo" />
          <div className=" hidden md:flex justify-between items-center h-24 max-w-[1240px]  px-4">
          <ul className="flex px-28">
            <li className='p-14'><Link to="/">Accueil</Link></li>
            <li className='p-14'><Link to="/Apropos">Àpropos</Link></li>
            <li className='p-14'>FAQ</li>
          </ul>
          <button onClick={handleLog} className="bg-white text-[#D5DD18] w-[90px] hover:border border-spacing-1 border-white hover:bg-transparent transition duration-300 ease-in-out rounded-3xl py-2 ">LogIn</button>
          </div>
          <div onClick={handleNav} className="block md:hidden">
            {!nav? <AiOutlineClose size={20}/>:<AiOutlineMenu size={20}/>}
            </div>
          <div className={ !nav ? 'fixed left-0 top-0 w-[60%] h-[70%] bg-[#142832] ease-in-out duration-500 rounded-3xl' : ' fixed left-[-100%]'}>
          <img  className='h-auto max-w-xs m-4 ' src={logo} alt="logo" />
          <ul className="p-4">
            <li className='p-5 border-b border-gray-600'><Link to="/">Accueil</Link></li>
            <li className='p-5 border-b border-gray-600'><Link to="/Apropos">Àpropos</Link></li>
            <li className='p-5'>FAQ</li>
            <button onClick={ handleLog && handleNav} className=" bg-white text-[#D5DD18] w-[90px] rounded-3xl py-2 my-8 mx-auto">LogIn</button>
            
          </ul>
           </div>
         </div>
         </div>
      );
}
 
export default Navbar;