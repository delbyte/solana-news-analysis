from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.main import analyze

app = FastAPI()

# Allow frontend (JS) to make requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify your frontend origin like ["http://localhost:5500"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TimeFrame(BaseModel):
    start_date: str  # Format: YYYY-MM-DD
    end_date: str

@app.post("/analyze")
def run_analysis(timeframe: TimeFrame):
    result = analyze(timeframe.start_date, timeframe.end_date)
    return result
