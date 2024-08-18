from services.query_service import QueryService
from models.retrievers import initialize_retrievers

def get_query_service() -> QueryService:
    retriever, query_engine = initialize_retrievers()
    return QueryService(retriever=retriever, query_engine=query_engine)
