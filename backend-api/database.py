from typing import List
from models import AnalysisPayload

# In-memory storage (prototype)
analysis_history: List[AnalysisPayload] = []


def save_analysis(payload: AnalysisPayload):
    analysis_history.append(payload)


def get_latest_analysis():
    if analysis_history:
        return analysis_history[-1]
    return None


def get_analysis_history():
    return analysis_history