from pydantic import BaseModel
from typing import Optional

class TranslationRequest(BaseModel):
    source: str
    hypothesis: str
    reference: Optional[str] = None

    source_lang: Optional[str] = None
    target_lang: Optional[str] = None
    domain: Optional[str] = None