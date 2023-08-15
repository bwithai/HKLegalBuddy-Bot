import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import Pinecone
import pinecone
from dotenv import load_dotenv
load_dotenv()

pinecone.init(
    api_key=os.environ['PIN_CONE_API_KEY'],
    environment='asia-southeast1-gcp-free'
)
api_key = os.environ["OPENAI_API_KEY"]


def run_llm(query: str):
    embeddings = OpenAIEmbeddings(api_key=api_key)
    doc_search = Pinecone.from_existing_index(index_name="getmakte-index", embedding=embeddings)
    chat = ChatOpenAI(verbose=True, temperature=0)
    qa = RetrievalQA.from_chain_type(llm=chat, chain_type="stuff", retriever=doc_search.as_retriever())
    return qa({"query": query})
