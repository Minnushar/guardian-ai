from pydantic import BaseModel
from typing import Dict, List, Optional


class RelationshipContext(BaseModel):
    known_friend: bool = False
    long_term_contact: bool = False
    online_only_contact: bool = False


class RiskBreakdown(BaseModel):
    raw_risk: int = 0
    smoothed_risk: int = 0


class AnalysisPayload(BaseModel):
    contact_hash: str
    app: str

    risk_score: int
    tripwire_score: int
    risk_level: str

    behavior_scores: Dict[str, float]
    risk_breakdown: RiskBreakdown

    relationship_context: RelationshipContext

    threat_categories: List[str]

    behavior_summary: str
    summary_confidence: float

    debug: Optional[dict] = {}