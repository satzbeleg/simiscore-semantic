import uuid
from typing import Dict

import sentence_transformers as sbert


class SimilarityScorer:
    def __init__(
        self,
        model: str = "paraphrase-multilingual-MiniLM-L12-v2",
    ) -> None:
        """Computes similarity scores between text strings.
        Attributes:
            model: sbert.SentenceTransformer
                Instance of pretrained language model.
            model_name: str, optional
                Name of the model to use. Default is model
                'paraphrase-multilingual-MiniLM-L12-v2' from
                sentence_transformers.

        """
        self.model = sbert.SentenceTransformer(model)
        self.model_name = model

    def compute_similarity_matrix(
        self, query_sents: Dict[uuid.UUID, str]
    ) -> Dict[str, list]:

        """
        Compute similarity scores for sequence of text strings.

        Parameters:
            query_sents: Union[dict, list]
                Sequence of text strings to be processed.
        Returns: Dict[str, list]
            A dictionary storing sentence ids and the similarity matrix.
        """
        ids = list(query_sents.keys())
        query_embeddings = self.model.encode(list(query_sents.values()))
        similarity_matrix = sbert.util.cos_sim(
            query_embeddings, query_embeddings
        ).tolist()
        return {"ids": ids, "matrix": similarity_matrix}
