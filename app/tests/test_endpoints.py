from fastapi.testclient import TestClient
import yaml
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

client = TestClient(app)

def load_config():
    """
    Load the current configuration from the config.yaml file.
    """
    config_path = "config/config.yaml"  # config.yaml 파일 경로
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config

def save_config(config):
    """
    Save the configuration back to the config.yaml file.
    """
    config_path = "config/config.yaml"  # config.yaml 파일 경로
    with open(config_path, "w") as file:
        yaml.safe_dump(config, file)

def test_process_documents_valid():
    """
    Test the process documents endpoint ("/process_documents/").
    """
    # Load the current config and save the original collection_name
    config = load_config()
    original_collection_name = config['retriever']['collection_name']
    
    try:
        # Update the collection_name for the test
        new_collection_name = "test_collection"
        config['retriever']['collection_name'] = new_collection_name
        save_config(config)
        
        # Execute the test
        response = client.post("/process_documents/")
        assert response.status_code == 200
  
    
    finally:
        # Restore the original collection_name after the test
        config['retriever']['collection_name'] = original_collection_name
        save_config(config)
        

def test_query_vector_store_valid():
    """
    Test the vector store query endpoint ("/query/").

    Checks that the endpoint returns a valid response for a valid query payload.
    """
    config = load_config()
    original_collection_name = config['retriever']['collection_name']
    
    try:
        # Update the collection_name for the test
        new_collection_name = "test_collection"
        config['retriever']['collection_name'] = new_collection_name
        save_config(config)
        valid_payload = {"query": "Enter query string."}
        response = client.post("/query/", json=valid_payload)
        assert response.status_code == 200
        
    finally:
        # Restore the original collection_name after the test
        config['retriever']['collection_name'] = original_collection_name
        save_config(config)
        


