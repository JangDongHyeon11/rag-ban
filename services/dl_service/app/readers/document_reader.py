from llama_index.core import SimpleDirectoryReader

def load_documents_from_directory(directory_path, required_exts=".pdf"):
    reader = SimpleDirectoryReader(input_dir=directory_path, required_exts=required_exts)
    return reader.load_data()
