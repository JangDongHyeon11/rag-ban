from llama_index.core.node_parser import SentenceSplitter

def split_documents_into_nodes(documents,chunk_size=400,chunk_overlap=0):
    try:
        splitter = SentenceSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        nodes = splitter.get_nodes_from_documents(documents)
        return nodes
    except Exception as e:
        print(f"Error splitting documents into nodes: {e}")
        return []
