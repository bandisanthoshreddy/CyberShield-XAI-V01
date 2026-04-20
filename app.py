"""
CyberShield — Mock Backend for Demo
====================================
Runs instantly without a trained model.
Swap get_mock_prediction() with the real model later.

Install:
    pip install fastapi uvicorn

Run:
    python app.py
    → open http://localhost:8000
"""

import random, re, time, math
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI(title="CyberShield Demo")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# ── Serve static files if folder exists ──────────────────────
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# ─────────────────────────────────────────────────────────────
# MOCK MODEL  — realistic rule-based predictor
# Replace this entire section with real model calls later
# ─────────────────────────────────────────────────────────────

THREAT_WORDS = [
    "kill","hurt","destroy","attack","murder","beat","fight","stab","shoot",
    "मारूंगा","नुकसान","चोट","मारेंगे","చంపేస్తాను","హాని","దాడి"
]
INSULT_WORDS = [
    "stupid","idiot","loser","ugly","dumb","worthless","moron","fool","pathetic","hate you",
    "बेवकूफ","मूर्ख","बेकार","गंदा","నీచుడు","తెలివితక్కువ","బుద్ధిహీనుడు","వెర్రివాడు"
]
HATE_WORDS = [
    "racist","terrorism","religion","ethnicity","caste","community","inferior","these people",
    "ये लोग","दुश्मन","మతం","కులం","వాళ్ళు","మన దేశానికి"
]
HARASS_WORDS = [
    "keep posting","everywhere","follow","everywhere you go","watching","leave you alone",
    "पीछा","हमेशा","వెంటాడు","ప్రతిచోటా"
]

def detect_lang(text: str) -> str:
    # Telugu unicode range
    if any('\u0C00' <= c <= '\u0C7F' for c in text):
        return "te"
    # Devanagari (Hindi)
    if any('\u0900' <= c <= '\u097F' for c in text):
        return "hi"
    return "en"

def get_mock_prediction(text: str) -> dict:
    t = text.lower()
    lang = detect_lang(text)

    threat_score    = sum(1 for w in THREAT_WORDS  if w in t) * 0.35
    insult_score    = sum(1 for w in INSULT_WORDS  if w in t) * 0.30
    hate_score      = sum(1 for w in HATE_WORDS    if w in t) * 0.28
    harass_score    = sum(1 for w in HARASS_WORDS  if w in t) * 0.25

    # Add some noise for realism
    noise = random.uniform(0.0, 0.08)
    threat_score  = min(threat_score  + noise, 0.95)
    insult_score  = min(insult_score  + noise, 0.95)
    hate_score    = min(hate_score    + noise, 0.95)
    harass_score  = min(harass_score  + noise, 0.95)

    safe_score = max(0.05, 1.0 - max(threat_score, insult_score, hate_score, harass_score) - noise)

    # Normalise to sum = 1
    raw = {
        "not_bullying": safe_score,
        "insult":       insult_score,
        "threat":       threat_score,
        "hate_speech":  hate_score,
        "harassment":   harass_score,
    }
    total = sum(raw.values())
    probs = {k: round(v / total, 4) for k, v in raw.items()}

    label = max(probs, key=probs.get)
    confidence = probs[label]

    return {
        "label":         label,
        "label_id":      list(raw.keys()).index(label),
        "confidence":    confidence,
        "probabilities": probs,
        "lang":          lang,
    }

def get_mock_attention(text: str, label: str) -> list:
    """Generate fake but plausible attention weights."""
    words = text.split()
    bad_words = set(THREAT_WORDS + INSULT_WORDS + HATE_WORDS + HARASS_WORDS)
    tokens = []
    for w in words:
        clean = re.sub(r'[^\w\u0900-\u097F\u0C00-\u0C7F]', '', w.lower())
        score = 0.75 if any(b in clean for b in bad_words) else random.uniform(0.05, 0.35)
        tokens.append({"token": w, "score": round(score, 3)})
    return tokens

def get_mock_lime(text: str, label: str) -> list:
    """Generate fake LIME feature weights."""
    words = list(set(text.split()))[:10]
    bad_words = set(THREAT_WORDS + INSULT_WORDS + HATE_WORDS + HARASS_WORDS)
    features = []
    for w in words:
        clean = re.sub(r'[^\w\u0900-\u097F\u0C00-\u0C7F]', '', w.lower())
        is_bad = any(b in clean for b in bad_words)
        weight = round(random.uniform(0.15, 0.55) if is_bad else random.uniform(-0.3, 0.05), 4)
        features.append({"word": w, "weight": weight, "positive": weight > 0})
    return sorted(features, key=lambda x: abs(x["weight"]), reverse=True)[:8]

