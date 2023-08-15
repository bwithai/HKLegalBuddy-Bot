import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
import pinecone
from langchain.document_loaders import DirectoryLoader

pinecone_api_key = os.environ['PIN_CONE_API_KEY']

pinecone.init(
    api_key=pinecone_api_key,
    environment='asia-southeast1-gcp-free'
)
loader = DirectoryLoader("/Users/saeedanwar/Desktop/upwork_projects/pakistan duabi school /v2/data")
api_key = os.environ["OPENAI_API_KEY"]


def ingestion() -> bool:
    raw_documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=100, separators=["\n\n", "\n", " ", ""])
    documents = text_splitter.split_documents(documents=raw_documents)
    print(f"Splitted into {len(documents)} chunks")
    embeddings = OpenAIEmbeddings(api_key=api_key)
    Pinecone.from_documents(documents, embeddings, index_name="getmakte-index")

    return True
