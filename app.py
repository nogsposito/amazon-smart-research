import streamlit as st
from sentence_transformers import SentenceTransformer
import os
import requests

API_URL = "http://127.0.0.1:8000/api/v1/search"

os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

from src.pipeline.search import search_disks

st.set_page_config(page_title='AI Vynil and CD Amazon Search', page_icon = '🎵')

st.title('AI Vynil and CD Amazon Search')
query = st.text_input('Enter your search query here:', placeholder="Ex: relaxing jazz for a rainy day")

def get_cover_url(asin):
    return f"https://ws-na.amazon-adsystem.com/widgets/q?_encoding=UTF8&Format=_SL250_&ASIN={asin}&MarketPlace=US&ID=AsinImage&WS=1&ServiceVersion=20070822"

if st.button('Search'):
    if query:
        with st.spinner('Searching for best matches...'):

            try:
                # Send the payload to the FastAPI backend
                payload = {"query": query, "limit": 5}
                response = requests.post(API_URL, json=payload)
                
                # 2. We check if the API responded with success (200 OK)
                if response.status_code == 200:
                    data = response.json()
                    results = data.get("results", [])
                    
                    if results:
                        st.success(f"Found {len(results)} results!")
                        for i, record in enumerate(results):
                            with st.container(border=True):
                                col1, col2 = st.columns([1, 3])
                                
                                with col1:
                                    st.image(get_cover_url(record['ASIN']), use_container_width=True)
                                    
                                with col2:
                                    st.subheader(record['Title'])
                                    st.caption(f"**ASIN:** {record['ASIN']}")
                                    st.link_button("🛒 See on Amazon", f"https://www.amazon.com/dp/{record['ASIN']}")
                                    
                                    with st.expander("⚙️ Technical AI Details"):
                                        st.metric(label="Vector Distance", value=record['Distance'])
                    else:
                        st.warning('No results found.')
                else:
                    st.error(f"API Error: {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("Failed to connect to the backend API.")