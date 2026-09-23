from typing import List

from pydantic import BaseModel, Field

from app.mqm.taxonomy import MQMCategory, MQMSeverity


class MQMErrorLLM(BaseModel):
    category: MQMCategory
    error_type: str
    severity: MQMSeverity
    description: str
    evidence_ids: List[str] = Field(default_factory=list)


class MQMClassificationResult(BaseModel):
    errors: List[MQMErrorLLM] = Field(default_factory=list)