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

    asin = item.get('parent_asin', '' ) # The Amazon product ID.
    
    title = clean_html(item.get('title', ''))

    # Treating description, which could be a list or a text
    raw_desc = item.get('description', [])
    if isinstance(raw_desc, list):
        raw_desc = " ".join(raw_desc)
    description = clean_html(raw_desc)

    categories = item.get('categories', [])
    if isinstance(categories, list):
        # Removemos 'CDs & Vinyl' se estiver presente, pois é redundante para a busca
        categories = [c for c in categories if c != 'CDs & Vinyl']
        categories_str = ", ".join(categories)
    else:
        categories_str = str(categories)
    
    features = item.get('features', [])
    if isinstance(features, list):
        features_str = ". ".join([clean_html(f) for f in features])
    else:
        features_str = clean_html(str(features))
    
    content_parts = []

    if title:
        content_parts.append(f"Title: {title}")
    if categories_str:
        content_parts.append(f"Genres/Categories: {categories_str}")
    if features_str:
        content_parts.append(f"Features: {features_str}")
    if description:
        content_parts.append(f"Description: {description}")
    
    content = '. '.join(content_parts)

    return {
        "asin": asin,
        "title": title,
        "content": content
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