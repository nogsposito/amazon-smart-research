import os
import polars as pl

script_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(script_path)))

JSON_PATH = os.path.join(project_root, "data", "meta_CDs_and_Vinyl.jsonl.gz")
PARQUET_PATH = os.path.join(project_root, "data", "amazon_catalog.parquet")

def convert_json_to_parquet():
    if not os.path.exists(JSON_PATH):
        print(f"Data file not found at {JSON_PATH}")
        return

    try:
        df = pl.read_ndjson(JSON_PATH, infer_schema_length=10000, ignore_errors=True)
        total_lines = df.height
        print(f"Total lines read: {total_lines}")

        # Most useful lines
        desired_columns = ['parent_asin', 'asin', 'title', 'description', 'features', 'categories']
        present_columns = [col for col in desired_columns if col in df.columns]
        clean_df = df.select(present_columns)
        
        clean_df.write_parquet(PARQUET_PATH, compression = 'zstd')

        print('Data saved successfully to Parquet format')

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    convert_json_to_parquet()