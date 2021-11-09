import uuid
from typing import Dict


def get_long_sentence_ids(query_sents: Dict[uuid.UUID, str]) -> list:
    # for 128 word pieces, the average sentences length of news and web corpora
    # was 480.5, adding 18.5 characters for whitespace, the limit is 500
    return [id for id, sent in query_sents.items() if len(sent) >= 500]
