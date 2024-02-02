import React from "react";
import lg from "../images/Artifindlogo.svg";
import ass1 from "../images/ass1.png";



const Aprop = () => {
     return ( 
       
        <div className=" text-black">
                <img className="object-cover" src={ass1} alt="ass1" />
                <div class="relative flex justify-center items-center py-20">
                    <div class=' absolute h-4 w-80 justify-center bg-[#24A393]/40'></div>
                    <h1 className="absolute md:text-3xl sm:text-xl text-xl font-bold">À propos d'Artifind:</h1>
                </div>
                <div className="justify-center items-center max-w-[1400px] m-auto grid lg:grid-cols-2 px-16 gap-4" >
                    <p className="md:text-3xl sm:text-xl text-xl ">  Bienvenue sur Artifind, votre moteur de recherche dédié aux articles scientifiques. Notre plateforme innovante a été conçue pour simplifier l'accès à la connaissance scientifique, offrant une expérience de recherche fluide et efficace.</p>
                    <img className="px-10 lg:px-44 " src={lg} alt="lg" />
                </div>

                <div className="md:text-3xl sm:text-xl text-xl px-16 py-9">
                    <div class="relative flex justify-center items-center py-20">
                        <div class=' absolute h-4 w-80 justify-center bg-[#D5DD18]/90'></div>
                        <h2 className="absolute md:text-3xl sm:text-xl text-xl font-bold">Ce que nous offrons :</h2>
                    </div>
                    <h3 className="md:text-3xl sm:text-xl text-xl font-bold px-6 py-4 ">Recherche ciblée : </h3>
                    <p className="py-4 text-gray-700"> Artifind se spécialise dans la recherche d'articles scientifiques, permettant aux utilisateurs de trouver rapidement des informations précises dans leur domaine d'étude.</p>
                    <h3 className="md:text-3xl sm:text-xl text-xl font-bold px-6 py-4">Filtrage intelligent : </h3>
                    <p className="py-4 text-gray-700">Grâce à des fonctionnalités de filtrage avancées, Artifind vous aide à affiner vos résultats de recherche en fonction de critères spécifiques tels que la date de publication, l'auteur et la revue scientifique.</p>
                    <h3 className="md:text-3xl sm:text-xl text-xl font-bold px-6 py-4">Interface conviviale :</h3> 
                    <p className="py-4 text-gray-700"> Naviguez facilement à travers notre interface conviviale, conçue pour rendre la recherche d'articles scientifiques aussi simple que possible.</p>
                </div>
                <div class="relative flex justify-center items-center py-20">
                    <div class=' absolute h-4 w-80 justify-center bg-[#24A393]/40'></div>
                    <h1 className="absolute md:text-3xl sm:text-xl text-xl font-bold">Notre mission :</h1>
                </div>
                   <p className="md:text-3xl sm:text-xl text-xl px-16 py-9">Chez Artifind, notre mission est de faciliter la découverte et l'accès à la connaissance scientifique. Nous croyons que la recherche devrait être accessible à tous, et c'est pourquoi nous mettons tout en œuvre pour simplifier le processus de recherche et rendre les informations scientifiques compréhensibles pour un public diversifié.</p>
            
         </div>
     );
}
 
export default Aprop;