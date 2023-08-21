import os
import logging
import pinecone
from dotenv import load_dotenv
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.pinecone import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

open_api_key = os.environ.get("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_env = os.getenv("PINECONE_ENV")
pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")

# Validate environment variables
if not all([open_api_key, pinecone_api_key, pinecone_env, pinecone_index_name]):
    logger.error("Missing required environment variables.")
    exit(1)

def init_services():
    try:
        openai_embeddings = OpenAIEmbeddings(openai_api_key=open_api_key)
        pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)
        return openai_embeddings
    except Exception as e:
        logger.error(f"Failed to initialize OpenAIEmbeddings or Pinecone: {e}")
        exit(1)

def load_docs(directory_path):
    try:
        loader = DirectoryLoader(directory_path)
        documents = loader.load()
        return documents
    except Exception as e:
        logger.error(f"Failed to load documents: {e}")
        return []

def split_docs(documents, chunk_size=500, chunk_overlap=20):
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        docs = text_splitter.split_documents(documents)
        return docs
    except Exception as e:
        logger.error(f"Failed to split documents: {e}")
        return []

def store_embeddings_in_pinecone(docs, openai_embeddings):
    try:
        Pinecone.from_documents(docs, openai_embeddings, index_name=pinecone_index_name)
    except Exception as e:
        logger.error(f"Failed to store embeddings in Pinecone: {e}")

def main():
    openai_embeddings = init_services()
    documents = load_docs("data/")
    if not documents:
        logger.error("No documents loaded.")
        exit(1)
    docs = split_docs(documents)
    if not docs:
        logger.error("No documents split.")
        exit(1)
    store_embeddings_in_pinecone(docs, openai_embeddings)

if __name__ == "__main__":
    main()
