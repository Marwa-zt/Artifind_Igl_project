// Articles.jsx
import React, { useState } from "react";
import searchIcon from "../../assets/searchIcon.png";
import ArticlesList from "./ArticlesList";
import "./articles.css";

const Articles = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [articles, setArticles] = useState([
    {
      id: 1,
      titre: "Title 1",
      auteur: "Author 1",
      institution: "Institution 1",
      reference: "Reference 1",
      date: "2022-01-01",
      verified: true, // Ajoutez une propriété 'verified' à vos articles
    },
    {
      id: 2,
      titre: "Title 2",
      auteur: "Author 2",
      institution: "Institution 2",
      reference: "Reference 2",
      date: "2022-02-01",
      verified: false, // Ajoutez une propriété 'verified' à vos articles
    },
    // Ajoutez d'autres articles au besoin
  ]);


  const filteredArticles = articles.filter(
    (article) =>
      article.titre.toLowerCase().includes(searchQuery.toLowerCase()) ||
      article.auteur.toLowerCase().includes(searchQuery.toLowerCase()) ||
      article.institution.toLowerCase().includes(searchQuery.toLowerCase()) ||
      article.reference.toLowerCase().includes(searchQuery.toLowerCase()) ||
      String(article.id).includes(searchQuery)
  );

  return (
    <>
      <div className="articles-container">
        <div className="centered-text">
          <h1>Liste des articles</h1>
        </div>
        <div className="article-info">
          <div className="search-bar">
            <img src={searchIcon} alt="Search Icon" />
            <input
              type="text"
              placeholder="Rechercher un article"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>

          <div className="article-count">
            <div className="rectangle-article">
              <p>{filteredArticles.length} articles</p>
            </div>
          </div>
        </div>
      </div>

      <ArticlesList articles={filteredArticles} setArticles={setArticles} />
    </>
  );
};

export default Articles;
