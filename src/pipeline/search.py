# python -m src.pipeline.search

import os
import chromadb

script_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(script_path)))
db_path = os.path.join(project_root, "chroma_db")

# Connects to database
client = chromadb.PersistentClient(path=db_path)

# Takes items in the database collection
try:
    collection = client.get_collection(name="amazon_vinyls")
    total_items = collection.count()
    print(f'Collection found: {total_items} items')
except ValueError:
    print('Collection not found')
    exit()

# Search for the most similar items in the database collection
def search_disks(query, top_k = 5):

    results = collection.query(
        query_texts = [query], n_results = top_k
    )

    ids = results['ids'][0]
    metadata = results['metadatas'][0]
    distance = results['distances'][0]

    for i in range (len(ids)):

        title = metadata[i]['title']
        asin = ids[i]

        print(f"NUMBER {i+1}: ASIN: {asin}, Title: {title}, Distance: {distance[i]}")

if __name__ == '__main__':
    my_query = 'elegant jazz night'
    search_disks(my_query, top_k = 3)