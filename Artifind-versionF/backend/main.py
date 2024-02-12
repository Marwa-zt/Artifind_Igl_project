from fastapi import FastAPI , BackgroundTasks , HTTPException,APIRouter, Depends, status
from pydantic import BaseModel
from typing import Annotated,List
import models
from sqlalchemy.orm import Session,sessionmaker
from database import engine, SessionLocal
import auth
import moderator
import upload
from auth import get_current_user
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from moderator import router
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from sqlalchemy import create_engine , select
from datetime import datetime
import logging  
import sys
sys.path.append(r'C:\Users\dell\Desktop\TPIGL_2024_Artifind_versionF\Artifind-versionF\backend')
import models
import extract
from models import Article
import json

logging.basicConfig(level=logging.DEBUG)
app = FastAPI()

app.include_router(auth.router)
app.include_router(moderator.router)
app.include_router(upload.router)
app.include_router(extract.router)

models.Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:3000",
    "localhost:3000",
    "http://localhost:5173"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.get("/", status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')

    # Check if the user is an admin and redirect to another page
    if user['role'] == 'admin':
        # Redirect logic for admin
        return {"message": "Welcome Admin! Redirect to admin page."}

    return {"User": user}


# -------------------HIBA-------------------------------------------

#retournant des réponses appropriées aux clients de l'API en cas d'erreur.
# logging.basicConfig(filename='app.log', level=logging.ERROR)
index_name = "index_article"
last_indexed_id = 5  # Variable pour stocker le dernier ID indexé

# Connexion à Elasticsearch
try:
    print("***************connected to elastic ****************")
    es = Elasticsearch(['https://localhost:9200'], basic_auth=('elastic', 'Q83RH6aUu5iRMA0cODIw'), verify_certs=False)
    if not es.ping():
        raise ConnectionError("Échec de la connexion à Elasticsearch.")
except ConnectionError as e:
    logging.error(f"Erreur de connexion à Elasticsearch : {e}")
    raise HTTPException(status_code=500, detail="Erreur de connexion à Elasticsearch")
except Exception as e:
    logging.error(f"Erreur lors de l'initialisation de l'objet Elasticsearch : {e}")
    raise HTTPException(status_code=500, detail="Erreur lors de l'initialisation de l'objet Elasticsearch")


# Connect to MySQL
try:
    engine = create_engine('mysql+mysqlconnector://marwa:12345678@localhost:3306/artifinddd')
    print("***************connected to Bdd ****************")
    
except Exception as e:
    logging.error(f"Erreur de connexion à MySQL : {e}")
    raise HTTPException(status_code=500, detail="Erreur de connexion à MySQL")

SessionLocal = sessionmaker(autocommit=False, bind=engine)



# Fonction pour extraire les articles avec un ID supérieur au dernier indexé
def fetch_new_articles(last_indexed_id):
    try:
        print('****************fetching new article***************')
        # Créez une session de base de données
        Session = sessionmaker(bind=engine)
        session = Session()

        # Sélectionnez les nouveaux articles avec un ID supérieur à last_indexed_id
        query = session.query(Article).filter(Article.id > last_indexed_id).all()

        # Fermez la session
        session.close()

        return query

    except Exception as e:
        # Gestion des erreurs
        logging.error(f"Erreur lors de la récupération des nouveaux articles depuis la base de données : {e}")


#---------------------------------fonction test--------------------------------

def get_all_articles():
    db = SessionLocal()
    return db.query(models.Article).all()      

def get_all_articles1(last_id=None):
    # Créer une session de base de données
    db = SessionLocal()
    # Récupérer tous les articles
    query = db.query(Article)

    # Filtrer les résultats si un dernier ID est spécifié
    if last_id is not None:
        query = query.filter(Article.id > last_id)

    # Récupérer les articles filtrés
    articles = query.all()

    # Fermer la session de la base de données
    db.close()

    # Retourner les articles
    return articles



# Fonction pour formater les données pour Elasticsearch   
def format_articles_for_elasticsearch(new_articles):
    formatted_articles = []
    for article in new_articles:
        formatted_article = {
            'id': article.id,
            'titre': article.titre,
            'resume': article.resume,
            'text_integral':article.text_integral ,
            'date': article.date.strftime('%Y-%m-%d'),  # Formatage de la date au format 'YYYY-MM-DD'
            'auteur': [f"{a.nom} {a.prenom}  " for a in article.auteur],
            'refs':[j.nom for j in article.refs],
            'institutions': [i.nom for i in article.institutions],
            'motscles':[k.mot for k in article.motscles],
            'url':article.url
        }
        formatted_articles.append(formatted_article)
    return json.dumps(formatted_articles)



# Fonction pour indexer les données dans Elasticsearch
def index_data_in_elasticsearch(formatted_data_json):
    print('*************indexing data in elastic search*************')
    global last_indexed_id
    formatted_articles = json.loads(formatted_data_json)
    
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body={"mappings": {"properties": { "id": {"type": "int"},"titre": {"type": "text"}, "resume": {"type": "text"} , "text_integral": {"type": "text"} , "date": {"type": "date","format": "yyyy-MM-dd"},  "auteur": {"type": "keyword"}, "refs": { "type": "text"  }, "institutions": {"type": "keyword"} ,"motscles": {"type": "keyword"} ,"url": {"type": "text"} }
                }}, ignore=400)

    actions = []

    for doc in formatted_articles:
        action = {
            "index": { "_index": index_name }  # Utilisation de "index" au lieu de "_op_type"
        }
        actions.append(action)
        actions.append(doc)  # Ajoutez le document après l'action

    response = es.bulk(body=actions, index=index_name)
    
     # Mise à jour du dernier ID indexé
    if not response.get("errors"):
        last_indexed_id = formatted_articles[-1]["id"]


    if response.get("errors"):
        for item in response["items"]:
            if "error" in item:
                error_message = item["error"]["reason"]
                print(f"Erreur lors de l'indexation : {error_message}")
                # Traitez l'erreur ici selon vos besoins
    else:
        print("Indexation réussie.")




