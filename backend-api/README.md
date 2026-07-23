# Guardian AI Backend API

This FastAPI service acts as the communication layer between the Local Tripwire AI engine and the Streamlit dashboard.

## Features

- Receives AI analysis from the Local Tripwire AI
- Stores analysis history
- Provides latest analysis
- Exposes REST APIs for the dashboard

## Endpoints

POST /history/analyse

Receives an analysis payload.

GET /history/latest

Returns the latest analysis.

GET /history/all

Returns the complete analysis history.

## Run

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```