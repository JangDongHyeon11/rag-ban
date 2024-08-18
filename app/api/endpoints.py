from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from models.query_model import QueryRequest
from services.query_service import QueryService
from core.dependencies import get_query_service
import asyncio
from core.config import config
from core.document_processing import split_documents_into_nodes
from core.qdrant_utils import create_collection_if_not_exists, upsert_chunked_nodes
from readers.document_reader import load_documents_from_directory
from AI.model import initialize_embedding_model
from qdrant_client import QdrantClient

router = APIRouter()

@router.post("/query")
async def query_vector_store(
    request: QueryRequest,
    query_service: QueryService = Depends(get_query_service),

):
    async def generate_response():
        streaming_response = query_service.process_query(request.query)

        if not streaming_response:
            raise HTTPException(status_code=404, detail="No response found")

        for text in streaming_response.response_gen:
            yield text  
            await asyncio.sleep(0.01)

    return StreamingResponse(generate_response(), media_type="text/plain")

@router.post("/process_documents/")
async def process_documents():
    try:
        client = QdrantClient(url=config.QDRANT_URL,prefer_grpc=True)
        documents = load_documents_from_directory(directory_path=config.DATAPATH)
        
        # Split the documents into nodes
        nodes = split_documents_into_nodes(documents=documents, chunk_size=config.CHUNK_SIZE, chunk_overlap=config.CHUNK_OVERLAP)
        embed_model=initialize_embedding_model(model_name=config.EMBED_MODEL_NAME)
        # Ensure the Qdrant collection exists
        create_collection_if_not_exists(client=client, collection_name=config.COLLECTION_NAME, embed_dimensional=config.EMBED_DIMENSIONAL)
        
        # Upsert the nodes into Qdrant
        upsert_chunked_nodes(nodes=nodes, client=client, collection_name=config.COLLECTION_NAME, embed_model=embed_model)
        return {"message": "Documents processed and uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

