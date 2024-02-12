from sqlalchemy import Column, String, Boolean, Integer


-- create_users.sql

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(50) UNIQUE,
    nom VARCHAR(50),
    prenom VARCHAR(50),
    hashed_password VARCHAR(255),
    is_verified BOOLEAN DEFAULT FALSE,
    verification_token VARCHAR(50)
);
CREATE TABLE admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(50) UNIQUE,
    nom VARCHAR(50),
    prenom VARCHAR(50),
    hashed_password VARCHAR(255),
    is_verified BOOLEAN DEFAULT FALSE,
    verification_token VARCHAR(50)
);
CREATE TABLE moderator (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(50) UNIQUE,
    nom VARCHAR(50),
    prenom VARCHAR(50),
    hashed_password VARCHAR(255),
    is_verified BOOLEAN DEFAULT FALSE,
    verification_token VARCHAR(50)
);


--verifier si l'utilisateur existe 
SELECT * FROM users
WHERE email = 'user@example.com' AND hashed_password ='xxxxx';


-- delete moderator
DELETE FROM moderator WHERE email = 'user@example.com';

--create new user 
INSERT INTO users (email, nom, prenom, hashed_password, is_verified, verification_token)
VALUES ('user@example.com', 'John', 'Doe', 'hashed_password_value', 0, 'verification_token_value');


--create new moderator 
INSERT INTO moderator (email, nom, prenom, hashed_password, is_verified, verification_token)
VALUES ('user@example.com', 'nom', 'prenom', 'hashed_password_value', 0, 'verification_token_value');

--modify info
UPDATE users
SET nom = 'NewName', prenom = 'NewFirstName', hashed_password = 'new_hashed_password'
WHERE email = 'user@example.com';