def get_mock_shap(text: str) -> list:
    """Generate fake SHAP values."""
    words = list(set(text.split()))[:10]
    bad_words = set(THREAT_WORDS + INSULT_WORDS + HATE_WORDS + HARASS_WORDS)
    features = []
    for w in words:
        clean = re.sub(r'[^\w\u0900-\u097F\u0C00-\u0C7F]', '', w.lower())
        is_bad = any(b in clean for b in bad_words)
        val = round(random.uniform(0.08, 0.42) if is_bad else random.uniform(-0.25, 0.04), 4)
        features.append({"token": w, "shap_value": val})
    return sorted(features, key=lambda x: abs(x["shap_value"]), reverse=True)[:8]

# ─────────────────────────────────────────────────────────────
# API ROUTES
# ─────────────────────────────────────────────────────────────

class PredictRequest(BaseModel):
    text: str
    include_xai: bool = True
    xai_methods: List[str] = ["attention", "lime"]

class BatchRequest(BaseModel):
    texts: List[str]

@app.get("/health")
def health():
    return {"status": "ok", "mode": "demo (mock model)"}

@app.post("/api/predict")
def predict(req: PredictRequest):
    t0 = time.perf_counter()
    if not req.text.strip():
        return JSONResponse({"detail": "Empty text"}, status_code=400)

    # Simulate model latency
    time.sleep(random.uniform(0.3, 0.8))

    pred = get_mock_prediction(req.text)
    xai  = {}

    if req.include_xai:
        if "attention" in req.xai_methods:
            xai["attention"] = {
                "tokens": get_mock_attention(req.text, pred["label"]),
                "raw_text": req.text,
            }
        if "lime" in req.xai_methods:
            xai["lime"] = {
                "method": "LIME",
                "prediction": pred,
                "top_features": get_mock_lime(req.text, pred["label"]),
                "explanation_score": round(random.uniform(0.72, 0.91), 3),
            }
        if "shap" in req.xai_methods:
            xai["shap"] = {
                "method": "SHAP",
                "prediction": pred,
                "top_features": get_mock_shap(req.text),
            }

    latency = round((time.perf_counter() - t0) * 1000, 1)
    return {
        "text":          req.text,
        "label":         pred["label"],
        "confidence":    pred["confidence"],
        "is_bullying":   pred["label"] != "not_bullying",
        "probabilities": pred["probabilities"],
        "lang":          pred["lang"],
        "xai":           xai,
        "latency_ms":    latency,
    }

@app.post("/api/batch")
def batch(req: BatchRequest):
    if not req.texts:
        return JSONResponse({"detail": "No texts"}, status_code=400)
    results = []
    for text in req.texts[:50]:
        p = get_mock_prediction(text)
        results.append({
            "text":        text,
            "label":       p["label"],
            "confidence":  p["confidence"],
            "is_bullying": p["label"] != "not_bullying",
            "lang":        p["lang"],
        })
    return {
        "results":  results,
        "total":    len(results),
        "flagged":  sum(1 for r in results if r["is_bullying"]),
    }

@app.get("/api/stats")
def stats():
    return {
        "model":      "MuRIL (demo mode — mock predictions)",
        "languages":  ["English", "Hindi (हिंदी)", "Telugu (తెలుగు)"],
        "labels": {
            "not_bullying": "Normal content",
            "insult":       "Personal attack",
            "threat":       "Physical/psychological threat",
            "hate_speech":  "Group-targeted hate",
            "harassment":   "Repeated offensive targeting",
        },
    }

# ─────────────────────────────────────────────────────────────
# SERVE THE FRONTEND (embedded HTML — no separate files needed)
# ─────────────────────────────────────────────────────────────

HTML = open(Path(__file__).parent / "index.html", encoding="utf-8").read()

@app.get("/", response_class=HTMLResponse)
def index():
    return HTML

# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "="*55)
    print("  CyberShield Demo")
    print("  → http://localhost:8000")
    print("  Mode: DEMO (mock predictions, no GPU needed)")
    print("  Ctrl+C to stop")
    print("="*55 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
