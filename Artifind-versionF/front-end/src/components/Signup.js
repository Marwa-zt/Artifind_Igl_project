import React, { useState, useEffect } from "react";
import { MdAlternateEmail } from "react-icons/md";
import { FaLock, FaUserCheck, FaGoogle } from "react-icons/fa";
import { AiOutlineClose } from 'react-icons/ai'
import axios from "axios";
import { useNavigate } from 'react-router-dom';

const Signup = () => {

  let nav = useNavigate();

  const [formData, setFormData] = useState({
    email: '',
    nom: '',
    prenom: '',
    password: '',
  });

  const handleSubmite = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:8000/auth', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        const result = await response.json();
        console.log(result);
        nav(`/Landingpage?value=${formData.email}`);
        // Handle successful signup, maybe redirect the user to another page
      } else {
        // Handle error response from the server
        console.error('Signup failed');
        alert('Email already registered!');
      }
    } catch (error) {
      console.error('Error during signup:', error);
    }
  };


  const [isLoginPageVisible, setLoginPageVisible] = useState(true);

  const handleCloseButtonClick = () => {
    setLoginPageVisible(false);
  };
  return (
    <div>
      {isLoginPageVisible && (

        <div className="fixed text-white left-0 top_0 w-full h-screen bg-black/70 px-4 py-7 flex_col z-10">

          <div className='mx-auto flex md:w-[50%] m-[5%] py-8 justify-center border-2 border-solid border-white border-opacity-20 backdrop-filter backdrop-blur  rounded-3xl transition ease-in-out duration-500 '>
            <AiOutlineClose className="absolute right-6 top-6 cursor-pointer" onClick={handleCloseButtonClick} size={20} />
            <form onSubmit={(e) => handleSubmite(e)} className="flex flex-col md:text-xl items-center" action="">
              <h1 className="font-bold p-6 text-xl md:text-3xl">Sign up</h1>
              <div className="input_box  flex py-4 border-b border-gray-300 justify-between items-center ">
                <input className="border-none outline-none bg-transparent px-5" type="email" placeholder="Email" onChange={(e) => setFormData({ ...formData, email: e.target.value })} value={formData.email} required />
                <MdAlternateEmail />
              </div>
              <div className="input_box flex py-4 border-b border-gray-300 justify-between items-center">
                <input className="border-none outline-none bg-transparent px-5" type="name" placeholder="Nom d'utilisateur" onChange={(e) => setFormData({ ...formData, nom: e.target.value },{...formData, prenom: e.target.value})} value={formData.nom} required />
                <FaUserCheck />
              </div>
              <div className="input_box flex py-4 border-b border-gray-300  text-gray-900  items-center">
                <input className="border-none outline-none bg-transparent px-5 text-white" type="password" placeholder="Mot de passe" onChange={(e) => setFormData({...formData, password: e.target.value})} value={formData.password} required />
                <FaLock className="text-white" />
              </div>
              <div className="justify-center flex text-white ">
                <button className="bg-[#D5DD18] w-[250px] cursor-pointer font-bold rounded-3xl mt-16 mb-1 mx-auto py-2" type="submit">Créer un compte</button>
              </div>
              <div className="bg-white text-gray-900 w-[250px] cursor-pointer flex justify-center font-bold text-sm  rounded-3xl mt-2 mb-4 mx-auto py-2 ">
                <FaGoogle className="m-2" />
                <button type="submit">Continuer avec Google</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
export default Signup;