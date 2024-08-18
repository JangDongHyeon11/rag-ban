from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.postprocessor import SentenceTransformerRerank
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
def initialize_embedding_model(model_name):
    return HuggingFaceEmbedding(model_name=model_name)

def initialize_rerank_model(model_name,rerank_top_k):
    return SentenceTransformerRerank(
    model=model_name, top_n=rerank_top_k
)

