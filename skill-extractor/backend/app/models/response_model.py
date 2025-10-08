from pydantic import BaseModel
from typing import List


class ExtractionResponse(BaseModel):
    skills:List[str]
    experience: str
