# API

import os
from fastapi import FastAPI
import chromadb

script_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(script_path)))
db_path = os.path.join(project_root, "chroma_db")

# Web app 
app = FastAPI(
    title = 'Amazon Smart Research API',
    description = 'API for searching Amazon vinyl & CD records based on user queries.',
    version = '1.0'
)

# Connecting to Database
client = chromadb.PersistentClient(path=db_path)

collection = client.get_collection(name="amazon_vinyls")

# ROUTES (Endpoints)

# Root endpoint (Health Check)
@app.get('/')
def home():
    return {
        'status': 'online',
        'message': 'Welcome to the Amazon Smart Research API!',
        'items_in_collection': collection.count()
    }

# Search route: Main endpoint
@app.get('/search')
def search_records(query: str, limit: int = 5):
    
    results = collection.query(
        query_texts=[query],
        n_results=limit
    )

    formatted_result = []

    ids = results['ids'][0]
    metadados = results['metadatas'][0]
    distancias = results['distances'][0]

    for i in range(len(ids)):
        disco = {
            "posicao": i + 1,
            "asin": ids[i],
            "titulo": metadados[i]['title'],
            "score_distancia": round(distancias[i], 4) 
        }
        formatted_result.append(disco)
        
    return {
        "query_original": query,
        "results": formatted_result
    }