import React,{useState} from "react";
import { MdAlternateEmail } from "react-icons/md";
import { FaLock } from "react-icons/fa"; 
import {AiOutlineClose} from 'react-icons/ai'

const Loginn
 = () => {
  const [isLoginPageVisible, setLoginPageVisible] = useState(true);

  const handleCloseButtonClick = () => {
    setLoginPageVisible(false);
  };
    return ( 
       <div>
        {isLoginPageVisible && (

        <div className="fixed text-white left-0 top_0 w-full h-screen bg-black/70 px-4 py-7 flex_col z-10">
          
          <div className='mx-auto flex md:w-[40%] m-[10%] py-10 justify-center border-2 border-solid border-white border-opacity-20 backdrop-filter backdrop-blur  rounded-3xl ease-in-out duration-500 '>
           <AiOutlineClose className="absolute right-6 top-6 cursor-pointer" onClick={handleCloseButtonClick} size={20}/>
           <form className="flex flex-col md:text-xl items-center" action="">
                <h1 className="font-bold p-4 text-xl md:text-3xl">Login</h1>
                <div className="input_box px-11 flex py-4 border-b border-gray-300 justify-between items-center">
                    <input className="border-none outline-none bg-transparent px-5" type="email" placeholder="Email" required/>
                    <MdAlternateEmail />
                </div>
                <div className="input_box px-11 flex py-4 border-b border-gray-300 justify-between items-center">
                    <input className="border-none outline-none bg-transparent px-5" type="password" placeholder="Mot de passe" required/>
                    <FaLock/>
                </div>
                <div className="justify-center flex text-white ">
                   <button className="bg-[#24A393] w-[200px] cursor-pointer  rounded-3xl mt-16 mb-4 mx-auto py-2" type="submit">Se connecter</button>
                 </div>
                <p>Je n’ai Pas de compte, <a className="cursor-pointer underline text-[#D5DD18]" href="#"> S'inscrire</a></p>
          </form>
          </div>
        </div>
        )}
       </div>
     );
}
 
export default Loginn
;