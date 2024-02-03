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
  
# hachage de mot de pass
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

class CreateUserRequest(BaseModel):
    email: EmailStr
    nom: str
    prenom: str
    password: str


create_user_request = CreateUserRequest(
    email="user@example.com",
    nom="maria",
    prenom="bono",
    password="securepassword",

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



#-------------------------------------------------------------------------------------------------------#

 #permettre aux admin de creer un moderateur
@router.post("/admin/create_user", status_code=status.HTTP_201_CREATED)
async def create_admin_user(
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
        hashed_password=bcrypt_context.hash(create_user_request.password),
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



#====================================================================================================================#
#endpoint de modiification d'un moderateur
@router.put("/modify-user/{email}", response_model=dict)
async def modify_user(email: str, new_user_data: CreateUserRequest, db: Session = Depends(get_db)):


    # Find the user by email
    user_to_modify = db.query(Moderator).filter(Moderator.email == email).first()

    # Check if the user exists
    if not user_to_modify:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    # Update user information if provided in the request
    if new_user_data.email:
        user_to_modify.email = new_user_data.email
    if new_user_data.nom:
        user_to_modify.nom = new_user_data.nom
    if new_user_data.prenom:
        user_to_modify.prenom = new_user_data.prenom
    if new_user_data.password:
        user_to_modify.hashed_password = bcrypt_context.hash(new_user_data.password)
    

    # Commit changes to the database
    db.commit()

    return {"message": "User information modified successfully"}


#---------------------------------------------------------------------------------------------------------------------#
