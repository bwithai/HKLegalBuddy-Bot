import os

os.environ["OPENAI_API_KEY"] = "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"

from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, PyPDFDirectoryLoader

# Load and process the text files
loader = PyPDFLoader('Avori project data.pdf')
# loader = DirectoryLoader('./new_articles/', glob="./*.pdf", loader_cls=PyPDFLoader)

documents = loader.load()

# splitting the text into
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
texts = text_splitter.split_documents(documents)

# Embed and store the texts
# Supplying a persist_directory will store the embeddings on disk
persist_directory = 'db'

# here we are using OpenAI embeddings but in future we will swap out to local embeddings
embedding = OpenAIEmbeddings()

# create simple ids
ids = [str(i) for i in range(1, len(texts) + 1)]

vectordb = Chroma.from_documents(documents=texts,
                                 embedding=embedding,
                                 persist_directory=persist_directory,
                                 ids=ids
                                 )

# persist the db to disk
vectordb.persist()
vectordb = None