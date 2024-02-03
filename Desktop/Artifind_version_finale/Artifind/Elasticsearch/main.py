# vérifier les paramètre de connexion avec BDD
# L'adapter avec BDD
# acceder à la partie qui contier des article vérifier d'après les modérateur 
from fastapi import FastAPI , BackgroundTasks , Query
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from sqlalchemy import create_engine

# créer une instance de FastAPI
app = FastAPI ()

# Connexion à Elasticsearch
es = Elasticsearch(['https://localhost:9200'], basic_auth=('elastic', 'ZTwHulctYUrbUtc_EA+Y'), verify_certs=False)
index_name = "index_article"
last_indexed_id = None  # Variable pour stocker le dernier ID indexé


# Connect to MySQL
engine = create_engine('mysql+mysqlconnector://user:password@localhost:3306/artifind')

#fetch data from MySQL
def fetch_data_from_mysql(last_id=None):
    # Connect to the database
    with engine.connect() as connection:
        # Execute a SELECT query on the 'article' table
        query = f'SELECT * FROM article WHERE id > {last_id}' if last_id else 'SELECT * FROM article'
        result = connection.execute(query)
        # Fetch all rows
        rows = result.fetchall()
    # Return the fetched data
    return rows


# Format data for Elasticsearch
def format_data_for_elasticsearch(rows):
    formatted_data = []   # créer une liste des document récupérés de la BBD
    for row in rows:
        doc = {
            'id':row[1] ,
            'titre': row[2],
            'resume': row[3],
            'auteurs': row[4],
            'institutions': row[5],
            'texte_integral': row[6],
            'date_publication': row[7],
        }
        formatted_data.append(doc)   # à chaque fois on recupère un document de l'article on l'ajoute à la liste
    return formatted_data   # returner la liste des document 


# Index data in Elasticsearch
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
     
    # Mettez à jour le dernier ID indexé
    if actions:
        last_indexed_id = actions[-1]['_source']['id']
    

# Background task to  index new articles
def index_new_articles(background_tasks: BackgroundTasks ):
    
    mysql_data = fetch_data_from_mysql(last_indexed_id)
    formatted_data = format_data_for_elasticsearch(mysql_data)
    index_data_in_elasticsearch(formatted_data)


# Fonction pour ajouter un nouvel article à la base de données
def add_new_article_to_database(article , background_tasks: BackgroundTasks ):
    
    # Code pour ajouter un nouvel article à la base de données
    
    #......


    # Planifier l'indexation en arrière-plan
    background_tasks.add_task(index_new_articles)

    
    return {"message": "Article added successfully."}


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

    return search_results["hits"]["hits"]




# Affecter une requette pour ajouter un article à la base de données 
@app.post("/add_article")
async def add_article(article , background_tasks: BackgroundTasks):
    return add_new_article_to_database(article)


# Affecter une requette de recherche 
@app.get("/search")
async def search_articles(query: str = Query(..., title="Recherche")):
    search_results = perform_elasticsearch_search(query)
    return {"results": search_results}



# La fonction main 
def main () :
   # Initial indexing when the application starts
    background_tasks = BackgroundTasks()
    index_new_articles(background_tasks)

    # ajoute un gestionnaire d'événements au démarrage de l'application  
    app.add_event_handler("startup", index_new_articles, background_tasks)
   




if __name__ == '__main__' :
   main ()





