from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from models import  Moderator
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from dotenv import dotenv_values
from typing import List
from upload import ArticleBase
from models import ArticleNonVerifie, Article




router = APIRouter(
    prefix='/moderator',
    tags=['moderator']
)

SECRET_KEY = '4567hj876yh99ik442gghn88ad098ujk12adf45avge7789hj90kbdd34dcg12hte567sw789'  #for JWT token encoding
ALGORITHM = 'HS256'
config_credential = dotenv_values(".env")
VERIFICATION_TOKEN_EXPIRATION = timedelta(hours=24)

class FormData(BaseModel):
    email: str
    password: str
  

# Include the 'id' field in CreateUserRequest
class CreateUserRequest(BaseModel):
    nom: str
    prenom: str
    email: EmailStr
    hashed_password: str




create_user_request = CreateUserRequest(
    email="john@example.com",
    nom="John",
    prenom="Doe",
    hashed_password="password123",

)


class Token(BaseModel):
    access_token:str
    token_type: str





#------------------------------------------------------------------------------------------------#
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]



router = APIRouter()

@router.get("/admin/get_moderators")
async def get_moderators(db: Session = Depends(get_db)):
    moderators = db.query(Moderator).all()
    
    # Convert Moderator instances to dictionaries
    moderators_dict_list = [
        {
            "id": moderator.id,
            "email": moderator.email,
            "nom": moderator.nom,
            "prenom": moderator.prenom,
            "hashed_password": moderator.hashed_password,
            "is_verified": moderator.is_verified,
            "verification_token": moderator.verification_token,
        }
        for moderator in moderators
    ]
    
    return moderators_dict_list
#-------------------------------------------------------------------------------------------------------#

@router.post("/admin/create_user", status_code=status.HTTP_201_CREATED)
async def create_user(
    db: db_dependency,
    create_user_request: CreateUserRequest,
):
    
    # Check if the email already exists
    existing_user = db.query(Moderator).filter(Moderator.email == create_user_request.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    create_user_model = Moderator(
        email=create_user_request.email,
        nom=create_user_request.nom,
        prenom=create_user_request.prenom,
        hashed_password=create_user_request.hashed_password,
    )

    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)

    return create_user_model



#-------------------------------------------------------------------------------------------------------------#
#endpoint de suppression d'utilisateur
@router.delete("/delete-user/{email}", response_model=dict)
async def delete_user(email: str, db: Session = Depends(get_db)):

    # Find the user by email
    user_to_delete = db.query(Moderator).filter(Moderator.email == email).first()

    # Check if the user exists
    if not user_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    # Delete the user
    db.delete(user_to_delete)
    db.commit()

    return {"message": "Moderator deleted successfully"}





@router.get("/get-user/{email}", response_model=dict)
async def get_user(email: str, db: Session = Depends(get_db)):

    # Find the user by email
    user = db.query(Moderator).filter(Moderator.email == email).first()

    # Check if the user exists
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    # Convert the user instance to a dictionary
    user_dict = {
        "id": user.id,
        "email": user.email,
        "nom": user.nom,
        "prenom": user.prenom,
        "hashed_password": user.hashed_password,
        "is_verified": user.is_verified,
        "verification_token": user.verification_token,
    }

    return user_dict


#====================================================================================================================#
#endpoint de modiification d'un moderateur

@router.put("/modify-user/{email}", response_model=dict)
async def modify_user(email: str, new_user_data: CreateUserRequest, db: Session = Depends(get_db)):

    # Find the user by email
    user_to_modify = db.query(Moderator).filter(Moderator.email == email).first()

    # Check if the user exists
    if not user_to_modify:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    # Check if the email in the request is provided and different from the current email
    if new_user_data.email and new_user_data.email != user_to_modify.email:
        # Check if the new email already exists
        existing_user = db.query(Moderator).filter(Moderator.email == new_user_data.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

    # Update user information if provided in the request
    if new_user_data.email:
        user_to_modify.email = new_user_data.email
    if new_user_data.nom:
        user_to_modify.nom = new_user_data.nom
    if new_user_data.prenom:
        user_to_modify.prenom = new_user_data.prenom
    
    # Check if a new password is provided, then update hashed password
    if new_user_data.hashed_password is not None:
       user_to_modify.hashed_password = new_user_data.hashed_password


    # Commit changes to the database
    db.commit()

    return {"message": "User information modified successfully"}

#---------------------------------------------------------------------------------------------------------------------#
#endpoint de modiification d'un article
@router.put("/modify-article/{id}", response_model=dict)
async def modify_article(id: str, new_article_data: ArticleBase, db: Session = Depends(get_db)):
    # Find the article by ...
    article_to_modify = db.query(ArticleNonVerifie).filter(ArticleNonVerifie.id == id).first()

    # Check if the article exists
    if not article_to_modify:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Article not found')
    article_to_modify = {
        "titre": article_to_modify.titre,
        "resume": article_to_modify.resume,
        "date": article_to_modify.date,
        "text_integral": article_to_modify.text_integral,
        "auteur": article_to_modify.auteur,
        "refs": article_to_modify.refs,
        "institutions": article_to_modify.institutions,
        "motscles": article_to_modify.motscles,
        "url": article_to_modify.url
    }
    # Update user information if provided in the request
    if new_article_data.titre:
        article_to_modify.titre = new_article_data.titre
    if new_article_data.resume:
        article_to_modify.resume = new_article_data.resume
    if new_article_data.date:
        article_to_modify.date = new_article_data.date
    if new_article_data.text_integral:
        article_to_modify.text_integral = new_article_data.text_integral
    if new_article_data.auteur:
        article_to_modify.auteur = new_article_data.auteur
    if new_article_data.refs:
        article_to_modify.refs = new_article_data.refs
    if new_article_data.institutions:
        article_to_modify.institutions = new_article_data.institutions
    if new_article_data.motscles:
        article_to_modify.motscles = new_article_data.motscles
    if new_article_data.url:
        article_to_modify.url = new_article_data.url
    # Commit changes to the database

    db.commit()

    return {"message": "Article information modified successfully"}




