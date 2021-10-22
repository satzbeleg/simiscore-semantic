from typing import Dict
import uuid

from sentence_transformers import SentenceTransformer, util


class SimilarityScorer:
    def __init__(self, model: str = "distiluse-base-multilingual-cased-v1") -> None:
        self.model = SentenceTransformer(model)

    def compute_similarity_matrix(
        self, query_sents: Dict[uuid.UUID, str]
    ) -> Dict[str, list]:
        ids = list(query_sents.keys())
        query_embeddings = self.model.encode(list(query_sents.values()))
        similarity_matrix = []

        for i, idx in enumerate(ids):
            similarity_matrix.append(
                util.cos_sim(query_embeddings[i], query_embeddings).tolist()
            )
        return {"ids": ids, "matrix": similarity_matrix}
