*🇧🇷 Ler em Português | 🇺🇸 [Read in English](README.md)*

# Amazon Smart Research - IA em Alta Escala (CDs e Vinis)

## Descrição do Projeto
Este projeto consiste no desenvolvimento de um motor de busca semântica de ponta a ponta, projetado para processar e indexar o catálogo massivo da Amazon (aproximadamente 700.000 produtos na categoria de CDs e Vinis). Ao contrário das buscas tradicionais por palavras-chave exatas, este sistema utiliza Inteligência Artificial e Processamento de Linguagem Natural (PLN/LLM) para compreender o contexto, as emoções e os conceitos abstratos contidos nas pesquisas dos usuários (ex: "jazz melancólico para um dia de chuva"), entregando resultados com precisão.

## O Impacto de Negócio
No mercado de E-commerce atual, a falha na busca é uma das maiores causas de abandono de carrinho (Search Abandonment). Se um cliente busca por um conceito e a plataforma não o entende, a venda é perdida. 
* **Retenção de Clientes:** O motor desenvolvido elimina a barreira da busca literal, interpretando o desejo real do consumidor.
* **Escalabilidade Industrial:** O pipeline foi arquitetado para deixar de ser apenas um protótipo acadêmico e passar a lidar com Big Data real (quase 1 milhão de registros), simulando o cenário real de grandes empresas de tecnologia.
* **Eficiência de Custos (ROI):** Toda a infraestrutura foi desenhada para processamento massivo em nuvem com custo de processamento otimizado, realizando o trabalho pesado em lote (batch processing) e garantindo uma operação de busca em produção extremamente barata e veloz.

## Arquitetura Técnica e Pipeline de Dados
O sistema foi modularizado em camadas independentes seguindo as boas práticas de Engenharia de Software:

1. **Camada de Ingestão e Limpeza (ETL):** Utilização da biblioteca Polars para manipulação de dados. A escolha do Polars em detrimento do Pandas justificou-se pela performance de execução multithreaded, permitindo processar arquivos de alta volumetria em segundos com baixo consumo de memória RAM.
2. **Camada de Vetorização (Embedding Pipeline):** Transformação de textos brutos em vetores densos de 768 dimensões utilizando o modelo de LLM State-of-the-Art `all-mpnet-base-v2` (SentenceTransformers). O processamento foi paralelizado em lotes (batches de 256) e executado em ambiente de nuvem computacional de alta performance utilizando processamento gráfico em GPU (Nvidia T4).
3. **Camada de Armazenamento Vetorial (Vector Database):** Indexação e persistência dos dados no ChromaDB. A busca é baseada em cálculo de distância matemática (similaridade de cosseno), permitindo varrer o banco de dados de alta escala instantaneamente.
4. **Camada de Aplicação (Interface):** Deploy de uma aplicação web em tempo real utilizando Streamlit Cloud, conectando o front-end ao motor de busca semântica de forma integrada.

## Desafios de Engenharia Superados (Resolução de Problemas)
Durante o ciclo de desenvolvimento em larga escala, um grande problema de infraestrutura foi identificado: o tempo de escrita do banco de dados vetorial diretamente em armazenamento de rede em nuvem (Google Drive) estava gerando um overhead de Input/Output (I/O), elevando o tempo estimado de processamento para mais de 4 horas devido ao tráfego de rede de pequenos arquivos.

* **Solução aplicada:** Reformulei o pipeline de dados para operar em arquitetura de "Cache Local com Persistência Assíncrona". O banco de dados passou a ser gerado no SSD NVMe local e temporário da máquina virtual da GPU. Isso reduziu drasticamente o tempo de gravação por lote, otimizando a eficiência do pipeline e protegendo a integridade dos dados contra oscilações de rede. Ao final, a base é compactada e transferida integralmente.

## Tecnologias Utilizadas
* Python
* Polars (Big Data e Performance)
* SentenceTransformers / PyTorch (Deep Learning e IA)
* ChromaDB (Vector Database)
* Google Colab / Cloud Computing (Nvidia T4 GPU Infrastructure)
* Streamlit (Deploy e Interface de Usuário)
* Git / GitHub (Controle de Versão)
