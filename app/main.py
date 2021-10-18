import uuid
from typing import Dict, List, Union

from fastapi import FastAPI

from app.pydantic_models import SentenceInstance

# define the server url (excl. hostname:port)
# srvurl = "/testapi/v1"
srvurl = ""

# basic information
app = FastAPI(
    title="Simiscore-Semantic ML API",
    descriptions=("This is a FastAPI boilerplate. " "Please adjust it to your needs. "),
    version="0.1.0",
    openapi_url=f"{srvurl}/openapi.json",
    docs_url=f"{srvurl}/docs",
    redoc_url=f"{srvurl}/redoc",
)


# specify the endpoints
@app.get(f"{srvurl}/")
def read_root():
    return {"msg": "Hello World"}


@app.get(f"{srvurl}/similarities/")
async def read_items_null():
    return {"instance_id": None}


@app.get(srvurl + "/similarities/{item_id}")
async def read_items(item_id: str, q: str = None):
    return {"instance_id": item_id, "q": q}


@app.post(f"{srvurl}/similarities/")
async def compute_similarites(
    query_sents: Union[List[str], Dict[str, str]],
) -> list:  # return matrix
    if isinstance(query_sents, list):
        query_sents = {uuid.uuid4(): sentence for sentence in query_sents}
    # compute similarities using SBERT
    matrix = {}
    return matrix
