import os

from langchain import LLMChain
from langchain.chains.chat_vector_db.prompts import CONDENSE_QUESTION_PROMPT
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import Chroma

api_key = os.environ['OPENAI_API_KEY']
persist_directory = 'db'

embedding = OpenAIEmbeddings(api_key=api_key)

# Now we can load the persisted database from disk, and use it as normal.
vectordb = Chroma(persist_directory=persist_directory,
                  embedding_function=embedding)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# retriever = vectordb.as_retriever()
retriever = vectordb.as_retriever()

llm = ChatOpenAI(temperature=0, model='gpt-3.5-turbo')

question_generator = LLMChain(llm=llm, prompt=CONDENSE_QUESTION_PROMPT)
doc_chain = load_qa_with_sources_chain(llm, chain_type="map_reduce")

# create the chain to answer questions
qa_chain = ConversationalRetrievalChain(retriever=retriever,
                                        question_generator=question_generator,
                                        combine_docs_chain=doc_chain,
                                        )

# User interactions and queries
chat_history = []


# # create the chain to answer questions
# qa_chain = RetrievalQA.from_chain_type(llm=OpenAI(openai_api_key=api_key),
#                                        chain_type="stuff",
#                                        retriever=retriever,
#                                        chain_type_kwargs={"prompt": PROMPT},
#                                        return_source_documents=True)


# Cite sources


def process_llm_response(llm_response):
    sources = []
    for source in llm_response["source_documents"]:
        sources.append(source.metadata['source'])
    return sources

# full example
# while True:
#     query = str(input("Enter Query : "))
#     print("after result result")
#     # Query the qa_chain
#     result = qa_chain({"question": query, "chat_history": chat_history})
#     print(result['answer'])
