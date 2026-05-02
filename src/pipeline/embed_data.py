import os
import chromadb
from sentence_transformers import SentenceTransformer
from src.pipeline.data_cleansing import preprocess
import gzip
import json

script_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(script_path)))

DATA_PATH = os.path.join(project_root, "data", "meta_CDs_and_Vinyl.jsonl.gz")

# Fast and efficient AI model for generating embeddings.
# Every text is converted to list of 384 numbers.
model = SentenceTransformer('all-MiniLM-L6-v2')

# Storing in local databse
client = chromadb.PersistentClient(path=os.path.join(project_root, "chroma_db"))
collection = client.get_or_create_collection(name="amazon_vinyls")

def run_indexing(limit = 100):

    if not os.path.exists(DATA_PATH):
        print(f"Data file not found")
        return

    documents = []
    metadatas = []
    ids = []

    seen_asins = set()

    with gzip.open(DATA_PATH, 'rt', encoding='utf-8') as f:
        for i, line in enumerate(f):
            
            if len(ids) >= limit:
                break

            raw_item = json.loads(line)

            if not raw_item.get('title'):
                continue

            clean_item = preprocess(raw_item)
            current_id = clean_item.get('asin')

            if current_id and current_id not in seen_asins:
                documents.append(clean_item['content'])
                ids.append(current_id)
                metadatas.append({"title": clean_item['title']})
                seen_asins.add(current_id)

    # Generate the 384 embeddings for documents and save it on disk
    if ids:
        collection.upsert(
            documents=documents,
            ids=ids,
            metadatas=metadatas
        )
        print(f"Indexed {collection.count()} items")
    else:
        print("No valid items found to index.")

if __name__ == '__main__':
    run_indexing(limit=500)