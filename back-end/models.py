#here we create the tables we need in our database
from msilib import Table
from click import DateTime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, DateTime
from database import Base
from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from uuid import UUID, uuid4


Base = declarative_base()

class BaseUser(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(length=50), unique=True, index=True)
    nom = Column(String(length=50))
    prenom = Column(String(length=50))
    hashed_password = Column(String(length=255))
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String(length=50))

class Admin(BaseUser):
    __tablename__ = "admins"

class users(BaseUser):
    __tablename__ = "Users"

class Moderator(BaseUser):
    __tablename__ = "moderators"

#____________________associations between tables in database____________________________________________________________________________________
article_auteur_association = Table(
    'article_auteur_association',
    Base.metadata,
    Column('article_id', Integer, ForeignKey('article.id')),
    Column('auteur_id', Integer, ForeignKey('auteur.id'))
)
article_references_association = Table(
    'article_references_association',
    Base.metadata,
    Column('article_id', Integer, ForeignKey('article.id')),
    Column('refs_id', Integer, ForeignKey('refs.id'))
)
article_institutions_association = Table(
    'article_institutions_association',
    Base.metadata,
    Column('article_id', Integer, ForeignKey('article.id')),
    Column('institutions_id', Integer, ForeignKey('institutions.id'))
)
article_motscles_association = Table(
    'article_motscles_association',
    Base.metadata,
    Column('article_id', Integer, ForeignKey('article.id')),
    Column('motscles_id', Integer, ForeignKey('motscles.id'))
)
#____________________associations between tables in database(article non verifie)_____________________________________________________________
articlenonverifie_auteur_association = Table(
    'articlenonverifie_auteur_association',
    Base.metadata,
    Column('articleNonVerifie_id', Integer, ForeignKey('articleNonVerifie.id')),
    Column('auteur_id', Integer, ForeignKey('auteur.id'))
)
articlenonverifie_references_association = Table(
    'articlenonverifie_references_association',
    Base.metadata,
    Column('articleNonVerifie_id', Integer, ForeignKey('articleNonVerifie.id')),
    Column('refs_id', Integer, ForeignKey('refs.id'))
)
articlenonverifie_institutions_association = Table(
    'articlenonverifie_institutions_association',
    Base.metadata,
    Column('articleNonVerifie_id', Integer, ForeignKey('articleNonVerifie.id')),
    Column('institutions_id', Integer, ForeignKey('institutions.id'))
)
articlenonverifie_motscles_association = Table(
    'articlenonverifie_motscles_association',
    Base.metadata,
    Column('articleNonVerifie_id', Integer, ForeignKey('articleNonVerifie.id')),
    Column('motscles_id', Integer, ForeignKey('motscles.id'))
)
#____________________________________________________________________________________________________________________
class Admin(Base):
    __tablename__ = "admin"
    id= Column(Integer, primary_key=True,index=True)
    nom= Column(String(16))
    prenom= Column(String(16))
    email=Column(String(200),unique=True)
    motpasse = Column("password", String(32))

class Auteur(Base):
    __tablename__ = "auteur"
    id= Column(Integer, primary_key=True,index=True)
    nom= Column(String(16))
    prenom= Column(String(16))
    article_id=Column(Integer, ForeignKey('article.id'))
    article = relationship("Article", secondary=article_auteur_association, back_populates="auteur")
    articlenonverifie_id=Column(Integer,ForeignKey('articleNonVerifie.id'))
    articlenonverifie = relationship("articleNonVerifie", secondary=article_institutions_association, back_populates="auteur")
    

class ArticleNonVerifie(Base):
    __tablename__ = "articleNonVerifie"
    id=Column(Integer, primary_key=True,index=True)
    titre=Column(String(200))
    resume=Column(String(10000))
    date=Column(DateTime)
    #auteur_id = Column(Integer, ForeignKey('auteur.id'))
    #institutions_id=Column(Integer, ForeignKey('institutions.id'))
    text_integral=Column(String(2000))
    #url_id = Column(Integer, ForeignKey('url.id'))
    #refs=Column(Integer, ForeignKey('refs.id'))
    auteurs = relationship("Auteur", secondary=article_auteur_association, back_populates="articleNonVerifie")
    references = relationship("References", secondary=article_references_association, back_populates="articleNonVerifie")
    institutions = relationship("Institutions", secondary=article_institutions_association, back_populates="articleNonVerifie")
    motscles = relationship("MotsCles", secondary=article_motscles_association, back_populates="articleNonVerifie")
    url = relationship("url", uselist=False, back_populates="articleNonVerifie")

class Article(Base):
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True)
    titre = Column(String(200))
    resume = Column(String(1000))
    date = Column(DateTime)
    #auteur_id = Column(Integer, ForeignKey('auteur.id'))
    #institutions_id=Column(Integer, ForeignKey('institutions.id'))
    text_integral=Column(String(20000))
    #url_id = Column(Integer, ForeignKey('url.id'))
    #refs_id=Column(Integer, ForeignKey('refs.id'))
    auteur = relationship("Auteur", secondary=article_auteur_association, back_populates="article")
    refs = relationship("References", secondary=article_references_association, back_populates="article")
    institutions = relationship("Institutions", secondary=article_institutions_association, back_populates="article")
    motscles = relationship("MotsCles", secondary=article_motscles_association, back_populates="article")
    url = relationship("Urls", uselist=False, back_populates="article")
    '''def __init__(self, **kwargs):
        self.auteur.update(kwargs)'''

class Urls(Base):
    __tablename__ = 'url'
    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey('article.id'))
    article = relationship("Article", uselist=False, back_populates="url") 
    articlenonverifie_id = Column(Integer, ForeignKey('articleNonVerifie.id'))
    articlenonverifie = relationship("ArticleNonVerifie", uselist=False, back_populates="url")   

class Institutions(Base):
    __tablename__="institutions"
    id=Column(Integer,primary_key=True,index=True)
    nom=Column(String(200))
    article_id=Column(Integer,ForeignKey('article.id'))
    article = relationship("Article", secondary=article_institutions_association, back_populates="institutions")
    articlenonverifie_id=Column(Integer,ForeignKey('articlenonverifie.id'))
    articlenonverifie = relationship("ArticleNonVerifie", secondary=article_institutions_association, back_populates="institutions")
    
class MotsCles(Base):
    __tablename__="motscles"
    id=Column(Integer,primary_key=True,index=True)
    mot=Column(String(50))
    article_id=Column(Integer,ForeignKey('article.id'))
    article = relationship("Article", secondary=article_motscles_association, back_populates="motscles")
    articlenonverifie_id=Column(Integer,ForeignKey('articlenonverifie.id'))
    articlenonverifie = relationship("ArticleNonVerifie", secondary=article_motscles_association, back_populates="motscles")
    


class References(Base):
    __tablename__="refs"
    id=Column(Integer,primary_key=True,index=True)
    nom=Column(String(200))
    article_id=Column(Integer,ForeignKey('article.id'))
    article = relationship("Article", secondary=article_references_association, back_populates="refs")
    articlenonverifie_id=Column(Integer,ForeignKey('articlenonverifie.id'))
    articlenonverifie = relationship("ArticleNonVerifie", secondary=article_references_association, back_populates="refs")

class Moderateur(Base):
    __tablename__ = "moderateur"
    id= Column(Integer, primary_key=True,index=True)
    nom= Column(String(16))
    prenom= Column(String(16))
    email=Column(String(200),unique=True)
    motpasse = Column("password", String(32))