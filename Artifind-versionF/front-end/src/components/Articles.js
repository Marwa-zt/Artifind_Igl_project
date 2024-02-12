import React, { useEffect, useState } from "react";
import NavMenu from "./NavMenu";
import { FaSearch } from "react-icons/fa";
import Footer from "./Footer";
import { IoFilter } from "react-icons/io5";
import { useNavigate, useLocation } from "react-router-dom";

const Articles = () => {
    const navigate = useNavigate();
    const location = useLocation();

    
    const searchParams = new URLSearchParams(location.search);
    const FormarticleString = searchParams.get('Formarticle');
    const Formarticle = FormarticleString ? JSON.parse(FormarticleString) : [];

    console.log(Formarticle);
    const handleClick = () => {
        navigate(`/Article?Formarticle=${encodeURIComponent(JSON.stringify(Formarticle.index))}`);
    }
   const handlefilter = () =>{
    navigate('Fav');
   }

    return (
        <div>
        <div className="absolute bg-[#142832] justify-center h-full w-full">
            <NavMenu />
            <div className="pt-24 pb-3 mx-10 lg:mx-40 border-b-2 border-b-gray-300 flex justify-center items-center">
                <form className="w-[60%] relative m-4 p-2 rounded-full bg-white border border-[#D5DD18]" action="">
                    <div className="relative flex">
                        <input type="search" placeholder='Filtrer..' className="outline-none w-[80%]" />
                        <button className="absolute right-12 top-1/2 -translate-y-1/2 p-2 bg-[#D5DD18] rounded-full">
                            <IoFilter onClick={handlefilter}  className="text-white" size={20} />
                        </button>
                        <button className="absolute right-1 top-1/2 -translate-y-1/2 p-2 bg-[#D5DD18] rounded-full">
                            <FaSearch className="text-white" size={20} />
                        </button>
                    </div>
                </form>
            </div>

            <ul className="text-white py-6 mx-10 lg:mx-40 border-b border-b-gray-300 flex flex-col">

                {Formarticle.length === 0 ? (
                    <div className="text-white py-6 mx-10 lg:mx-40 border-b border-b-gray-300 flex flex-col">
                        <h1 className="font-bold text-xl lg:text-3xl py-3">Pas de résultat trouvé</h1>
                    </div>
                ) : (
                    Formarticle.map((article, index) => (
                        <div className="text-white py-6 mx-10 lg:mx-40 border-b border-b-gray-300 flex flex-col" key={index}>
                            <h1 onClick={handleClick} className="font-bold text-xl lg:text-3xl py-3 cursor-pointer">{article.titre} :</h1>
                            <p className="lg:text-2xl py-2">{article.resume ? article.resume : 'pas de résumé.'}</p>
                            <div className="flex">
                                <h3 className="lg:text-2xl font-bold">Mots clé : </h3>
                                <p className="px-4 py-1.5">{article.motscles ? article.motscles : 'pas de mot clé!'}</p>
                            </div>
                        </div>
                    ))
                )}
            </ul>
            <Footer />
        </div>
        </div>
    );
}

export default Articles;
