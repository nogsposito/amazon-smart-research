import gzip
import json
import re
from bs4 import BeautifulSoup

# Clear HTML tags that might come with metadata.
def clean_html(text):

    if not text:
        return ''
    
    soup = BeautifulSoup(text, 'html.parser') # remove tags html
    clean_text = soup.get_text(separator=' ')
    clean_text = re.sub(r'\s+', '', clean_text).strip() # remove extra whitespace
    return clean_text

# Transform the features list into a single string
def format_features(features):

    if isinstance(features, list):
        return ' '.join([clean_html(f) for f in features])

# Friendly formatting to be used for AI. Like a full description of what the product is.
def preprocess(item):

    asin = item.get('asin', '' ) # The Amazon product ID.
    
    title = clean_html(item.get('title', ''))

    # Treating description, which could be a list or a text
    description_raw = item.get('description', '')
    if isinstance(description_raw, list):
        description_raw = ' '.join(description_raw)
    
    description = clean_html(description_raw)
    features = format_features(item.get('features', []))

    combined_content = f"Product: {title}. About: {description}. Details: {features}"

    return {
        "asin": asin,
        "title": title,
        "content": combined_content
    }

if __name__ == '__main__':

    DATA_PATH = 'data/meta_CDs_and_Vinyl.jsonl.gz'

    processed_count = 0
    with gzip.open(DATA_PATH, 'rt', encoding='utf-8') as f:
        for line in f:
            raw_data = json.loads(line)
            if raw_data.get('title'):
                clean_record = preprocess(raw_data)
                if processed_count < 5:
                    print(processed_count)
                    print(clean_record['asin'])
                    print(f"Content: {clean_record['content'][:200]}...\n")
                processed_count += 1

            if processed_count >= 10:
                break