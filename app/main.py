import uuid
from typing import Dict, List, Union

from fastapi import FastAPI

from app.similarity_scorer import SimilarityScorer
from app.validate_input import get_long_sentence_ids

# define the server url (excl. hostname:port)
# srvurl = "/testapi/v1"
srvurl = ""
similarity_scorer = SimilarityScorer()
# basic information
app = FastAPI(
    title="Simiscore-Semantic ML API",
    descriptions=(
        "Simiscore-Semantic ML API computes similarities between sentences "
        "using a pretrained language model."
    ),
    version="0.1.0",
    openapi_url=f"{srvurl}/openapi.json",
    docs_url=f"{srvurl}/docs",
    redoc_url=f"{srvurl}/redoc",
)


@app.get(f"{srvurl}/")
def get_info() -> dict:
    """Returns basic information about the application"""
    return {"version": app.version, "model": similarity_scorer.model_name}


@app.post(f"{srvurl}/similarities/", response_model=Dict[str, list])
async def compute_similarites(
    query_sents: Union[List[str], Dict[uuid.UUID, str]],
) -> Dict[str, list]:
    """
    Computes similarity score for a sequence of text strings.

    Parameters:
        query_sents: Union[dict, list]
            Sequence of text strings to be processed.
    Returns: Dict[str, list]
            A dictionary containing the sentence ids ('ids') and a matrix
            with the similarity scores ('matrix'). Indices in the matrix
            correspond to the indices in the ids-list.
    """
    if isinstance(query_sents, list):
        query_sents = {uuid.uuid4(): sentence for sentence in query_sents}
    truncated_sent_ids = get_long_sentence_ids(query_sents)
    # compute similarities using SBERT
    response = similarity_scorer.compute_similarity_matrix(query_sents)
    if truncated_sent_ids:
        response["truncated"] = truncated_sent_ids
    return response
