from models.retrievers import RetrieverQueryEngine, VectorIndexRetriever

class QueryService:
    def __init__(self, retriever: VectorIndexRetriever, query_engine: RetrieverQueryEngine):
        self.retriever = retriever
        self.query_engine = query_engine

    def process_query(self, query: str) -> str:

        response = self.query_engine.query(query)

        return response
