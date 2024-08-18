from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks,Request
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
from fastapi.responses import JSONResponse
import logging
from utils import (prepare_db,check_db_healthy,commit_only_api_log_to_db)
from pydantic import BaseModel
import time

FORMATTER = logging.Formatter(
    '%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)-3d | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setFormatter(FORMATTER)
logger.addHandler(ch)

fh = logging.FileHandler('logs.log')  
fh.setFormatter(FORMATTER)
logger.addHandler(fh)

# prepare database
prepare_db()

class Message(BaseModel):
    message: str


router = APIRouter()

@router.get("/health_check",response_model=Message, responses={404: {"model": Message}})
async def health_check():
    resp_code = 200
    resp_message = "Service is ready and healthy."
    try:
        check_db_healthy()
    except:
        resp_code = 404
        resp_message = "DB is not functional. Service is unhealthy."
    return JSONResponse(status_code=resp_code, content={"message": resp_message})
                        
@router.post("/query")
async def query_vector_store(
    background_tasks: BackgroundTasks,
    request: QueryRequest,
    raw_request: Request,
    query_service: QueryService = Depends(get_query_service),
):
    start_time = time.time()
    logger.info('query api')
  
    try:
        time_spent = round(time.time() - start_time, 4)
        resp_code = 200
        resp_message = "RAG Query the successfully"
        background_tasks.add_task(commit_only_api_log_to_db, raw_request, resp_code, resp_message, time_spent)
        
        async def generate_response():
            streaming_response = query_service.process_query(request.query)

            if not streaming_response:
                raise HTTPException(status_code=404, detail="No response found")

            for text in streaming_response.response_gen:
                yield text  
                await asyncio.sleep(0.1)

        return StreamingResponse(generate_response(), media_type="text/plain")

    except Exception as e:
        logger.error(f'Loading model failed with exception:\n {e}')
        time_spent = round(time.time() - start_time, 4)
        resp_code = 404
        resp_message = "RAG Query failed"
        background_tasks.add_task(commit_only_api_log_to_db, raw_request, resp_code, resp_message, time_spent)
        return JSONResponse(status_code=resp_code, content={"message": resp_message})
    


@router.post("/process_documents/")
async def process_documents(    request: Request, background_tasks: BackgroundTasks):
    start_time = time.time()
    try:
        logger.info('process_documents api')
        client = QdrantClient(url=config.QDRANT_URL, prefer_grpc=True)
        documents = load_documents_from_directory(directory_path=config.DATAPATH)
        
        # Split the documents into nodes
        nodes = split_documents_into_nodes(documents=documents, chunk_size=config.CHUNK_SIZE, chunk_overlap=config.CHUNK_OVERLAP)
        embed_model = initialize_embedding_model(model_name=config.EMBED_MODEL_NAME)
        
        # Ensure the Qdrant collection exists
        create_collection_if_not_exists(client=client, collection_name=config.COLLECTION_NAME, embed_dimensional=config.EMBED_DIMENSIONAL)
        
        # Upsert the nodes into Qdrant
        upsert_chunked_nodes(nodes=nodes, client=client, collection_name=config.COLLECTION_NAME, embed_model=embed_model)
        
        time_spent = round(time.time() - start_time, 4)
        resp_code = 200
        resp_message = "Documents processed and uploaded successfully"
        background_tasks.add_task(commit_only_api_log_to_db, request, resp_code, resp_message, time_spent)
        
        return {"message": resp_message}
        
    except Exception as e:
        logger.error(f'Processing documents failed with exception:\n {e}')
        time_spent = round(time.time() - start_time, 4)
        resp_code = 500
        resp_message = "Processing documents failed"
        background_tasks.add_task(commit_only_api_log_to_db, request, resp_code, resp_message, time_spent)
        raise HTTPException(status_code=resp_code, detail=str(e))
