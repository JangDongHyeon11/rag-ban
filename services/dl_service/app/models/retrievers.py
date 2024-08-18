from qdrant_client import QdrantClient
from AI.model import initialize_embedding_model,initialize_rerank_model
# from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import PromptTemplate, get_response_synthesizer
from llama_index.core.indices.vector_store.base import VectorStoreIndex
from llama_index.core.query_engine import RetrieverQueryEngine
from core.config import config
from core.hybrid_search import HybridRetriever
from llama_index.retrievers.bm25 import BM25Retriever
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.llms.openai import OpenAI
from core.llm_loader_cpu import LLMCPULoader
from core.llm_loader_gpu import LLMGPULoader

import torch
def initialize_retrievers():
    # GPU_USE에 따라 디바이스 설정
    if config.GPU_USE:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    else:
        device = torch.device('cpu')
    device = str(device) 
    client = QdrantClient(url=config.QDRANT_URL)
    embed_model = initialize_embedding_model(model_name=config.EMBED_MODEL_NAME,device=device)
    vector_store = QdrantVectorStore(client=client, collection_name=config.COLLECTION_NAME, embed_model=embed_model)
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store, embed_model=embed_model)
    retriever = VectorIndexRetriever(index=index, similarity_top_k=config.EMBED_MODEL_TOP_K)
    nodes=vector_store.get_nodes()
  
    
    # Check if BM25 retriever is enabled in the configuration
    if config.BM25_RETRIEVER:

        bm25_retriever = BM25Retriever.from_defaults(nodes=nodes, similarity_top_k=config.BM25_TOP_K)
        retriever_to_use = HybridRetriever(vector_retriever=retriever, bm25_retriever=bm25_retriever)

    else:
        retriever_to_use = VectorIndexRetriever(index=index,docstore=index.docstore, similarity_top_k=config.EMBED_MODEL_TOP_K)

    
    qa_prompt = PromptTemplate("""\
    Context information is below.
    ---------------------
    {context_str}
    ---------------------

    Given the context information and not prior knowledge, \
    answer the query. Please be concise, and complete. \
    If the context does not contain an answer to the query \
    respond with I don't know.
    Write in Korean.

    Query: {query_str}
    Answer: \
    """)
    
    if(config.LLM_TYPE == "openai"):
        llm=OpenAI(temperature=0, model=config.GEN_MODEL)
    else:
        if device=="cpu":
            llm_loader=LLMCPULoader(config.GEN_MODEL)
        else:
            llm_loader=LLMGPULoader(config.GEN_MODEL)
        llm = llm_loader.load_llm()
    response_synthesizer = get_response_synthesizer(
        llm=llm,
        text_qa_template=qa_prompt,
        streaming=True
    )

    rerank = initialize_rerank_model(
        model_name=config.RERANKER_MODEL_NAME, rerank_top_k=config.RERANKER_MODEL_TOP_K,device=device
    ) 

    query_engine = RetrieverQueryEngine(
        retriever=retriever_to_use,
        response_synthesizer=response_synthesizer,
        node_postprocessors=[rerank]
    )

    return retriever_to_use, query_engine
