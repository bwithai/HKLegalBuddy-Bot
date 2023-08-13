import os

os.environ["OPENAI_API_KEY"] = "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"

from langchain import OpenAI
from langchain.chains import RetrievalQA
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

persist_directory = 'db'

embedding = OpenAIEmbeddings()

# Now we can load the persisted database from disk, and use it as normal.
vectordb = Chroma(persist_directory=persist_directory,
                  embedding_function=embedding)

# retriever = vectordb.as_retriever()
retriever = vectordb.as_retriever(search_kwargs={"k": 1})

# create the chain to answer questions
qa_chain = RetrievalQA.from_chain_type(llm=OpenAI(),
                                       chain_type="stuff",
                                       retriever=retriever,
                                       return_source_documents=True)


# Cite sources
def process_llm_response(llm_response):
    print(llm_response['result'])
    print('\n\nSources:')
    for source in llm_response["source_documents"]:
        print(source.metadata['source'])


# full example
while True:
    query = str(input("Enter Query : "))
    llm_response = qa_chain(query)
    print(llm_response)
    # process_llm_response(llm_response)

# # break it down
# query = "What is the news about Pando?"
# llm_response = qa_chain(query)
# # process_llm_response(llm_response)
# print(llm_response)