# Background task to  index new articles
def index_new_articles(background_tasks: BackgroundTasks ):
    
    mysql_data = fetch_new_articles(last_indexed_id)
    formatted_data = format_articles_for_elasticsearch(mysql_data)
    index_data_in_elasticsearch(formatted_data)


# Fonction pour ajouter un nouvel article à la base de données
@app.post("/add_article")
async def add_article(article, background_tasks: BackgroundTasks):
    
    # Code pour ajouter un nouvel article à la base de données
    #.....

    background_tasks.add_task(index_new_articles) # appel au fonction qui index ce nouvel article dans ElasticSearch
    return {"message": "Article ajouté avec succès."}     



# variable pour stocker les résultats actuelles de la recherche 
cached_results = []   



# chercher dans les documents de elasticSearch le mot clé dans query 
def perform_elasticsearch_search(query: str):

    search_body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["titre", "resume", "auteur" , "institutions" , "text_integral" ,"refs", "motscles"]
            }
        }
    }
    search_results = es.search(index=index_name, body=search_body)
    hits = search_results["hits"]["hits"]

    formatted_results = []
    for hit in hits:
        result = {
            "titre": hit['_source']['titre'],
            "resume": hit['_source'].get('resume', ''),
            "text_integral": hit['_source'].get('text_integral', ''),
            "date": hit['_source'].get('date', ''),
            "auteur": hit['_source'].get('auteur', ''),
            "refs": hit['_source'].get('refs', ''),
            "institutions": hit['_source'].get('institutions', ''),
            "motscles": hit['_source'].get('motscles', ''),
            "url": hit['_source'].get('url', '')
        }
        formatted_results.append(result)
    cached_results.extend(formatted_results)

    return formatted_results


# Affecter une requette de recherche 
@app.get("/search/{query}")
async def search_articles(query: str):
    search_results = perform_elasticsearch_search(query)
    return {"results": search_results}


# ***filtrer par auteur 
@app.get("/filter_by_author/{author}")
async def filter_by_author(author: str):
    # Filtrer les résultats stockés dans cached_results par auteur
    filtered_results = [
        {
            "titre": result['titre'],
            "resume": result['resume'],
            "text_integral": result['text_integral'],
            "date": result['date'],
            "auteur": result['auteur'],
            "refs": result['refs'],
            "institutions": result['institutions'],
            "motscles": result['motscles'],
            "url": result['url']
        }
        for result in cached_results if author in result['auteurs']
    ]
    cached_results[:] = filtered_results  # Mise à jour de cached_results avec les nouveaux résultats
    return filtered_results


# ***filtrer les résultats de la recherche par institution 
@app.get("/filter_by_institution/{institution}")
async def filter_by_institution(institution: str):
    # Filtrer les résultats stockés dans cached_results par institution
    filtered_results = [
        {
           "titre": result['titre'],
            "resume": result['resume'],
            "text_integral": result['text_integral'],
            "date": result['date'],
            "auteur": result['auteur'],
            "refs": result['refs'],
            "institutions": result['institutions'],
            "motscles": result['motscles'],
            "url": result['url']

        }
        for result in cached_results if institution in result['institutions']
    ]
    cached_results[:] = filtered_results  # Mise à jour de cached_results avec les nouveaux résultats
    return filtered_results

