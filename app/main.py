from operator import index
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from elasticsearch import Elasticsearch
from pydantic import BaseModel
from fastapi import FastAPI, Request
import warnings
warnings.filterwarnings("ignore")

templates = Jinja2Templates(directory="./templates")
app = FastAPI(title="Data API")
es = Elasticsearch({"scheme": "http", "host": "host.docker.internal", "port": 9200},  max_retries=30,
                   retry_on_timeout=True, request_timeout=30)

if not es.ping():
    raise ValueError("Connection failed")
else:
    print("Successfully connected to Elasticsearch.")

index_name = "movies"

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])


@app.get('/health', status_code=200, summary="Returns HC Page.", tags=["hc"])
async def home():
    return {"message": "Still Alive"}


@app.get("/", status_code=200, summary="Returns Search Page.", tags=["search"])
def root(request: Request):
    result = "Type a number"
    return templates.TemplateResponse('home.html', context={'request': request, 'result': result})


@app.get('/match', status_code=200, summary="Returns Matches.", tags=["search"])
async def match(term: str):
    body = {
        "query": {
            "match": {
                "movies": {
                    "query": term,
                    "fuzziness": "auto"
                }
            }
        }
    }
    res = es.search(index=index_name, body=body)
    if res["hits"]["total"]["value"] > 0:
        f = []
        for i in res["hits"]["hits"][0:-1]:
            f.append(i["_source"]["movies"])
        return f
    else:
        return "Sonuç Bulunamadı"
