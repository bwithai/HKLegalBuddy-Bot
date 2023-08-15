import os
from fastapi import FastAPI, Request, Response
from starlette.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from backend.core import run_llm

from dotenv import load_dotenv
load_dotenv()


app = FastAPI()
templates = Jinja2Templates(directory="templates")
# Define a static directory to serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")


def root_dir():
    return os.path.abspath(os.path.dirname(__file__))


def get_file(filename):
    try:
        src = os.path.join(root_dir(), filename)
        return open(src).read()
    except IOError as exc:
        return str(exc)


@app.get('/')
async def metrics():
    content = get_file('templates/index.html')
    return Response(content, media_type="text/html")


@app.get('/{prompt}')
async def index(prompt: str):
    result = run_llm(query=prompt)
    print(result)
    return result

# @app.get("/train-model")
# async def train_model():
#     result = ingestion()
#     if result:
#         return {
#             "status": 200,
#             "message": "****** Added to Pinecone vectorstore vectors"
#         }
#
#     return {
#         "status": 101,
#         "message": "something happen with ingestion vectorization"
#     }
