import os
import shutil
import time

from typing import List

from fastapi import FastAPI, UploadFile
from starlette.middleware.cors import CORSMiddleware

from ingest import ingestion
from retrieve_QA import qa_chain
from schemas import QueryResponse

# app
app = FastAPI(
    title='Meet HKLegalBuddy – Your Friendly Guide to Hong Kong Law!',
    version='1.0.0',
    redoc_url='/api/v1/docs'
)

# cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.post("/api/v1/load-and-store")
async def load_and_store_pdf_files(files: List[UploadFile]) -> dict[str, str]:
    if not files:
        return {
            "status": 400,
            "result": "No upload file sent"
        }

    dist_path = os.path.join(os.getcwd(), 'pdf')
    if not os.path.exists(dist_path):
        os.makedirs(dist_path)

    # Iterate over each uploaded file
    for file in files:
        # move file to pdf directory
        with open(f"{file.filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        new_file_src = f"{file.filename}"
        store_new_file_at_dist = f"{dist_path}"
        shutil.move(new_file_src, store_new_file_at_dist)

    return {
        'status': 200,
        "result": "Files uploaded and stored successfully",
    }


@app.get("/api/v1/list-pdf-files")
async def list_pdf_files():
    pdf_directory = 'pdf/'
    dist_path = os.path.join(os.getcwd(), pdf_directory)
    if not os.path.exists(dist_path):
        return {
            "status": 400,
            "result": "pdf directory is not found"
        }

    # List all files in the directory and filter PDF files
    pdf_files = [filename for filename in os.listdir(pdf_directory) if filename.endswith('.pdf')]

    return {
        "status": 200,
        "result": pdf_files
    }


@app.get("/api/v1/vectorize-pdfs")
async def vectorize_pdfs():
    pdf_directory = 'pdf/'

    dist_path = os.path.join(os.getcwd(), pdf_directory)
    if not os.path.exists(dist_path):
        return {
            "status": 400,
            "result": "upload pdf first"
        }

    try:
        ingestion()
    except Exception as e:
        return {
            "status": 500,
            "result": f"An error occurred: {e}"
        }

    return {
        'status': 200,
        "result": "Vectorization is Done, You can now Meet HKLegalBuddy – Your Friendly Guide to Hong Kong Law! "
    }


@app.post("/api/v1/query")
async def request_query(response: QueryResponse):
    include_resources = response.include_resources
    start = time.time()
    res = qa_chain(response.query)
    answer, docs = res['result'], res['source_documents']
    end = time.time()

    # Prepare the response string
    response_string = f"> Answer (took {round(end - start, 2)} s.):\n\n{answer}"

    # Add the relevant sources used for the answer
    if include_resources:
        for document in docs:
            response_string += f"\n\n> {document.metadata['source']}:\n{document.page_content}"

    return {
        "status": 200,
        "query": response.query,
        "result": response_string
    }


@app.delete("/api/v1/delete-test-data")
async def delete_test_data():
    status = False
    dist_path = os.path.join(os.getcwd(), 'pdf')
    if os.path.exists(dist_path):
        shutil.rmtree(dist_path)
        status = True
    else:
        return {
            "status": 400,
            "result": "pdf directory not found"
        }

    if status:
        return {
            "status": 200,
            "result": "pdf directory removed"
        }
