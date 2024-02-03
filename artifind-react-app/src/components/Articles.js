import React from "react";
import NavMenu from "./NavMenu";
import { FaSearch } from "react-icons/fa";
import Footer from "./Footer";
import { IoFilter } from "react-icons/io5";
import { useNavigate } from "react-router-dom";
const Articles = () => {
    
        let nav = useNavigate();
        const handelclick = () =>{
            nav('/Article');
        }

    return (  
        <div className="absolute bg-[#142832] justify-center ">
         <NavMenu/>
         <div className=" pt-24 pb-3 mx-10 lg:mx-40 border-b-2 border-b-gray-300 flex justify-center items-center ">
            <form className="w-[60%] relative m-4 p-2 rounded-full bg-white  border border-[#D5DD18]" action="">
                <div className="relative flex ">
                    <input type="search" placeholder="Recherche.." className="outline-none w-[80%]"/>
                    
                        <button className="absolute right-12 top-1/2 -translate-y-1/2 p-2 bg-[#D5DD18] rounded-full">
                        <IoFilter onClick={""} className="text-white" size={20} />
                        </button>

                        <button className="absolute right-1 top-1/2 -translate-y-1/2 p-2 bg-[#D5DD18] rounded-full">
                        <FaSearch className="text-white" size={20}/>
                        </button>
                </div>
            </form>
        </div>
        <div className=" text-white py-6 mx-10 lg:mx-40 border-b border-b-gray-300 flex flex-col">
            <h1 onClick={()=>handelclick() } className="font-bold text-xl lg:text-3xl py-3 cursor-pointer">Titre d'article</h1>
            <p className="lg:text-2xl py-2">Quelque citations a partir du texte intégral exemple: Google Scholar provides a simple across a wide variety of disciplines and sources: articles, theses, ...  </p>
            <div className="flex">
                <h3 className=" lg:text-2xl font-bold">Mots clé : </h3>
                <p className="px-3">search , google , article , science...</p>
           </div>
        </div>
        
        <Footer/>
        </div>
    );
}
 
export default Articles;