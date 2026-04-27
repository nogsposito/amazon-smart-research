import gzip
import json
import os

DATA_PATH = 'data/meta_CDs_and_Vinyl.jsonl.gz'

# Initial version of metadata processing: in order to avoid overloading the system (reading one at a time)
def process_metadata():
    if not os.path.exists(DATA_PATH):
        print("Error")
        return

    with gzip.open(DATA_PATH, 'rt', encoding='utf-8') as f:
        for i, line in enumerate(f):
            item = json.loads(line) # loads as dictionary
            
            title = item.get('title', 'Untitled')
            print(f"Processing item {i}: {title}")
            
            if i >= 9:
                break

if __name__ == "__main__":
    process_metadata()