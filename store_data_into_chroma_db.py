import os

from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFDirectoryLoader, DirectoryLoader, PyPDFLoader
import openai

from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.environ['OPENAI_API_KEY']


def store_data_in_chromadb(file_path):
    # Load and process the text file
    loader = PyPDFLoader(file_path)
    # loader = PyPDFDirectoryLoader(path='pdf/')

    documents = loader.load()

    # splitting the text into
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_documents(documents)

    # Embed and store the texts
    # Supplying a persist_directory will store the embeddings on disk
    persist_directory = 'db'

    # here we are using OpenAI embeddings but in future we will swap out to local embeddings
    embedding = OpenAIEmbeddings()

    # # Create simple ids
    ids = [str(i) for i, _ in enumerate(texts, start=1)]

    print("Length of texts:", len(texts))
    print("Length of ids:", len(ids))

    vectordb = Chroma.from_documents(documents=texts,
                                     embedding=embedding,
                                     persist_directory=persist_directory,
                                     ids=ids
                                     )

    # persist the db to disk
    vectordb.persist()
    vectordb = None
    return True