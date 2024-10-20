## LlamaIndex-Qdrant-QA-Pipeline
This repository contains a streaming Q&A pipeline using the LlamaIndex framework and Qdrant vector database. 

The pipeline is deployed using Docker-compose with a FastAPI app and nginx and Gunicorn servers. 



![image](https://github.com/user-attachments/assets/60e172b8-75ed-4370-bcce-d290eadafda6)


### Main Features
  
- Platform: Docker, Docker-compose

- Vector DB: Qdrant

- Parsing: Uses SimpleDirectoryReader Future Additions(LlamaParse,Unstructured-io,NaverClovaOcr,UpstageDocumentParse)

- Indexing: Uses SentenceSplitter Future Additions(Semantic Splitter,small2big)

- Hybrid Search: Implements hybrid search functionality using the BM25 algorithm. Future Additions(Query Rewriting,query expansion ,HyDE)

- Embedding and Model: upskyy/kf-deberta-multitask

- Reranker Model: Dongjin-kr/ko-reranker

- Databases: PostgreSQL (SQL)

- Streaming: ON

- LLM: OpenAI or SLM Future Additions(Claude,Gemini)

- Prompt

- Machine Learning Service Deployment: FastAPI, Uvicorn, Gunicorn, Nginx

- Streamlit: UI

- Rag framework: Llamaindex

- Future Additions:data preprocessing,Summary,Query Classification,evaluation, Monitoring

### Service Ports
Most of the ports can be customized in the .env file at the root of this repository. Here are the default values:

- PostgreSQL: 5432
- pgAdmin: 16543 (user: pgadmin123@gmail.com, password: pgadmin123)
- Deep Learning Service: 8888
- Web UI Interface for Deep Learning Service: 4243
- Nginx: 80

### Configuration

This project uses a config.yaml file to manage various settings.  File location ```services/dl_service/app/config/config.yaml```:
```
generator:
  llm_type: openai ### openai,local
  model: gpt-4o-mini ### gpt-4o-mini, sosoai/hansoldeco-gemma-2-2b-v0.1
  max_new_tokens: 500

gpu:
  use: false

data:
  path: files
retriever:
  bm25_retriever: true
  bm25_top_k: 3
  chunk_size: 500
  chunk_overlap: 0
  embed_model:
    model_name: upskyy/kf-deberta-multitask
    embed_dimensional: 768
    top_k: 10
  collection_name: kakaobank
  qdrant_url: http://qdrant:6333 # Or use "http://qdrant:6333" as needed
  reranker_model:
    model_name: Dongjin-kr/ko-reranker #corrius/cross-encoder-mmarco-mMiniLMv2-L12-H384-v1
    top_n: 5
  vector_store: qdrant

```

  
### How to Use
- Make sure the .env file is complete:
```
POSTGRES_PORT=5432
DL_SERVICE_PORT=8888
WEB_UI_PORT=4243
NGINX_PORT=80
DB_API_LOG_TABLE_NAME=api_log
MAIN_DB_PW=pgadmin123
OPENAI_API_KEY = "Enter your API KEY"
```

- At the root of the repo directory, run ```docker-compose up``` or ```docker-compose up -d``` to detach the terminal.

  
- If you are not using an ARM-based computer (e.g., Mac M1 for development), you need to comment out the linux/arm64 lines in docker-compose.yml. Otherwise, the system will not function properly.
Setup Instructions
- [For users with CUDA] If you have CUDA-compatible GPU(s), you can uncomment deploy section under
dl_service in docker-compose.yml and change the base image in services/dl_service/Dockerfile from
ubuntu:18.04 to nvidia/cuda:11.4.3-cudnn8-devel-ubuntu20.04 (the text is there in the file, you just
need to comment and uncomment) to leverage your GPU(s). You might also need to install nvidia-container-
toolkit on the host machine to make it work. For Windows/WSL2 users, we found this article very helpful.


