from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base





URL_DATABASE ="mysql+mysqlconnector://root:ah123//12ah@localhost:3306/artifind"

#engine = create_engine(URL_DATABASE, connect_args= ({'check_same_thread': False}))
engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False,bind=engine)

Base = declarative_base()
 