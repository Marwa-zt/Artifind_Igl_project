from fastapi import FastAPI , BackgroundTasks , HTTPException
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from sqlalchemy import create_engine , select
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import logging 
from typing import List
import sys
sys.path.append(r'C:\Users\dell\Desktop\TPIGL_2024_Artifind_versionF\Artifind-versionF\backend')
import models
from models import Article
import json



#retournant des réponses appropriées aux clients de l'API en cas d'erreur.
# logging.basicConfig(filename='app.log', level=logging.ERROR)
index_name = "index_article"
last_indexed_id = None  # Variable pour stocker le dernier ID indexé


# créer une instance de FastAPI

##app = FastAPI ()

#es = Elasticsearch(['https://localhost:9200'], basic_auth=('elastic', 'DuM926SgH0j078rOv4Dm'), verify_certs=False)


# Connexion à Elasticsearch
try:
    es = Elasticsearch(['https://localhost:9200'], basic_auth=('elastic', 'DuM926SgH0j078rOv4Dm'), verify_certs=False)
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
        # Connexion à la base de données
        with engine.connect() as connection:
            # Création d'une requête SQL pour sélectionner les articles avec un ID supérieur à last_indexed_id
            query = select([Article]).where(Article.id > last_indexed_id) if last_indexed_id else select([Article])

            # Exécution de la requête SQL
            result = connection.execute(query)

            # Récupération des données des nouveaux articles
            new_articles = result.fetchall()

        return new_articles

    except Exception as e:
        # Gestion des erreurs
        logging.error(f"Erreur lors de la récupération des nouveaux articles depuis la base de données : {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération des données depuis la base de données")



# Fonction pour formater les données pour Elasticsearch   
def format_articles_for_elasticsearch(new_articles):
    formatted_articles = []
    for article in new_articles:
        formatted_article = {
            'id': article.id,
            'titre': article.titre,
            'resume': article.resume,
            'texte_integral':article.text_integral ,
            'date': article.date.strftime('%Y-%m-%d'),  # Formatage de la date au format 'YYYY-MM-DD'
            'auteurs': [f"{a.nom} {a.prenom}  " for a in article.auteur],
            'refs':[j.nom for j in article.refs],
            'institutions': [i.nom for i in article.institutions],
            'motscles':[k.mot for k in article.motscles]
        }
        formatted_articles.append(formatted_article)
    return json.dumps(formatted_articles)



# Fonction pour indexer les données dans Elasticsearch
def index_data_in_elasticsearch(formatted_data_json):
    global last_indexed_id
    formatted_articles = json.loads(formatted_data_json)
    
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body={"mappings": {"properties": { "id": {"type": "int"},"titre": {"type": "text"}, "resume": {"type": "text"} , "texte_integral": {"type": "text"} , "date": {"type": "date"},  "auteurs": {"type": "keyword"}, "refs": { "type": "text"  }, "institutions": {"type": "keyword"} ,"motscles": {"type": "keyword"} }
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
                "fields": ["titre", "resume", "auteurs" , "institutions" , "texte_integral" ,"refs", "motscles"]
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
            "texte_integral": hit['_source'].get('texte_integral', ''),
            "date": hit['_source'].get('date', ''),
            "auteurs": hit['_source'].get('auteurs', ''),
            "refs": hit['_source'].get('refs', ''),
            "institutions": hit['_source'].get('institutions', ''),
            "motscles": hit['_source'].get('motscles', '')
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
            "texte_integral": result['texte_integral'],
            "date": result['date'],
            "auteurs": result['auteurs'],
            "refs": result['refs'],
            "institutions": result['institutions'],
            "motscles": result['motscles']
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
            "texte_integral": result['texte_integral'],
            "date": result['date'],
            "auteurs": result['auteurs'],
            "refs": result['refs'],
            "institutions": result['institutions'],
            "motscles": result['motscles']
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
            "texte_integral": result['texte_integral'],
            "date": result['date'],
            "auteurs": result['auteurs'],
            "refs": result['refs'],
            "institutions": result['institutions'],
            "motscles": result['motscles']
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
            "texte_integral": result['texte_integral'],
            "date": result['date'],
            "auteurs": result['auteurs'],
            "refs": result['refs'],
            "institutions": result['institutions'],
            "motscles": result['motscles']
        }
        for result in cached_results if keyword in result['motscles']
    ]
    cached_results[:] = filtered_results  # Mise à jour de cached_results avec les nouveaux résultats
    return filtered_results



# La fonction main 
def main () :
    
    
   # Initial indexing when the application starts
    background_tasks = BackgroundTasks()
    index_new_articles(background_tasks)
    # ajoute un gestionnaire d'événements au démarrage de l'application  
    app.add_event_handler("startup", index_new_articles, background_tasks) 




if __name__ == '__main__' :
   main 