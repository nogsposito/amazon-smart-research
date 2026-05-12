# python -m src.pipeline.search

import os
import chromadb

script_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(script_path)))
db_path = os.path.join(project_root, "chroma_db")

# Connects to database
def get_db_coolection():

    client = chromadb.PersistentClient(path=db_path)

    # Takes items in the database collection
    try:
        collection = client.get_collection(name="amazon_products")
        total_items = collection.count()
        print(f'Collection found: {total_items} items')
        return collection
    except ValueError:
        print('Collection not found')
        return None

# Search for the most similar items in the database collection
def search_disks(query, top_k = 5):

    collection = get_db_coolection()

    if not collection:
        return []

    results = collection.query(
        query_texts = [query], n_results = top_k
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