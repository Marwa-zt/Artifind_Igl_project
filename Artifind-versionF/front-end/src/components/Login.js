import React, { useState, useEffect } from "react";
import { MdAlternateEmail } from "react-icons/md";
import { FaLock } from "react-icons/fa";
import { AiOutlineClose } from 'react-icons/ai'
import axios from 'axios'
import { Navigate, useNavigate } from 'react-router-dom';
import { Link } from "react-router-dom";
const Loginn
  = () => {
    let nav = useNavigate();

    const [formData, setFormData] = useState({
      email: '',
      password: '',
    });

    const handleloge = async (e) => {
      e.preventDefault();

      try {
        const response = await fetch('http://localhost:8000/auth/token', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(formData),
        });

        if (response.ok) {
          const result = await response.json();
          console.log(result);
          fetch('http://localhost:8000/auth/users/me', {
            method: 'GET',
            headers: {
              'Authorization': 'Bearer ' + 'http://localhost:8000/auth/token',
              'Content-Type': 'application/json',

            },
          })
            .then(response => {
              if (!response.ok) {
                throw new Error('Network response was not ok');
              }
              return response.json();
            })
            .then(data => {
              // Assuming the response contains user data in JSON format
              console.log('User data:', data);
              // Access email and password from the data object
              const { email, password } = data;
              console.log('Email:', email);
              console.log('Password:', password);
            })
            .catch(error => {
              console.error('Error fetching user data:', error);
            });
            nav(`/Landingpage?value=${formData.email}`);

        } else {
          alert("l'utilisateur n'existe pas.Veuillez s'inscrire svp.");
          console.error('LogiIn failed');
        }

      } catch (error) {
        console.error('Error during login:', error);
      }
    };

    // const handleloge = async (e) => {
    //   e.preventDefault();

    //   try {
    //     const response = await axios.post('http://localhost:8000/auth/token', formData, {
    //       headers: {
    //         'Content-Type': 'application/json',
    //       },
    //     });

    //     if (response.status === 200) {
    //       const result = response.data;
    //       console.log(result);
    //     } else {
    //       console.error('Login failed');
    //     }
    //   } catch (error) {
    //     console.error('Error during login:', error);
    //   }
    // };

    const [isLoginPageVisible, setLoginPageVisible] = useState(true);

    const handleCloseButtonClick = () => {
      setLoginPageVisible(false);
    };
    return (
      <div>
        {isLoginPageVisible && (
          <div className="fixed text-white left-0 top_0 w-full h-screen bg-black/70 px-4 py-7 flex_col z-10">
            <div className='mx-auto flex md:w-[40%] m-[10%] py-10 justify-center border-2 border-solid border-white border-opacity-20 backdrop-filter backdrop-blur  rounded-3xl ease-in-out duration-500 '>
              <AiOutlineClose className="absolute right-6 top-6 cursor-pointer" onClick={handleCloseButtonClick} size={20} />
              <form onSubmit={(e) => handleloge(e)} className="flex flex-col md:text-xl items-center" action="">
                <h1 className="font-bold p-4 text-xl md:text-3xl">Login</h1>
                <div className="input_box px-11 flex py-4 border-b border-gray-300 justify-between items-center">
                  <input className="border-none outline-none bg-transparent px-5" type="email" placeholder="Email" onChange={(e) => setFormData({ ...formData, email: e.target.value })} value={formData.email} required />
                  <MdAlternateEmail />
                </div>
                <div className="input_box px-11 flex py-4 border-b border-gray-300 justify-between items-center">
                  <input className="border-none outline-none bg-transparent px-5" type="password" placeholder="Mot de passe" onChange={(e) => setFormData({ ...formData, password: e.target.value })} value={formData.password} required />
                  <FaLock />
                </div>
                <div className="justify-center flex text-white ">
                  <button className="bg-[#24A393] w-[200px] cursor-pointer  rounded-3xl mt-16 mb-4 mx-auto py-2" type="submit">Se connecter</button>
                </div>
                <p>Je n’ai Pas de compte, <a className="cursor-pointer underline text-[#D5DD18]"><Link to="Singup">S'inscrire</Link> </a></p>
              </form>
            </div>
          </div>
        )}
      </div>
    );
  }

export default Loginn
  ;