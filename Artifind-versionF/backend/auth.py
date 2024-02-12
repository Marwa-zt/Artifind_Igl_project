from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from models import Admin, Moderator, users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import secrets
from fastapi.responses import HTMLResponse
from dotenv import dotenv_values
from fastapi.templating import Jinja2Templates
from gen_email import send_emaill
from fastapi.responses import HTMLResponse,RedirectResponse 


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


SECRET_KEY = '4567hj876yh99ik442gghn88ad098ujk12adf45avge7789hj90kbdd34dcg12hte567sw789'  #for JWT token encoding
ALGORITHM = 'HS256'
config_credential = dotenv_values(".env")
VERIFICATION_TOKEN_EXPIRATION = timedelta(hours=24)

class UserCredentials(BaseModel):
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
    nom="John",
    prenom="Doe",
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



#---------------------------------------------------------------------------------------------------#
#endpoint FastAPI pour creer un user
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):

    # Check if the email already exists
    existing_user = db.query(users).filter(users.email == create_user_request.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    verification_token = secrets.token_urlsafe(16)

    create_user_model = users(
        email=create_user_request.email,
        nom=create_user_request.nom,
        prenom=create_user_request.prenom,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        verification_token=verification_token,
    )

    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    verification_link = f"https://example.com/verify?token={verification_token}"

    # Send email verification
    subject = "Account Creation Confirmation"
    recipients = [create_user_model.email]
    body = f"Hello {create_user_model.nom},\n\nYour account has been successfully created.\n\n"
    body += f"Please click the following link to verify your email address: {verification_link}\n\nThank you!"

    #await send_emaill(subject, recipients, body)

    return create_user_model
#----------------------------------------------------------------------------------------------------------#
#pour verifier l'email
templates = Jinja2Templates(directory="templates")
@router.post("/verification", response_class=HTMLResponse)
async def email_verification(request: Request, token: str):
    user = await verify_token(token)

    if user and not user.is_verified:
        user.is_verified = True
        await user.save()
        return templates.TemplateResponse("verificatiom.html",
                                         { "request": request,"username": user.nom})

    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token",
            headers={"WWW-Authenticatee": "Bearer"}
        )


async def verify_token(token: str):
    try:
        payload = jwt.decode(token,config_credential['SECRET'])
        user = await users.get(id = payload.get("id"))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token",
            headers={"WWW-Authenticatee": "Bearer"}
        )
    return user

#-----------------------------------------------------------------------------------------------------#
#authentification 
@router.post("/token", status_code=status.HTTP_200_OK)
async def login_for_access_token(
    form_data: UserCredentials ,
    db: Session = Depends(get_db)
):
    user = authenticate_user(form_data, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    role = user.role  
    user_id = user.id
    
    token = create_access_token(user.email, user_id, timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"}
       
        
    #return {"access_token": token, "token_type": "bearer"}

#------------------------------------------------------------------------------------------------------------#
def authenticate_user(credentials: UserCredentials, db: Session):
    user = db.query(users).filter(users.email == credentials.email).first()

    if user and bcrypt_context.verify(credentials.password, user.hashed_password):
        return user

    # Si ce n'est pas un utilisateur régulier, vérifiez s'il s'agit d'un administrateur
    admin = db.query(Admin).filter(Admin.email == credentials.email).first()

    if admin and bcrypt_context.verify(credentials.password, admin.hashed_password):
        return admin
    
    moderator = db.query(Moderator).filter(Moderator.email == credentials.email).first()

    if moderator and bcrypt_context.verify(credentials.password, moderator.hashed_password):
        return moderator
    '''
    moderator = db.query(Moderator).filter(Moderator.email == form_data.email).first()
    if moderator and bcrypt_context.verify(form_data.password, moderator.hashed_password):
        return moderator
        '''
   

    return None
#------------------------------------------------------------------------------------------------------#
def create_access_token(email: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': email, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


#--------------------------------------------------------------------------------------------------===#
#extraire les infos de l'user actuelle
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get('sub')
        print(email)
        user_id: int = payload.get('id')
        if email is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
        return {'email': email, 'id': user_id}
    except JWTError as e:
         print(f"JWT Error: {e}")
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
 #--------------------------------------------------------------------------------------------------   
@router.get("/users/me", response_model=dict)
async def get_current_user_info(
    current_user: dict = Depends(get_current_user)
):
    return current_user
