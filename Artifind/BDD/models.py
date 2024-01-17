from sqlalchemy import Boolean,Column,Integer,String,ForeignKey,Table,DateTime
from sqlalchemy.orm import relationship
from database import Base
from uuid import UUID, uuid4
#____________________associations____________________________________________________________________________________
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
    Column('references_id', Integer, ForeignKey('references.id'))
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
    articles = relationship("Article", secondary=article_auteur_association, back_populates="auteurs")
    
class Urls(Base):
    __tablename__ = "urls"
    id= Column(Integer, primary_key=True,index=True)
    url=Column( String(200))
    article_id = Column(Integer, ForeignKey('article.id'))
    article = relationship("Article", back_populates="url")

class Article(Base):
    __tablename__ = "article"
    id=Column(Integer, primary_key=True,index=True)
    titre=Column(String(200))
    resume=Column(String(10000))
    date=Column(DateTime)
    autheur_id = Column(Integer, ForeignKey('autheur.id'))
    institutions=Column(String(20000))
    text_integral=Column(String(200000))
    url_id = Column(Integer, ForeignKey('url.id'))
    references=Column(String(2000))
    auteurs = relationship("Auteur", secondary=article_auteur_association, back_populates="article")
    references = relationship("References", secondary=article_references_association, back_populates="article")
    institutions = relationship("Institutions", secondary=article_institutions_association, back_populates="article")
    motscles = relationship("MotsCles", secondary=article_motscles_association, back_populates="article")
    url = relationship("Urls", uselist=False, back_populates="article")

class Institutions(Base):
    __tablename__="insitutions"
    id=Column(Integer,primary_key=True,index=True)
    nom=Column(String(200))
    article_id=Column(Integer,ForeignKey('article.id'))
    articles = relationship("Article", secondary=article_institutions_association, back_populates="institutions")
    
class MotsCles(Base):
    __tablename__="insitutions"
    id=Column(Integer,primary_key=True,index=True)
    mot=Column(String(50))
    article_id=Column(Integer,ForeignKey('article.id'))
    articles = relationship("Article", secondary=article_motscles_association, back_populates="motscles")

class References(Base):
    __tablename__="references"
    id=Column(Integer,primary_key=True,index=True)
    nom=Column(String(200))
    article_id=Column(Integer,ForeignKey('article.id'))
    articles = relationship("Article", secondary=article_references_association, back_populates="references")

class Moderateur(Base):
    __tablename__ = "moderateur"
    id= Column(Integer, primary_key=True,index=True)
    nom= Column(String(16))
    prenom= Column(String(16))
    email=Column(String(200),unique=True)
    motpasse = Column("password", String(32))

