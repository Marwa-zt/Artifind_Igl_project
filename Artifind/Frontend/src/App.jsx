// App.jsx
import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import NavBar from "./components/common/NavBar";
import Upload from "./components/upload/upload";
import Moderators from "./components/moderators/Moderators";
import Articles from "./components/articles/Articles";

const App = () => {
  return (
    <Router>
      <div className="app">
        <NavBar />

        <Routes>
          <Route path="/gestion-des-moderateurs" element={<Moderators/>} />
          <Route path="/importation-des-articles" element={<Upload/>} />
          <Route path="/liste-des-articles" element={<Articles/>}/>
        </Routes>
      </div>
    </Router>
  );
};

export default App;
