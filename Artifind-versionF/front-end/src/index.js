import React from 'react';
import ReactDOM from "react-dom/client";
import {
  createBrowserRouter,
  RouterProvider,
  Route,
  Link,
} from "react-router-dom";
import './index.css';
import App from './App';
import  Navbar from './components/Navbar';
import Aprop from './components/Apropos';
import Footer from './components/Footer';
import Login2 from './components/Login';
import Signup from './components/Signup';
import LandingPage from './components/LandingPage';
import Articles from './components/Articles';
import Article from './components/ArticleDetail';
import Favories from './components/Favories';

const router = createBrowserRouter([
  { path: "/",element: <App/>,},
  { path: "Navbar", element: <Navbar />,},
  {path: "Apropos", element: <Aprop />,},
  {path: "Footer", element: <Footer />,},
  {path: "Lognin", element: <Login2 />,},
  {path: "Singup", element: <Signup />,},
  {path: "Landingpage", element: <LandingPage />,},
  {path: "Articles", element: <Articles />,},
  {path: "Article", element: <Article />,},  
  {path: "Fav", element: <Favories />,}, 
  

]);
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <RouterProvider router={router} />   
  );

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
