import joblib
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np

# 1. Initialize FastAPI and Load Model
app = FastAPI(title="FinGuard: AI Social Credit Analyzer")

try:
    model = joblib.load('advanced_social_risk_model.pkl')
    print("✅ Model loaded successfully.")
except Exception as e:
    print(f"❌ Error loading model: {e}")

# 2. Define the Input Schema
class UserProfile(BaseModel):
    name: str
    avg_tenure_months: float
    total_exp_months: float
    recent_hops: int
    network_score: float
    sentiment: float
    consistency_index: float
@app.get("/")
def read_root():
    """
    This is the landing page of your API. 
    It tells the user the system is online and where to find the docs.
    """
    return {
        "project": "FinGuard AI: Social Credit Risk Analyzer",
        "status": "Online",
        "version": "2.0.0",
        "api_documentation": "/docs",
        "message": "Send a POST request to /analyze to get a credit risk report."
    }
# 3. The Prediction Endpoint
@app.post("/analyze")
async def analyze_risk(profile: UserProfile):
    # Prepare features for the model (must match Colab order)
    features = np.array([[
        profile.avg_tenure_months,
        profile.total_exp_months,
        profile.recent_hops,
        profile.network_score,
        profile.sentiment,
        profile.consistency_index
    ]])

    # Generate Prediction and Probability
    risk_probability = model.predict_proba(features)[0][1]
    prediction = int(model.predict(features)[0])

    # 4. Agentic Explanation Logic (Simulating LLM Reasoning)
    if risk_probability > 0.7:
        summary = "High Risk: Significant behavioral instability detected."
    elif risk_probability > 0.3:
        summary = "Moderate Risk: Some inconsistent patterns; manual review suggested."
    else:
        summary = "Low Risk: Profile demonstrates high professional stability."

    # Highlight specific flags
    flags = []
    if profile.recent_hops > 2:
        flags.append("High job-hopping frequency in short period.")
    if profile.sentiment < -0.2:
        flags.append("Negative professional sentiment detected in public profiles.")

    return {
        "candidate_name": profile.name,
        "reliability_score": f"{round((1 - risk_probability) * 100, 2)}%",
        "risk_category": "RED" if prediction == 1 else "GREEN",
        "ai_narrative": summary,
        "behavioral_flags": flags if flags else "No major flags detected."
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)