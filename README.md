*🇺🇸 Read in English | 🇧🇷 [Ler em Português](README.pt-br.md)*

# Amazon Smart Research - High-Scale AI (CDs & Vinyl)

## Project Description
This project consists of developing an end-to-end semantic search engine designed to process and index Amazon's massive catalog (approximately 700,000 products in the CDs & Vinyl category). Unlike traditional exact-match keyword searches, this system uses Artificial Intelligence and Natural Language Processing (NLP/LLM) to understand the context, emotions, and abstract concepts within user queries (e.g., "melancholic jazz for a rainy day"), delivering highly accurate results.

**[🚀 Live Demo](https://amazon-smart-research.streamlit.app/)**

## Business Impact
In the current E-commerce market, search failure is one of the leading causes of Search Abandonment. If a customer searches for a concept and the platform doesn't understand it, the sale is lost. 
* **Customer Retention:** The developed engine eliminates the barrier of literal search, interpreting the consumer's real intent.
* **Industrial Scalability:** The pipeline was architected to evolve from a mere academic prototype to handling real Big Data (nearly 1 million records), simulating the real-world scenario of major tech companies.
* **Cost Efficiency (ROI):** The entire infrastructure was designed for massive cloud processing with optimized compute costs, performing the heavy lifting via batch processing, and ensuring an extremely cheap and fast production search operation.

## Technical Architecture & Data Pipeline
The system was modularized into independent layers following Software Engineering best practices:

1. **Ingestion & Cleansing Layer (ETL):** Utilization of the Polars library for data manipulation. The choice of Polars over Pandas was justified by its multithreaded execution performance, allowing the processing of high-volume files in seconds with low RAM consumption.
2. **Vectorization Layer (Embedding Pipeline):** Transformation of raw texts into dense 768-dimensional vectors using the State-of-the-Art LLM `all-mpnet-base-v2` (SentenceTransformers). Processing was parallelized in batches (batch size: 256) and executed in a high-performance cloud computing environment using GPU acceleration (Nvidia T4).
3. **Vector Database Layer:** Indexing and data persistence in ChromaDB. The search is based on mathematical distance calculation (cosine similarity), allowing for instantaneous scanning of the high-scale database.
4. **Application Layer (Interface):** Deployment of a real-time web application using Streamlit Cloud, seamlessly connecting the front-end to the semantic search engine.

## Engineering Challenges Overcome
During the large-scale development cycle, a major infrastructure bottleneck was identified: the write time of the vector database directly to a cloud network storage (Google Drive) was generating an Input/Output (I/O) overhead, increasing the estimated processing time to over 4 hours due to the network traffic of thousands of small SQLite files.

* **Applied Solution:** I refactored the data pipeline to operate on a "Local Cache with Asynchronous Persistence" architecture. The database is now generated on the temporary, local NVMe SSD of the GPU virtual machine. This drastically reduced the write time per batch, optimizing pipeline efficiency and protecting data integrity against network fluctuations. Ultimately, the finalized database is compressed and transferred entirely.

## Technologies Used
* Python
* Polars (Big Data & Performance)
* SentenceTransformers / PyTorch (Deep Learning & AI)
* ChromaDB (Vector Database)
* Google Colab / Cloud Computing (Nvidia T4 GPU Infrastructure)
* Streamlit (Deploy & User Interface)
* Git / GitHub (Version Control)
