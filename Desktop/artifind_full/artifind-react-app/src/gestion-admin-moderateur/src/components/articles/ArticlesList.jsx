// ArticlesList.jsx
import React from "react";
import "./articlesList.css";
import ConfirmationModal from "../moderators/ConfirmationModal";
import modifyIcon from "../../assets/modifyIcon.png";

const ArticlesList = ({ articles }) => {
  // You may need to pass setArticles or modify your data management accordingly

  const handleModifier = (id) => {
    // Implement your modification logic here
    console.log(`Modifier article with id ${id}`);
  };

  const handleVerifier = (id) => {
    // Implement your verification logic here
    console.log(`Verifier article with id ${id}`);
  };

  return (
    <div className="articles-list">
      <div className="titles">
        <div>Titre</div>
        <div>Auteur</div>
        <div>Institution</div>
        <div>Reference</div>
        <div>Date</div>
        <div></div> {/* New column for actions */}
      </div>
      <div className="separator"></div>
      <div className="articles-container">
        {articles.map((article) => (
          <div key={article.id} className="article">
            <div>{article.titre}</div>
            <div>{article.auteur}</div>
            <div>{article.institution}</div>
            <div>{article.reference}</div>
            <div>{article.date}</div>
            <div className="buttons">
              {/* Add your "Modifier" and "Verifier" buttons here */}
              <button onClick={() => handleModifier(article.id)}>
                <img
                  src={modifyIcon}
                  alt="Modify Icon"
                  className="buttonIcon"
                />
                Modifier
              </button>
              <div
                className={`verifier-rectangle ${
                  article.verified
                    ? "verifier-rectangle-verified"
                    : "verifier-rectangle-not-verified"
                }`}
              >
                {article.verified ? "Verifié" : "Non Verifié"}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ArticlesList;
