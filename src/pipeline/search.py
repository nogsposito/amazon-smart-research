# python -m src.pipeline.search

import os
import chromadb
from sentence_transformers import SentenceTransformer

script_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(script_path)))
db_path = os.path.join(project_root, "chroma_db")

model = SentenceTransformer('all-mpnet-base-v2')

# Connects to database
def get_db_collection():

    client = chromadb.PersistentClient(path=db_path)

    # Takes items in the database collection
    client = chromadb.PersistentClient(path="./chroma_db")
    return client.get_collection(name="amazon_products")

# Search for the most similar items in the database collection
def search_disks(query, top_k = 5):

    try:
        collection = get_db_collection()
    except Exception as e:
        print(f"Error to connect: {e}")
        return []

    if not collection:
        return []
    
    query_embedding = model.encode([query])

    results = collection.query(
        query_embeddings=query_embedding.tolist(), 
        n_results=top_k
    )

    ids = results['ids'][0]
    metadata = results['metadatas'][0]
    distance = results['distances'][0]

    result_list = []

    for i in range (len(ids)):

        record = {
            'ASIN': ids[i],
            'Title': metadata[i]['title'],
            'Distance': round(distance[i], 4)
        }
        result_list.append(record)

    return result_list

if __name__ == '__main__':
    
    my_query = 'elegant jazz night'

    results = search_disks(my_query, top_k = 3)

    for res in results:
        print(f"NUMBER {results.index(res)+1}: ASIN: {res['ASIN']}, Title: {res['Title']}, Distance: {res['Distance']}")