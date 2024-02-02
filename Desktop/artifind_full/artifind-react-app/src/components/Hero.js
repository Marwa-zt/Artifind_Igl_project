import React,{useState} from "react";
import bg from '../images/bg.jpg';
import Signup from "./Signup";
import {ReactTyped} from "react-typed";
import Navbar from "./Navbar";
import Footer from "./Footer";
import Aprop from "./Apropos";

const Hero = () => {
    const [signup, setSignup] = useState(false)
    const handlesign = () => {
      setSignup(!signup)
    }
    return ( 
        <div>
            <Navbar/>
            {signup && <Signup/>}
        <div className='w-full h-screen text-white' >
            <img className="top-0 left-0 w-full h-full object-cover"
                src={bg}
                alt="bg"
            />
            <div className="bg-black/70 absolute top-0 left-0 w-full h-screen"/>
        
            <div className=" absolute top-0 h-full w-full flex flex-col justify-center ">
                   
                    <div className="text-center">
                        <div className='py-24'></div>
                        <h1 className="md:text-7xl sm:text-6xl text-4xl font-bold md:py-4">Explore et apprends</h1>
                        
                        <div class="relative flex justify-center items-center py-4">
                                <div class=' absolute h-4 w-1/2 justify-center bg-[#24A393]/40'></div>
                                <p className="absolute md:text-3xl sm:text-xl text-xs">Les articles scientifiques les plus populaires</p>
                                
                        </div>
                       <ReactTyped className='text-[#24A393] font-thin md:text-2xl sm:text-xl text-xs pl-2 py-3' strings={['Entre vos mains!']} typeSpeed={120} backSpeed={140} loop></ReactTyped>
                            
                            <div className="py-20">
                                <p className='md:text-xl text-sx'>Inscrivez-vous maintenant!</p>
                                <button onClick={handlesign} className="bg-[#24A393] w-[200px] rounded-3xl font-bold my-3 mx-auto py-2 ">S’inscrire</button>
                              
                            </div>
                    </div>
        
            </div>
        </div>
        <Aprop/>
        <Footer/>
     </div>
     );
}
 
export default Hero;