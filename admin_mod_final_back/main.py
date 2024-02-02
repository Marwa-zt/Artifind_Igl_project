from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import auth
import moderator
from auth import get_current_user
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
import logging
from moderator import router

# ... rest of your code


# Add this at the beginning of your script
logging.basicConfig(level=logging.DEBUG)
app = FastAPI()
app.include_router(auth.router)
app.include_router(moderator.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


models.Base.metadata.create_all(bind=engine)

# Add SessionMiddleware to the app
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

from fastapi import Depends
# ... (other imports)

@app.get("/", status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')

    # Check if the user is an admin and redirect to another page
    if user['role'] == 'admin':
        # Redirect logic for admin
        return {"message": "Welcome Admin! Redirect to admin page."}

    return {"User": user}

