import os

from langchain import OpenAI, PromptTemplate
from langchain.chains import RetrievalQA
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

api_key = os.environ['OPENAI_API_KEY']
persist_directory = 'db'

embedding = OpenAIEmbeddings(api_key=api_key)

# Now we can load the persisted database from disk, and use it as normal.
vectordb = Chroma(persist_directory=persist_directory,
                  embedding_function=embedding)

# retriever = vectordb.as_retriever()
retriever = vectordb.as_retriever(search_kwargs={"k": 1})

# Pass in a custom prompt to RetrievalQA that includes a context section:
template = """/ 
{context}: You are a legal assistant who is very knowledgeable the laws in Hong Kong. You will be 
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

# create the chain to answer questions
qa_chain = RetrievalQA.from_chain_type(llm=OpenAI(openai_api_key=api_key),
                                       chain_type="stuff",
                                       retriever=retriever,
                                       chain_type_kwargs={"prompt": PROMPT},
                                       return_source_documents=True)


# Cite sources


def process_llm_response(llm_response):
    sources = []
    for source in llm_response["source_documents"]:
        sources.append(source.metadata['source'])
    return sources

# full example
# while True:
#     query = str(input("Enter Query : "))
#     llm_response = qa_chain(query)
#     sources = process_llm_response(llm_response)
#     # Create the formatted result string
#     formatted_result = "{}\n\nSources:\n{}".format(llm_response['result'], '\n'.join(sources))
#
#     result = {
#         'query': llm_response['query'],
#         'result': formatted_result
#     }
#     print(result['result'])
