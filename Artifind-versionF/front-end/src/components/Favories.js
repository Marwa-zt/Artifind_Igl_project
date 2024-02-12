import React from "react";
import NavMenu from "./NavMenu";
import { FaStar } from "react-icons/fa";
import Footer from "./Footer";
const Favories = () => {
    return (  
        <div className="absolute bg-[#142832] justify-center ">
         <NavMenu/>
         <div className=" pt-24 pb-3 mx-10 lg:mx-40 border-b-2 border-b-gray-300 flex justify-center items-center ">
            
        </div>
        
        <div className="flex items-center justify-center p-3">
                <FaStar className="text-[#D5DD18]" size={30} />
                <h3 className=" font-bold text-xl lg:text-3xl pt-1 px-3 text-[#D5DD18]"> Favories </h3>
       
        </div>
        
         <div className=" pt-3 pb-3 mx-10 lg:mx-40 border-b-2 border-b-gray-300 flex justify-center items-center ">
            
        </div>
        <div className=" text-white py-6 mx-10 lg:mx-40 border-b border-b-gray-300 flex flex-col">
            <h1 className="font-bold text-xl lg:text-3xl py-3 text-gray-200">Titre d'article</h1>
            <p className="lg:text-2xl py-2">Quelque citations a partir du texte intégral exemple: Google Scholar provides a simple across a wide variety of disciplines and sources: articles, theses, ...  </p>
            <div className="flex">
                <h3 className=" lg:text-2xl font-bold text-gray-200">Mots clé : </h3>
                <p className="px-3">search , google , article , science...</p>
           </div>
        </div>
        <div className=" text-white py-6 mx-10 lg:mx-40 border-b border-b-gray-300 flex flex-col">
            <h1 className="font-bold text-xl lg:text-3xl py-3 text-gray-200">Titre d'article</h1>
            <p className="lg:text-2xl py-2">Quelque citations a partir du texte intégral exemple: Google Scholar provides a simple across a wide variety of disciplines and sources: articles, theses, ...  </p>
            <div className="flex">
                <h3 className=" lg:text-2xl font-bold text-gray-200">Mots clé : </h3>
                <p className="px-3">search , google , article , science...</p>
           </div>
        </div>
        <div className=" text-white py-6 mx-10 lg:mx-40 border-b border-b-gray-300 flex flex-col">
            <h1 className="font-bold text-xl lg:text-3xl py-3 text-gray-200">Titre d'article</h1>
            <p className="lg:text-2xl py-2">Quelque citations a partir du texte intégral exemple: Google Scholar provides a simple across a wide variety of disciplines and sources: articles, theses, ...  </p>
            <div className="flex">
                <h3 className=" lg:text-2xl font-bold text-gray-200">Mots clé : </h3>
                <p className="px-3">search , google , article , science...</p>
           </div>
        </div>
        
        <Footer/>
        </div>
    );
}
 
export default Favories;