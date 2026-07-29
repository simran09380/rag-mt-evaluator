from pydantic import BaseModel


class TranslationRequest(BaseModel):
    source: str
    hypothesis: str
    reference: str
    domain: str