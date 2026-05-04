import streamlit as st
import chromadb
from sentence_transformers import SentenceTransformer
import os

os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

from src.pipeline.search import search_disks

st.set_page_config(page_title='AI Vynil and CD Amazon Search', page_icon = '🎵')

st.title('AI Vynil and CD Amazon Search')
query = st.text_input('Enter your search query here:', placeholder="Ex: relaxing jazz for a rainy day")

if st.button('Search'):
    if query:
        with st.spinner('Searching for best matches...'):

            results = search_disks(query, top_k = 5)

            if results:
                st.success(f'Found {len(results)} results!')
                for i, record in enumerate(results):
                    with st.container(border = True):
                        st.subheader(f"Result {i+1}")
                        st.write(f"**ASIN:** {record['ASIN']}")
                        st.write(f"**Title:** {record['Title']}")
                        st.write(f"**Similarity:** {record['Distance']}")
                        st.markdown(f"[🛒 See in Amazon](https://www.amazon.com/dp/{record['ASIN']})")  
            else:
                st.warning('No results found. Please try a different query.')
    else:
        st.error('Please enter a search query before clicking the search button.')