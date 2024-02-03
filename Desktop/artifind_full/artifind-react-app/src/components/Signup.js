import React,{useState,useEffect} from "react";
import { MdAlternateEmail } from "react-icons/md";
import { FaLock , FaUserCheck,FaGoogle} from "react-icons/fa"; 
import {AiOutlineClose} from 'react-icons/ai'
import axios from "axios";
import { useNavigate } from 'react-router-dom';

const Signup = () => {
   

   const [email,setEmail] = useState('');
   const [pwd, setpwd] = useState('');
   const [nom,setnom] = useState('');
   const [prenm,setprenom] = useState('');
   let nav = useNavigate();
   const handleSubm = () =>{
    nav('/Landingpage');
   }
   const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:8000/auth/', {
        email: email,
        nom: nom,
        prenom: prenm,
        password: pwd,
      }
      , {
        withCredentials: true,
       });
      console.log('Data added successfully:', response.data);
      nav('/Landingpage');
    } catch (error) {
      console.error('Error adding data:', error);
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
             <AiOutlineClose className="absolute right-6 top-6 cursor-pointer" onClick={handleCloseButtonClick} size={20}/>
             <form onSubmit={()=> handleSubm() } className="flex flex-col md:text-xl items-center" action="">
                  <h1 className="font-bold p-6 text-xl md:text-3xl">Sign up</h1>
                  <div className="input_box  flex py-4 border-b border-gray-300 justify-between items-center ">
                      <input className="border-none outline-none bg-transparent px-5" type="email" placeholder="Email" onChange={(e)=>setEmail(e.target.value)} value={email} required/>
                      <MdAlternateEmail />
                  </div>
                  <div className="input_box flex py-4 border-b border-gray-300 justify-between items-center">
                      <input className="border-none outline-none bg-transparent px-5" type="name" placeholder="Nom d'utilisateur" onChange={(e)=>setnom(e.target.value) && setprenom(e.target.value)} value={nom} required/>
                      <FaUserCheck/>
                  </div>
                  <div className="input_box flex py-4 border-b border-gray-300  text-gray-900  items-center">
                      <input className="border-none outline-none bg-transparent px-5 text-white" type="password" placeholder="Mot de passe" onChange={(e)=>setpwd(e.target.value)} value={pwd}required/>
                      <FaLock className="text-white"/>
                  </div>
                  <div className="justify-center flex text-white ">
                     <button className="bg-[#D5DD18] w-[250px] cursor-pointer font-bold rounded-3xl mt-16 mb-1 mx-auto py-2" type="submit">Créer un compte</button>
                   </div>
                   <div  className="bg-white text-gray-900 w-[250px] cursor-pointer flex justify-center font-bold text-sm  rounded-3xl mt-2 mb-4 mx-auto py-2 ">
                     <FaGoogle className="m-2"/>
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