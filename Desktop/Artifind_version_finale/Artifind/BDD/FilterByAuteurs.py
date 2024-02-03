from fastapi import FastAPI, Query
from elasticsearch import Elasticsearch

app = FastAPI()

# Assuming your Elasticsearch instance is running on localhost:9200
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
index_name = 'your_index_name'  # Replace with the actual name of your Elasticsearch index

@app.get("/filter_by_author")
async def filter_by_author(author: str = Query(..., title="Author Name")):
    query = {
        "query": {
            "match": {
                "auteurs": author
            }
        }
    }

    result = es.search(index=index_name, body=query)

    hits = result['hits']['hits']
    filtered_data = [{"titre": hit['_source']['titre'],
                      "resume": hit['_source']['resume'],
                      "auteurs": hit['_source']['auteurs'],
                      "institutions": hit['_source']['institutions'],
                      "text_integral": hit['_source']['text_integral'],
                      "url_pdf": hit['_source']['url_pdf'],
                      "references": hit['_source']['references']}
                     for hit in hits]

    return filtered_data
