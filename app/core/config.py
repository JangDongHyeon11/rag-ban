import os
import yaml
from dotenv import load_dotenv
import openai
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
# tiktoken
import tiktoken
# Load environmental variables from .env file
load_dotenv()

def load_config():
    with open('config/config.yaml', 'r') as file:
        return yaml.safe_load(file)

class Config:
    _config = load_config()

    QDRANT_URL = _config['retriever']['qdrant_url']
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    EMBED_DIMENSIONAL = _config['retriever']['embed_model']['embed_dimensional']
    EMBED_MODEL_NAME = _config['retriever']['embed_model']['model_name']
    EMBED_MODEL_TOP_K = _config['retriever']['embed_model']['top_k']
    COLLECTION_NAME = _config['retriever']['collection_name']
    BM25_RETRIEVER = _config['retriever']['bm25_retriever']
    BM25_TOP_K = _config['retriever']['bm25_top_k']
    RERANKER_MODEL_NAME = _config['retriever']['reranker_model']['model_name']
    RERANKER_MODEL_TOP_K = _config['retriever']['reranker_model']['top_n']
    DATAPATH = _config['data']['path']
    CHUNK_SIZE = _config['retriever']['chunk_size']
    CHUNK_OVERLAP = _config['retriever']['chunk_overlap']
    LLM_TYPE = _config['generator']['llm_type']
    GEN_MODEL = _config['generator']['model']  
    
    OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")
    if(LLM_TYPE =="openai"):
        openai.api_key = OPENAI_API_KEY
        Settings.llm = OpenAI(model="gpt-4o-mini", temperature=0)
        # Settings.tokenizer = tiktoken.encoding_for_model(GEN_MODEL).encode

            
config = Config()
