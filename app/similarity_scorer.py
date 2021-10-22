from typing import Dict
import torch

from sentence_transformers import SentenceTransformer, util


class SimilarityScorer:
    def __init__(self, model="distiluse-base-multilingual-cased-v1"):
        self.model = SentenceTransformer(model)

    def compute_similarity_matrix(self, query_sents: Dict[str, str]):
        ids = list(query_sents.keys())
        query_embeddings = self.model.encode(list(query_sents.values()))
        similarity_matrix = []

        for i, id in enumerate(ids):
            similarity_matrix.append(
                util.cos_sim(query_embeddings[i], query_embeddings).tolist()
            )
        return {"ids": ids, "matrix": similarity_matrix}
