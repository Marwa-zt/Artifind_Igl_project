import React from "react";
import NavMenu from "./NavMenu";
import Footer from "./Footer";
import { useState,useLocation } from "react";
const Article = () => {
     const location = useLocation();

    
     const searchParams = new URLSearchParams(location.search);
     const FormarticleString = searchParams.get('Formarticle');
     const Formarticle = FormarticleString ? JSON.parse(FormarticleString) : {};  

    return (
        <div className="absolute bg-[#142832] justify-center ">
         <NavMenu/>
         <div className=" pt-24 pb-3 m-5 mx-10 lg:mx-40 border-b-2 border-b-gray-300 flex justify-center ">
        </div>

        <div className=" text-white py-6 px-6 mx-10 lg:mx-40 border border-gray-300 rounded-xl flex flex-col">
            <div className="flex items-center justify-center">
                <h1 className="font-bold text-xl lg:text-3xl py-5">{Formarticle.titre ? Formarticle.titre: "Titre d'article"}</h1>
            </div>
            <div className="flex flex-col">
                <h3 className=" lg:text-2xl font-bold text-gray-400 ">Résumé: </h3>
                <p className="lg:text-2xl py-2 ml-4">{Formarticle.resume ? Formarticle.resume: "resume"}</p>
           </div>
           <div className="flex ">
                <h3 className=" lg:text-2xl font-bold text-gray-400 ">Auteurs: </h3>
                <p className="px-3 pt-1.5">{Formarticle.auteur ? Formarticle.auteur: "Pas d'auteur"}</p>
           </div>
           <div className="flex">
                <h3 className=" lg:text-2xl font-bold text-gray-400">Institut : </h3>
                <p className="px-3 pt-1.5">search , google , article , science...</p>
           </div>
        
           <div className="flex">
                <h3 className=" lg:text-2xl font-bold text-gray-400">Référence : </h3>
                <p className="px-3 pt-1.5">search , google , article , science...</p>
           </div>
           <div className="flex">
                <h3 className=" lg:text-2xl font-bold text-gray-400">Date : </h3>
                <p className="px-3 pt-1.5">01/01/1976 - 02/01/1977</p>
           </div>
           <div className="flex">
                <h3 className=" lg:text-2xl font-bold text-gray-400">Mots clé : </h3>
                <p className="px-3 pt-1.5">search , google , article , science...</p>
           </div>
           <div className="flex items-center justify-center flex-col">
                <h3 className=" font-bold text-xl lg:text-3xl py-5 text-[#D5DD18]"> Text: </h3>
                <p className="lg:text-2xl py-2 ml-4 pl-4">Resume Quelque citations a partir du texte intégral exemple: Google Scholar provides a simple across a wide variety of disciplines and sources: articles, theses, ... Resume Quelque citations a partir du texte intégral exemple: Google Scholar provides a simple across a wide variety of disciplines and sources: articles, theses, ... Resume Quelque citations a partir du texte intégral exemple: Google Scholar provides a simple across a wide variety of disciplines and sources: articles, theses, ... Resume Quelque citations a partir du texte intégral exemple: Google Scholar provides a simple across a wide variety of disciplines and sources: articles, theses, ... Resume Quelque citations a partir du texte intégral exemple: Google Scholar provides a simple across a wide variety of disciplines and sources: articles, theses, ...  </p>
           </div>
         </div>
        <Footer/>
        </div>
    );
}
 
export default Article;