from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class ConceptStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    MASTERED = "mastered"
    NEEDS_REVIEW = "needs_review"


class StruggleSignals(BaseModel):
    help_requests: int = 0
    error_count: int = 0
    confusion_indicators: int = 0


class StudentProgress(BaseModel):
    status: ConceptStatus
    mastery_level: float = Field(ge=0.0, le=1.0)
    attempts: int = 0
    last_interaction: Optional[datetime] = None
    struggle_signals: StruggleSignals


class CurriculumConcept(BaseModel):
    name: str
    description: str
    prerequisites: List[str] = []
    difficulty: int = Field(ge=1, le=5)
    key_concepts: List[str]
    student_progress: StudentProgress


class StudentProfile(BaseModel):
    interests: List[str] = []
    learning_velocity: float = 1.0
    active_concepts: List[str] = []
    preferred_examples: List[str] = []


class CurriculumState(BaseModel):
    curriculum: Dict[str, CurriculumConcept]
    student_profile: StudentProfile
    metadata: Dict

    @classmethod
    def from_json(cls, json_str: str):
        return cls.model_validate_json(json_str)

    def to_json_str(self) -> str:
        return self.model_dump_json(indent=2)
