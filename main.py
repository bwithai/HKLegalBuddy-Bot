import os
import shutil
from typing import List, Any

from fastapi import FastAPI, UploadFile
from starlette.middleware.cors import CORSMiddleware
from store_data_into_chroma_db import store_data_in_chromadb
from retrieve_QA import qa_chain, process_llm_response
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
        return {"message": "No upload file sent"}

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
        "message": "Files uploaded and stored successfully",
    }


@app.get("/api/v1/vectorize-pdfs")
async def vectorize_pdfs():
    status = store_data_in_chromadb()
    if status:
        return {
            'status': 200,
            "message": "Vectorization is Done, You can now Meet HKLegalBuddy – Your Friendly Guide to Hong Kong Law! "
        }


@app.post("/api/v1/query")
async def request_query(response: QueryResponse):
    llm_response = qa_chain(response.query)
    sources = process_llm_response(llm_response)

    result: dict[str, str | Any] = {
        'status': 200,
        "query": llm_response["query"],
        "result": llm_response["result"],
    }

    print(result)
    return result

@app.delete("/api/v1/delete-test-data")
async def delete_test_data():
    status = False
    dist_path = os.path.join(os.getcwd(), 'pdf')
    if os.path.exists(dist_path):
        shutil.rmtree(dist_path)
        status = True
    else:
        return {
            "status": 101,
            "message": "pdf directory not found"
        }

    if status:
        return {
            "status": 200,
            "message": "pdf directory removed"
        }
