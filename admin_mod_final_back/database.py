from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# ... rest of your code




#URL_DATABASE ="sqlite:///your_database.db"

URL_DATABASE ="mysql+mysqlconnector://admin:1234567890@localhost:3306/artifind"

#engine = create_engine(URL_DATABASE, connect_args= ({'check_same_thread': False}))
engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False,bind=engine)

Base = declarative_base()
 