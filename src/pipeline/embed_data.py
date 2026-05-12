import os
import chromadb
from sentence_transformers import SentenceTransformer
from src.pipeline.data_cleansing import preprocess
import gzip
import json
import polars as pl
from tqdm import tqdm

script_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(script_path)))

PARQUET_PATH = os.path.join(project_root, 'data', 'amazon_catalog.parquet')
DB_PATH = os.path.join(project_root, 'data', 'chroma_db')

def run_batch_indexing(batch_size = 256):

    if not os.path.exists(PARQUET_PATH):
        print(f"Parquet file not found at {PARQUET_PATH}. Please ensure the file exists.")
        print('data_ingestion should be run before')
        return

    # Fast and efficient AI model for generating embeddings.
    # Every text is converted to list of 384 numbers.
    print('Initializing AI model for embeddings...')
    model = SentenceTransformer('all-mpnet-base-v2')

    print('Connecting to ChromaDB...')
    client = chromadb.PersistentClient(path=DB_PATH)
    collection_name = 'amazon_products'

    try:
        client.delete_collection(name=collection_name)
        print(f"Existing collection '{collection_name}' deleted.")
    except:
        pass

    collection = client.create_collection(name=collection_name)

    # Reading Parquet
    print(f"Reading data from {PARQUET_PATH}...")
    df = pl.read_parquet(PARQUET_PATH).head(15000)
    total_lines = df.height

    print('Initializing batch indexing...')
    # Loop for processing batches
    for i in tqdm(range(0, total_lines, batch_size), desc="Indexing batches"):
        
        print(f"Processing batch {i//batch_size + 1}...")

        # Dataframe slice
        batch_df = df.slice(i, batch_size)
        lines = batch_df.to_dicts()

        texts_to_ai = []
        ids = []
        metadata = []

        for line in lines:

            clean_items = preprocess(line)

            if clean_items.get('content') and clean_items.get('asin'):
                
                texts_to_ai.append(clean_items['content'])
                ids.append(clean_items['asin'])
                metadata.append({ "title": clean_items['title']})

        # If batch ended up empty (all produts were invalid)
        if not texts_to_ai:
            continue

        # Where AI process all texts and generates the embeddings
        print(f"Generating embeddings for batch {i//batch_size + 1}...")
        embeddings = model.encode(texts_to_ai)

        print(f"Upserting batch {i//batch_size + 1} to ChromaDB...")
        collection.upsert(
            ids = ids,
            embeddings = embeddings.tolist(),
            metadatas = metadata
        )


if __name__ == '__main__':
    run_batch_indexing(batch_size = 256)