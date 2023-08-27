import os
import time
import openai

from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import Chroma
from langchain import PromptTemplate

# from dotenv import load_dotenv
# load_dotenv()

openai.api_key = os.environ['OPENAI_API_KEY']
persist_directory = 'db'

embedding = OpenAIEmbeddings()

# Now we can load the persisted database from disk, and use it as normal.
vectordb = Chroma(persist_directory=persist_directory,
                  embedding_function=embedding)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# retriever = vectordb.as_retriever()
retriever = vectordb.as_retriever()

llm = ChatOpenAI(temperature=0, model='gpt-3.5-turbo')

template = """/ 
{context}: You are name is virtual lawyer. You are a legal assistant who is very knowledgeable the laws in Hong Kong. You will be 
answering questions from Hong Kong citizens about their legal problems. The questions you receive will span from 
different legal areas such as, but limited to, work injury, road accident claim, divorce, criminal,etc. As a chatbot, 
your main objective is to assist users by generating answers based on the laws and past cases of Hong Kong. Your 
answer must be accurate and simple to understand. Do not use too many legal jargons that normal citizens might find 
it hard to comprehend. Talk to the user with the language he or she is using. Whenever you are not 100% sure about 
your answer or you don't know how to answer, advise the user to contact a real lawyer for consultation.

Question: {question}
Answer: 
"""

PROMPT = PromptTemplate(template=template, input_variables=["context", 'question'])

qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff",
                                       retriever=retriever, return_source_documents=True,
                                       chain_type_kwargs={"prompt": PROMPT})

# full example
# while True:
#     query = input("\nEnter a query: ")
#     if query == "exit":
#         break
#     if query.strip() == "":
#         continue
#
#     # Get the answer from the chain
#     start = time.time()
#     res = qa_chain(query)
#     answer, docs = res['result'], res['source_documents']
#     end = time.time()
#
#     # Print the result
#     print("\n\n> Question:")
#     print(query)
#     print(f"\n> Answer (took {round(end - start, 2)} s.):")
#     print(answer)
#
#     # Print the relevant sources used for the answer
#     for document in docs:
#         print("\n> " + document.metadata["source"] + ":")
#         print(document.page_content)