# ***filtrer les résultats de la reccherche selon date de publication 
@app.get("/filter_by_publication_date/{start_date}/{end_date}")
async def filter_by_publication_date(start_date: str, end_date: str):
    # Convertir les dates fournies en objets datetime
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    # Filtrer les résultats stockés dans cached_results entre les deux dates
    filtered_results = [
        {
            "titre": result['titre'],
            "resume": result['resume'],
            "text_integral": result['text_integral'],
            "date": result['date'],
            "auteur": result['auteur'],
            "refs": result['refs'],
            "institutions": result['institutions'],
            "motscles": result['motscles'],
            "url": result['url']
        }
        for result in cached_results 
        if start_date <= datetime.strptime(result['date'], "%Y-%m-%d").date() <= end_date
    ]
    cached_results[:] = filtered_results  # Mise à jour de cached_results avec les nouveaux résultats
    return filtered_results


#***filtere les résultats de la recherche selon les mots clés 
@app.get("/filter_by_keyword/{keyword}")
async def filter_by_keyword(keyword: str):
    # Filtrer les résultats stockés dans cached_results par mot-clé dans le champ texte_integral
    filtered_results = [
        {
            "titre": result['titre'],
            "resume": result['resume'],
            "text_integral": result['text_integral'],
            "date": result['date'],
            "auteur": result['auteur'],
            "refs": result['refs'],
            "institutions": result['institutions'],
            "motscles": result['motscles'],
            "url": result['url']
        }
        for result in cached_results if keyword in result['motscles']
    ]
    cached_results[:] = filtered_results  # Mise à jour de cached_results avec les nouveaux résultats
    return filtered_results

# Fonction main
try:
    print('**********m***************')
    
    A = get_all_articles1(last_indexed_id)
    for article in A :
        print(article.id)

    #dgag = format_articles_for_elasticsearch (A)
    #print("dgag")
   
    # Initial indexing when the application starts
    # background_tasks = BackgroundTasks()
    # index_new_articles(background_tasks)
    # ajoute un gestionnaire d'événements au démarrage de l'application  
    #app.add_event_handler("startup", index_new_articles, background_tasks) 
    print ('*************index main****************')

    """
    for result in results:
     print("Titre:", result["titre"])
     print("Résumé:", result["resume"])
     print("Texte intégral:", result["text_integral"])
     print("Date:", result["date"])
     print("Auteurs:", result["auteur"])
     print("Références:", result["refs"])
     print("Institutions:", result["institutions"])
     print("Mots-clés:", result["motscles"])
     print("\n")

    """



    


   

except Exception as e:
    logging.error(f"Erreur d'execution : {e}")
    raise HTTPException(status_code=500, detail="Erreur d'exec")
    
SessionLocal = sessionmaker(autocommit=False, bind=engine)







"""# La fonction main 
def main () :
    print('**********main***************')
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body={"mappings": {"properties": { "id": {"type": "int"},"titre": {"type": "text"}, "resume": {"type": "text"} , "texte_integral": {"type": "text"} , "date": {"type": "date"},  "auteurs": {"type": "keyword"}, "refs": { "type": "text"  }, "institutions": {"type": "keyword"} ,"motscles": {"type": "keyword"} }
                }}, ignore=400)
    search_body = {
    "query": {"match_all": {}}}

    # Exécution de la requête de recherche
    search_result = es.search(index=index_name, body=search_body)

    # Affichage des informations de chaque document
    for hit in search_result['hits']['hits']:
        result = hit['_source']
        print("Titre:", result.get("titre"))
        print("Résumé:", result.get("resume"))
        print("Texte intégral:", result.get("texte_integral"))
        print("Date:", result.get("date"))
        print("Auteurs:", result.get("auteurs"))
        print("Références:", result.get("refs"))
        print("Institutions:", result.get("institutions"))
        print("Mots-clés:", result.get("motscles"))
        print("\n")

   # Initial indexing when the application starts
    background_tasks = BackgroundTasks()
    index_new_articles(background_tasks)
    # ajoute un gestionnaire d'événements au démarrage de l'application  
    app.add_event_handler("startup", index_new_articles, background_tasks) 
    print ('*************index main****************')
    search_body = {
    "query": {"match_all": {}}}

    # Exécution de la requête de recherche
    search_result = es.search(index=index_name, body=search_body)

    # Affichage des informations de chaque document
    for hit in search_result['hits']['hits']:
        result = hit['_source']
        print("Titre:", result.get("titre"))
        print("Résumé:", result.get("resume"))
        print("Texte intégral:", result.get("texte_integral"))
        print("Date:", result.get("date"))
        print("Auteurs:", result.get("auteurs"))
        print("Références:", result.get("refs"))
        print("Institutions:", result.get("institutions"))
        print("Mots-clés:", result.get("motscles"))
        print("\n")




if __name__ == '__main__' :
   main """

