from ast import Dict, List
from fastapi import FastAPI,HTTPException,Depends,status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, List


app= FastAPI()
models.Base.metadata.create_all(bind=engine)
#----baseClasses------------------------------------------------------------
class ArticleNonVerifieBase(BaseModel):
    titre: str
    resume: str
    text_integral: str
    date: datetime
    auteur: List[Dict[str, str]]
    refs: List[str]
    institutions: List[str]
    motscles: List[str]
    url: str
    
class AuteurBase(BaseModel):
    nom:str
    prenom:str

class ArticleBase(BaseModel):
    titre: str
    resume: str
    text_integral: str
    date: datetime
    auteur: List[Dict[str, str]]
    refs: List[str]
    institutions: List[str]
    motscles: List[str]
    url: str

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
#-----------------------------article non verifie-----------------------------------------------------
@app.get("/articlenonverifie/{articlenonverifie_id}",status_code=status.HTTP_200_OK)
async def read_articlenonverifie(articlenonverifie_id:int,db:db_dependency):
    articlenonverifie=db.query(models.ArticleNonVerifie).filter(models.ArticleNonVerifie.id==articlenonverifie_id).first()
    if articlenonverifie is None :
        raise HTTPException(status_code=404 , detail="articlenonverifie not found")
    return articlenonverifie
'''
    '''
def save_articlenonverifie_to_database(articlenonverifie_data):
    db=SessionLocal()
    try:
        articlenonverifie = ArticleNonVerifieBase(
            titre=articlenonverifie_data['titre'],
            resume=articlenonverifie_data['resume'],
            date=datetime.now(),
            text_integral=articlenonverifie_data['text_integral']
        )
        for auteur_data in articlenonverifie_data['auteur']:
            auteur = AuteurBase(nom=auteur_data['nom'], prenom=auteur_data['prenom'])
            articlenonverifie.auteur.append(auteur)
        for reference_data in articlenonverifie_data.get('refs', []):
            reference = ReferencesBase(nom=reference_data)
            articlenonverifie.refs.append(reference)
        
        
        for institution_data in articlenonverifie_data.get('institutions', []):
            institution = InstitutionsBase(nom=institution_data)
            articlenonverifie.institutions.append(institution)
        
        for mot_data in articlenonverifie_data.get('motscles', []):
            mot = MotsClesBase(mot=mot_data)
            articlenonverifie.motscles.append(mot)

        if 'urls' in articlenonverifie_data:
            urls = UrlsBase(url=articlenonverifie_data['url'])
            articlenonverifie.url = urls
        
        db.add(articlenonverifie)
        
        db.commit()
        
        return {"message": "articlenonverifie added successfully"}
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

@app.post("/save_articlenonverifie/", status_code=status.HTTP_201_CREATED)
async def add_articlenonverifie_to_database(articlenonverifie_data: dict):
    try:
        save_articlenonverifie_to_database(articlenonverifie_data)
        return {"message": "articlenonverifie added successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@app.delete("/articlenonverifies/{articlenonverifie_id}",status_code=status.HTTP_200_OK)
async def delete_articlenonverifie(articlenonverifie_id:int,db:db_dependency):
    db_articlenonverifie=db.query(models.articlenonverifie).filter(models.articlenonverifie.id==articlenonverifie_id).first()
    if db_articlenonverifie is None:
        raise  HTTPException(status_code=404,detail="articlenonverifie not found")
    db.delete(db_articlenonverifie)
    db.commit()
#------------------------------articles----------------------------------------------------------------

@app.get("/article/{article_id}",status_code=status.HTTP_200_OK)
async def read_article(article_id:int,db:db_dependency):
    article=db.query(models.Article).filter(models.Article.id==article_id).first()
    if article is None :
        raise HTTPException(status_code=404 , detail="article not found")
    return article
'''
@app.post("/article/",status_code=status.HTTP_201_CREATED)
async def add_article(article:ArticleBase,db:db_dependency):
    db_article=models.Article(**article.model_dump())
    db.add( db_article)
    db.commit()
'''
def save_article_to_database(article_data):
    db=SessionLocal()
    try:
        article = ArticleBase(
            titre=article_data['titre'],
            resume=article_data['resume'],
            date=datetime.now(),
            text_integral=article_data['text_integral']
        )
        for auteur_data in article_data['auteur']:
            auteur = AuteurBase(nom=auteur_data['nom'], prenom=auteur_data['prenom'])
            article.auteur.append(auteur)
        for reference_data in article_data.get('refs', []):
            reference = ReferencesBase(nom=reference_data)
            article.refs.append(reference)
        
        
        for institution_data in article_data.get('institutions', []):
            institution = InstitutionsBase(nom=institution_data)
            article.institutions.append(institution)
        
        for mot_data in article_data.get('motscles', []):
            mot = MotsClesBase(mot=mot_data)
            article.motscles.append(mot)

        if 'urls' in article_data:
            urls = UrlsBase(url=article_data['url'])
            article.url = urls
        
        db.add(article)
        
        db.commit()
        
        return {"message": "Article added successfully"}
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

@app.post("/save_article/", status_code=status.HTTP_201_CREATED)
async def add_article_to_database(article_data: dict):
    try:
        # Call the function to save the article to the database
        save_article_to_database(article_data)
        return {"message": "Article added successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

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
async def read_references(refs_id:int,db:db_dependency):
    refs=db.query(models.Refs).filter(models.Refs.id==refs_id).first()
    if refs is None :
        raise HTTPException(status_code=404 , detail="references not found")
    return refs

@app.post("/refrences/",status_code=status.HTTP_201_CREATED)
async def add_references(refs:ReferencesBase,db:db_dependency):
    db_references=models.References(**refs.model_dump())
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
