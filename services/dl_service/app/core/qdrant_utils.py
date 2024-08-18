from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import ResponseHandlingException
from qdrant_client.models import Distance, PointStruct, VectorParams
from uuid import uuid4

def create_collection_if_not_exists(client, collection_name, embed_dimensional):
    try:
        collections = client.get_collections()
        existing_collection_names = [col.name for col in collections.collections]
        
        if collection_name in existing_collection_names:
            # 컬렉션이 존재하면 삭제
            client.delete_collection(collection_name=collection_name)
            print(f"Collection '{collection_name}' deleted.")
        
        # 새 컬렉션 생성
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=embed_dimensional, distance=Distance.COSINE)
        )
        print(f"Collection '{collection_name}' created.")
        
    except ResponseHandlingException as e:
        print(f"Error checking, deleting, or creating collection: {e}")



#384
def upsert_chunked_nodes(nodes, client, collection_name,embed_model):
    print(nodes[:4])
    """
    Process and upsert chunked metadata into Qdrant.

    Args:
    ----
    data (list): The list of document chunks.
    client (QdrantClient): The Qdrant client instance.
    collection_name (str): The name of the collection.
    embed_model (FastEmbedEmbedding): The Embedding Model
    """
    chunked_nodes = []

    for item in nodes:
        qdrant_id = str(uuid4())
        document_id = item.id_
        code_text = item.text
        source = item.metadata["file_path"]
        file_name = item.metadata["file_name"]
        page=item.metadata["page_label"]
        creation_date=item.metadata["creation_date"]
        modified_date=item.metadata["last_modified_date"]       

        content_vector = embed_model.get_text_embedding(code_text)

        payload = {
            "text": code_text,
            "document_id": document_id,
            "metadata": {
                            "qdrant_id": qdrant_id,
                            "source": source,
                            "file_name": file_name,
                            "page":page,
                            "creation_date":creation_date,
                            "modified_date":modified_date
                            }
                }


        metadata = PointStruct(id=qdrant_id, vector=content_vector, payload=payload)

        chunked_nodes.append(metadata)
    
    if chunked_nodes:
        client.upsert(
            collection_name=collection_name,
            wait=True,
            points=chunked_nodes
        )

    print(f"{len(chunked_nodes)} Chunked metadata upserted.")
    