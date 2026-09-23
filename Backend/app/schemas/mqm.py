from typing import List

from pydantic import BaseModel, Field

from app.mqm.taxonomy import MQMCategory, MQMSeverity


class MQMError(BaseModel):
    category: MQMCategory
    error_type: str
    severity: MQMSeverity
    penalty: int
    description: str
    evidence_ids: List[str] = Field(default_factory=list)


class MQMEvaluation(BaseModel):
    errors: List[MQMError] = Field(default_factory=list)
    total_errors: int = 0
    total_penalty: int = 0