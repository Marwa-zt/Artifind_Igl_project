from fastapi import FastAPI , BackgroundTasks , Query , HTTPException
from elasticsearch import Elasticsearch , ElasticsearchException
from elasticsearch.helpers import bulk
from sqlalchemy import create_engine
import logging


#retournant des réponses appropriées aux clients de l'API en cas d'erreur.
logging.basicConfig(filename='app.log', level=logging.ERROR)


# créer une instance de FastAPI
app = FastAPI ()

# Connexion à Elasticsearch
try:
    es = Elasticsearch(['https://localhost:9200'], basic_auth=('elastic', 'ZTwHulctYUrbUtc_EA+Y'), verify_certs=False)
except ElasticsearchException as e:
    logging.error(f"Erreur de connexion à Elasticsearch : {e}")  # enregistrer l'erreur 
    raise HTTPException(status_code=500, detail="Erreur de connexion à Elasticsearch")  # gérere un requette Http 

index_name = "index_article"
last_indexed_id = None  # Variable pour stocker le dernier ID indexé

# Connect to MySQL
try:
    engine = create_engine('mysql+mysqlconnector://root:mariamarai@localhost:3306/artifind')
except Exception as e:
    logging.error(f"Erreur de connexion à MySQL : {e}")
    raise HTTPException(status_code=500, detail="Erreur de connexion à MySQL")


# Fonction pour récupérer les données depuis MySQL
def fetch_data_from_mysql(last_id=None):
    try:
        # Connect to the database
        with engine.connect() as connection:
            # Execute a SELECT query on the 'article' table
            query = f'SELECT * FROM article WHERE id > {last_id}' if last_id else 'SELECT * FROM article'
            result = connection.execute(query)
            # Fetch all rows
            rows = result.fetchall()
        return rows
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des données depuis MySQL: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération des données depuis MySQL")
        


# Fonction pour formater les données pour Elasticsearch
def format_data_for_elasticsearch(rows):
    formatted_data = []   # créer une liste des document récupérés de la BBD
    for row in rows:
        doc = {
            'id':row[0] ,
            'titre': row[1],
            'resume': row[2],
            'auteurs': row[3],
            'institutions': row[4],
            'texte_integral': row[5],
            'date_publication': row[6],
        }
        formatted_data.append(doc)   # à chaque fois on recupère un document de l'article on l'ajoute à la liste
    return formatted_data   # returner la liste des document 


# Fonction pour indexer les données dans Elasticsearch      data is formatted_data
def index_data_in_elasticsearch(data):
    global last_indexed_id
    # Ensure the index exists
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body={"mappings": {"properties": { "id": {"type": "int"},"titre": {"type": "text"}, "resume": {"type": "text"},  "auteurs": {"type": "keyword"}, "institutions": {"type": "keyword"}, "texte_integral": {"type": "text"}, "date_publication": {"type": "date"} }
                }}, ignore=400)
    # Use the Elasticsearch bulk helper for efficient indexing (mettre les info de chaque article dans l'index)
    actions = [
        {
            '_op_type': 'index',
            '_index': index_name,
            '_source': doc,
        }
        for doc in data
    ]
    es.bulk(actions=actions, index=index_name, raise_on_error=False)
    # Mise à jour le dernier ID indexé
    if actions:
        last_indexed_id = actions[-1]['_source']['id']


# Background task to  index new articles
def index_new_articles(background_tasks: BackgroundTasks ):
    
    mysql_data = fetch_data_from_mysql(last_indexed_id)
    formatted_data = format_data_for_elasticsearch(mysql_data)
    index_data_in_elasticsearch(formatted_data)


# Fonction pour ajouter un nouvel article à la base de données
@app.post("/add_article")
async def add_article(article, background_tasks: BackgroundTasks):
    
    # Code pour ajouter un nouvel article à la base de données
    #.....

    background_tasks.add_task(index_new_articles)
    return {"message": "Article ajouté avec succès."}



cached_results = []   # variable pour stocker les résultats actuelles de la recherche 
# chercher dans les documents de elasticSearch le mot clé dans query 
def perform_elasticsearch_search(query: str):

    search_body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["titre", "resume", "auteurs", "institutions", "mots_cles", "texte_integral", "date_publication"]
            }
        }
    }

    search_results = es.search(index=index_name, body=search_body)
    hits = search_results["hits"]["hits"]

    formatted_results = [
        {
            "titre": hit['_source']['titre'],
            "resume": hit['_source']['resume'],
            "auteurs": hit['_source']['auteurs'],
            "institutions": hit['_source']['institutions'],
            "texte_integral": hit['_source']['texte_integral'],
            "date_publication": hit['_source']['date_publication']
        }
        for hit in hits
    ]
    cached_results.extend(formatted_results)

    return formatted_results



# Affecter une requette de recherche 
@app.get("/search")
async def search_articles(query: str = Query(..., title="Recherche")):
    search_results = perform_elasticsearch_search(query)
    return {"results": search_results}


# ***filtrer par auteur 
@app.get("/filter_by_author")
async def filter_by_author(author: str = Query(..., title="Author Name")):
    # Filtrer les résultats stockés dans cached_results par auteur
    filtered_results = [
        {
            "titre": result['titre'],
            "resume": result['resume'],
            "auteurs": result['auteurs'],
            "institutions": result['institutions'],
            "texte_integral": result['texte_integral'],
            "date_publication": result['date_publication']
        }
        for result in cached_results if author in result['auteurs']
    ]
    cached_results[:] = filtered_results  # Mise à jour de cached_results avec les nouveaux résultats
    return filtered_results

# ***filtrer les résultats de la recherche par institution 
@app.get("/filter_by_institution")
async def filter_by_institution(institution: str = Query(..., title="Institution Name")):
    # Filtrer les résultats stockés dans cached_results par institution
    filtered_results = [
        {
            "titre": result['titre'],
            "resume": result['resume'],
            "auteurs": result['auteurs'],
            "institutions": result['institutions'],
            "texte_integral": result['texte_integral'],
            "date_publication": result['date_publication']
        }
        for result in cached_results if institution in result['institutions']
    ]
    cached_results[:] = filtered_results  # Mise à jour de cached_results avec les nouveaux résultats
    return filtered_results

# ***filtrer les résultats de la reccherche selon date de publication 
@app.get("/filter_by_publication_date")
async def filter_by_publication_date(publication_date: str = Query(..., title="Publication Date")):
    # Filtrer les résultats stockés dans cached_results par date de publication
    filtered_results = [
        {
            "titre": result['titre'],
            "resume": result['resume'],
            "auteurs": result['auteurs'],
            "institutions": result['institutions'],
            "texte_integral": result['texte_integral'],
            "date_publication": result['date_publication']
        }
        for result in cached_results if publication_date == result['date_publication']
    ]
    cached_results[:] = filtered_results  # Mise à jour de cached_results avec les nouveaux résultats
    return filtered_results


#***filtere les résultats de la recherche selon les mots clés 
@app.get("/filter_by_keyword")
async def filter_by_keyword(keyword: str = Query(..., title="Keyword")):
    # Filtrer les résultats stockés dans cached_results par mot-clé dans le champ texte_integral
    filtered_results = [
        {
            "titre": result['titre'],
            "resume": result['resume'],
            "auteurs": result['auteurs'],
            "institutions": result['institutions'],
            "texte_integral": result['texte_integral'],
            "date_publication": result['date_publication']
        }
        for result in cached_results if keyword in result['texte_integral']
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
   main ()





