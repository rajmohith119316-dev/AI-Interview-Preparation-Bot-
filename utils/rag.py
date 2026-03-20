from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

def load_data(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def create_vector_db(text):
    splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=50)
    chunks = splitter.split_text(text)

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_db = FAISS.from_texts(chunks, embeddings)

    return vector_db

def search_docs(vector_db, query):
    return vector_db.similarity_search(query, k=2)