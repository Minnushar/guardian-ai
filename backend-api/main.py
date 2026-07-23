from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import AnalysisPayload
from database import (
    save_analysis,
    get_latest_analysis,
    get_analysis_history
)

app = FastAPI(title="Guardian AI Backend API")

# Allow dashboard and Android app to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Guardian AI Backend is running."
    }


@app.post("/history/analyse")
def analyse(payload: AnalysisPayload):
    save_analysis(payload)

    return {
        "message": "Analysis received successfully.",
        "risk_score": payload.risk_score,
        "risk_level": payload.risk_level
    }


@app.get("/history/latest")
def latest():

    latest_record = get_latest_analysis()

    if latest_record is None:
        return {
            "message": "No analysis available."
        }

    return latest_record


@app.get("/history/all")
def history():
    return get_analysis_history()