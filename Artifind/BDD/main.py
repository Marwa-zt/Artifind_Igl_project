from fastapi import FastAPI,HTTPException,Depends,status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from datetime import datetime

app= FastAPI()
models.Base.metadata.create_all(bind=engine)
#----baseClasses------------------------------------------------------------
class AdminBase(BaseModel):
    nom:str
    prenom:str
    email:str
    motpasse:str

class AuteurBase(BaseModel):
    nom:str
    prenom:str

class ArticleBase(BaseModel):
    titre:str
    resume:str
    date:datetime
    #auteurs:str
    #institutions:str
    text_integral:str
    #url_pdf:str
    #references:str
class UrlsBase(BaseModel):
    url:str

class ReferencesBase(BaseModel):
    nom:str

class InstitutionsBase(BaseModel):
    nom:str

class MotsClesBase(BaseModel):
    mot:str



#----prepare our database-----------------------------------------------------
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]

#                    __________________________________
#                    |post/ get/ put/ delete  methodes|
#
#------------------------------articles----------------------------------------------------------------
@app.get("/article/{article_id}",status_code=status.HTTP_200_OK)
async def read_article(article_id:int,db:db_dependency):
    article=db.query(models.Article).filter(models.Article.id==article_id).first()
    if article is None :
        raise HTTPException(status_code=404 , detail="article not found")
    return article

@app.post("/article/",status_code=status.HTTP_201_CREATED)
async def add_article(article:ArticleBase,db:db_dependency):
    db_article=models.Article(**article.model_dump())
    db.add( db_article)
    db.commit()

@app.delete("/articles/{article_id}",status_code=status.HTTP_200_OK)
async def delete_article(article_id:int,db:db_dependency):
    db_article=db.query(models.Article).filter(models.Article.id==article_id).first()
    if db_article is None:
        raise  HTTPException(status_code=404,detail="Admin not found")
    db.delete(db_article)
    db.commit()
#------------------------------urls----------------------------------------
@app.get("/urls/{urls_id}",status_code=status.HTTP_200_OK)
async def read_urls(urls_id:int,db:db_dependency):
    urls=db.query(models.Urls).filter(models.Urls.id==urls_id).first()
    if urls is None :
        raise HTTPException(status_code=404 , detail="urls not found")
    return urls

@app.post("/urls/",status_code=status.HTTP_201_CREATED)
async def add_urls(urls:UrlsBase,db:db_dependency):
    db_urls=models.Urls(**urls.model_dump())
    db.add(db_urls)
    db.commit()

#------------------------------auteur----------------------------------------
@app.get("/auteur/{auteur_id}",status_code=status.HTTP_200_OK)
async def read_auteur(auteur_id:int,db:db_dependency):
    auteur=db.query(models.Auteur).filter(models.Auteur.id==auteur_id).first()
    if auteur is None :
        raise HTTPException(status_code=404 , detail="Auteur not found")
    return auteur

@app.post("/auteur/",status_code=status.HTTP_201_CREATED)
async def add_auteur(auteur:AuteurBase,db:db_dependency):
    db_auteur=models.Auteur(**auteur.model_dump())
    db.add(db_auteur)
    db.commit()

#------------------------------references----------------------------------------
@app.get("/references/{references_id}",status_code=status.HTTP_200_OK)
async def read_references(references_id:int,db:db_dependency):
    references=db.query(models.References).filter(models.References.id==references_id).first()
    if references is None :
        raise HTTPException(status_code=404 , detail="references not found")
    return references

@app.post("/references/",status_code=status.HTTP_201_CREATED)
async def add_references(references:ReferencesBase,db:db_dependency):
    db_references=models.References(**references.model_dump())
    db.add(db_references)
    db.commit()

#------------------------------institutions----------------------------------------------------------------
@app.get("/institutions/{institutions_id}",status_code=status.HTTP_200_OK)
async def read_institutions(institutions_id:int,db:db_dependency):
    institutions=db.query(models.Institutions).filter(models.Institutions.id==institutions_id).first()
    if institutions is None :
        raise HTTPException(status_code=404 , detail="institutions not found")
    return institutions

@app.post("/institutions/",status_code=status.HTTP_201_CREATED)
async def add_institutions(institutions:InstitutionsBase,db:db_dependency):
    db_institutions=models.Institutions(**institutions.model_dump())
    db.add( db_institutions)
    db.commit()

#------------------------------motscles----------------------------------------------------------------
@app.get("/motscles/{motscles_id}",status_code=status.HTTP_200_OK)
async def read_motscles(motscles_id:int,db:db_dependency):
    motscles=db.query(models.MotsCles).filter(models.MotsCles.id==motscles_id).first()
    if motscles is None :
        raise HTTPException(status_code=404 , detail="motscles not found")
    return motscles

@app.post("/motscles/",status_code=status.HTTP_201_CREATED)
async def add_motscles(motscles:MotsClesBase,db:db_dependency):
    db_motscles=models.MotsCles(**motscles.model_dump())
    db.add( db_motscles)
    db.commit()
#-----------------------------------------------------------------------------

















'''
#------------------------------admin----------------------------------------------------"""
@app.post("/admin/",status_code=status.HTTP_201_CREATED)
async def add_admin(admin:AdminBase,db:db_dependency):
    db_admin=models.Admin(**admin.model_dump())
    # ^ likely returns a dictionary with the admin data,
    # and ** unpacks this dictionary to match it with the Admin model's attributes.
    db.add( db_admin)
    db.commit()
@app.get("/admin/{admin_id}",status_code=status.HTTP_200_OK)
async def read_admin(admin_id:int,db:db_dependency):
    admin=db.query(models.Admin).filter(models.Admin.id==admin_id).first()
    if admin is None :
        raise HTTPException(status_code=404,detail="Admin not found")
    return admin
'''
