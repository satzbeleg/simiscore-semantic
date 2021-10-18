from typing import Optional

from pydantic import BaseModel


class SentenceInstance(BaseModel):
    instance_id: str
    sentence: Optional[str]
