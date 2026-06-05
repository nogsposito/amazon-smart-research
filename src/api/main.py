import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import chromadb

# script_path = os.path.abspath(__file__)
# project_root = os.path.dirname(os.path.dirname(os.path.dirname(script_path)))

# FastAPI 
app = FastAPI(
    title = 'Amazon Smart Research API',
    description = 'API for searching Amazon vinyl & CD records based on user queries.',
    version = '1.0'
)

DB_PATH = os.environ.get("DB_PATH", "./loaded_db")

# Connecting to Database
try:
    client = chromadb.PersistentClient(path=DB_PATH)
    collection = client.get_collection(name="amazon_vinyls")
except Exception as e:
    print(f"Warning: Could not connect to ChromaDB. Ensure the 'loaded_db' folder exists. Error: {e}")
    collection = None

class SearchRequest(BaseModel):
    query: str
    limit: int = 5

# ROUTES (Endpoints)

# Root endpoint (Health Check)
@app.get('/')
def home():
    if collection is None:
        return {"status": "degraded", "message": "API is running, but Vector DB is missing"}
    
    return {
        'status': 'online',
        'message': 'Welcome to the Amazon Smart Research API!',
        'items_in_collection': collection.count()
    }

# Search route: Main endpoint
@app.get('/search')
def search_records(payload: SearchRequest):
    
    if collection is None:
        raise HTTPException(status_code=503, detail="Database is not initialized.")
        
    if not payload.query.strip():
        raise HTTPException(status_code=400, detail="Search query cannot be empty.")
        
    try:
        # Querying the ChromaDB collection
        results = collection.query(
            query_texts=[payload.query],
            n_results=payload.limit
        )

        formatted_results = []

        # Extracting data from the ChromaDB response dictionary
        ids = results['ids'][0]
        metadata = results['metadatas'][0]
        distances = results['distances'][0]

        for i in range(len(ids)):
            record = {
                "Rank": i + 1,
                "ASIN": ids[i],
                # Ensure the key matches exactly how you stored it in your pipeline
                "Title": metadata[i].get('title', 'Unknown Title'), 
                "Distance": round(distances[i], 4) 
            }
            formatted_results.append(record)
            
        return {
            "original_query": payload.query,
            "results": formatted_results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")