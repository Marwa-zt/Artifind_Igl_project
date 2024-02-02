import { useState } from 'react';
import React  from "react";
import {AiOutlineClose} from 'react-icons/ai'
import { FaRegUserCircle } from "react-icons/fa";
import { MdFavorite } from "react-icons/md";
import { IoIosLogOut } from "react-icons/io";
import ass1 from "../images/ass2.png";
const MenuNot = () => {
    const [isLoginPageVisible, setLoginPageVisible] = useState(true);

  const handleCloseButtonClick = () => {
    setLoginPageVisible(false);
  };
    return ( 
        <div>
        {isLoginPageVisible && (
        <div className="fixed left-0 top_0 bottom-0 w-full h-full bg-black/40 flex_col z-10">
            <div className="fixed top-0  w-full lg:w-1/2 md:w-[60%] h-[55%] right-[-20%] border-r border-r-gray-900 bg-[#142832] rounded-3xl ease-in-out duration-500 p-4">
             <AiOutlineClose className=" text-white cursor-pointer" onClick={handleCloseButtonClick} size={20}/>
            <div className='flex py-4 px-6 border-b border-gray-300 items-center'>
              <FaRegUserCircle className='text-[#24A393]' size={30}/>
              <p className='px-3'> Utilisateur</p>
            </div>
            <div className='text-white font-medium flex flex-col py-20 px-6'>
               <div className='flex items-center py-2'>
                <MdFavorite className='text-white' size={20} />
                <button className='px-2'>Favoris</button>
               </div>
               <div className='flex items-center py-2'>
               <IoIosLogOut  className='text-white' size={20} />
                <button className='px-2'>Déconnecter</button>
               </div>
               <div className='flex items-center px-28 py-3'>
                <img src={ass1} alt="ass1" />
               </div>
            </div>
            </div>
        </div>
        )}
       </div>
     );
}
 
export default MenuNot;