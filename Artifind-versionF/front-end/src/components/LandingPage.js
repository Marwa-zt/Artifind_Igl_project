import React, { useState } from "react";
import bg from '../images/bg.jpg';
import { FaSearch } from "react-icons/fa";
import NavMenu from "./NavMenu";
import { ReactTyped } from "react-typed";
import { useNavigate } from "react-router-dom";

const LandingPage = ({value}) => {
    const nav = useNavigate();

    const [motcle, setMotcle] = useState('');

    const handleChange = (e) => {
        setMotcle(e.target.value); 
    }
    const [aut, setAut] = useState({
        nom: 'Aut',
        prenom: 'prAut'
    });
    const [Formarticle, setFormarticle] = useState([{
        titre: 'HELLO WORLD 01',
        resume: 'bla bla bla bla 01',
        text_integral: 'txt txt txt txt 01',
        date: '20/02/2024',
        auteur: aut,
        refs: 'ref ref ref ref 01',
        institutions: '01',
        motscles: 'motcle motcle 01',
        url: 'url url 01'
    },
    {
        titre: 'HELLO WORLD 02',
        resume: 'bla bla bla bla 02',
        text_integral: 'txt txt txt txt 02',
        date: '20/02/2024',
        auteur: aut,
        refs: 'ref ref ref ref 02',
        institutions: '02',
        motscles: 'motcle motcle 02',
        url: 'url url 02'
    }
    ]);
    
    const handleSubm = async (e) => {

        e.preventDefault();
        try {
            const response = await fetch(`http://127.0.0.1:8000/elastic/search/${motcle}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                const result = await response.json();
                console.log(result);
                nav(`/Articles?Formarticle=${encodeURIComponent(JSON.stringify(result))}`);
                // Handle successful signup, maybe redirect the user to another page
            } else {
                // Handle error response from the server
                console.error('search failed');
                alert('erreur dans la récuperation des articles depuis Elasticsearch');
            }
        } catch (error) {
            console.error('erreur dans la récuperation des articles depuis Elasticsearch:', error);
        }
    }


    return (
        <div>
            <NavMenu value={value} />
            <div className='w-full h-screen text-white'>
                <img className="top-0 left-0 w-full h-full object-cover" src={bg} alt="bg" />
                <div className="bg-black/70 absolute top-0 left-0 w-full h-screen" />

                <div className="absolute top-0 h-full w-full flex flex-col justify-center">
                    <div className="text-center">
                        <div className='py-24'></div>
                        <h1 className="md:text-7xl sm:text-6xl text-4xl font-bold md:py-4">Explore et apprends</h1>

                        <div className="relative flex justify-center items-center py-4">
                            <div className='absolute h-4 w-1/2 justify-center bg-[#24A393]/40'></div>
                            <p className="absolute md:text-3xl sm:text-xl text-xs">Les articles scientifiques les plus populaires</p>
                        </div>

                        <ReactTyped className='text-[#24A393] font-thin md:text-2xl sm:text-xl text-xs pl-2 py-3' strings={['Entre vos mains!']} typeSpeed={120} backSpeed={140} loop></ReactTyped>

                        <div className="py-20 flex justify-center text-black">
                            <form onSubmit={handleSubm} className="w-[50%] relative m-4" action="">
                                <div className="relative ">
                                    <input type="search" value={motcle} onChange={handleChange} placeholder="Recherche.." className="w-full p-3 rounded-full bg-white outline-none border border-[#D5DD18]" />
                                    <button type="submit" className="absolute right-1 top-1/2 -translate-y-1/2 p-3 bg-[#D5DD18] rounded-full">
                                        <FaSearch className="text-white" />
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default LandingPage;
