import React from "react";
import lg from "../images/lg.svg";
const Footer = () => {
    return ( 
        <div className="w-full mt-24 bg-gray-900 text-gray-300 py-2 px-2 ">
           <div className="max-w-[1400px] mx-auto grid grid-cols-3 border-b-2 border-gray-400 py-8 px-4">
             <div>
                <img src={lg} alt="lg" />
             </div>
             <div>
                <h4 className="font-bold pt-2">A propos</h4>
                <ul>
                    <li className="py-1">website</li>
                    <li className="py-1">notre équipe</li>
                </ul>
             </div>
             <div>
                <h4 className="font-bold pt-2">Contact</h4>
                <ul>
                    <li className="py-1">Iglx@gmail.com</li>
                    <li className="py-1">+213 553 371 990</li>
                </ul>
             </div>
           </div>
        </div>
     );
}
 
export default Footer;