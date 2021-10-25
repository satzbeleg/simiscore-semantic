import uuid
from typing import Dict, List, Union

from fastapi import FastAPI

from app.similarity_scorer import SimilarityScorer

# define the server url (excl. hostname:port)
# srvurl = "/testapi/v1"
srvurl = ""
similarity_scorer = SimilarityScorer()
# basic information
app = FastAPI(
    title="Simiscore-Semantic ML API",
    descriptions=(
        "This is a FastAPI boilerplate. " "Please adjust it to your needs. "
    ),
    version="0.1.0",
    openapi_url=f"{srvurl}/openapi.json",
    docs_url=f"{srvurl}/docs",
    redoc_url=f"{srvurl}/redoc",
)


@app.get(f"{srvurl}/")
def get_info():
    return {"version": app.version, "model": similarity_scorer.model_name}


@app.post(f"{srvurl}/similarities/", response_model=Dict[str, list])
async def compute_similarites(
    query_sents: Union[List[str], Dict[uuid.UUID, str]],
) -> Dict[str, list]:
    if isinstance(query_sents, list):
        query_sents = {uuid.uuid4(): sentence for sentence in query_sents}
    # compute similarities using SBERT
    response = similarity_scorer.compute_similarity_matrix(query_sents)
    return response
