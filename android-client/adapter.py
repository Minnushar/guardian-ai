from person2.model import base_model_score
from person2.memory import SenderMemory
from person2.behavior import extract_behavior, get_threat_categories
from person2.context import infer_context
from person2.summary import generate_summary
from person2.confidence import compute_confidence
from person2.tripwire import get_tripwire

import math
from collections import Counter
import requests
from datetime import datetime

# -----------------------------
# MEMORY
# -----------------------------
memory = SenderMemory()

# ✅ FIXED ENDPOINT (must match P3 exactly)
PERSON3_URL = "https://YOUR-BACKEND-NGROK-URL.ngrok-free.app/history/analyse"


# -----------------------------
# NOISE DETECTION
# -----------------------------
def char_entropy(text):
    if len(text) == 0:
        return 0

    freq = Counter(text)
    total = len(text)

    entropy = 0
    for count in freq.values():
        p = count / total
        entropy -= p * math.log2(p)

    return entropy


def uniqueness_ratio(text):
    if len(text) == 0:
        return 0
    return len(set(text)) / len(text)


def is_noise(text):
    text = text.lower().strip()

    if len(text) <= 3:
        return True

    if char_entropy(text) > 4.2:
        return True

    if uniqueness_ratio(text) > 0.9:
        return True

    return False


# -----------------------------
# MAIN ENGINE
# -----------------------------
def process(sender_id, messages, trigger_message):

    memory.init(sender_id)
    sender_data = memory.get(sender_id)

    # -------------------------
    # DEDUP
    # -------------------------
    seen = sender_data.get("seen_messages", set())

    if trigger_message in seen:
        return {
            "contact_hash": sender_id,
            "trigger_message": trigger_message,
            "local_score": sender_data.get("last_risk", 0),
            "summary": "Duplicate message ignored",
            "status": get_tripwire(sender_data.get("last_risk", 0))
        }

    # -------------------------
    # MODEL INPUT
    # -------------------------
    weighted_messages = [
        m + " [low_signal]" if is_noise(m) else m
        for m in messages
    ]

    model_output = base_model_score(weighted_messages)
    scores = model_output["scores"]
    raw_risk = model_output["risk_score"]

    # -------------------------
    # SAFE NORMALIZATION
    # -------------------------
    normal = scores.get("normal conversation", 0)
    trust = scores.get("trust building", 0)

    if normal > 0.75 and trust > 0.65:
        raw_risk = int(raw_risk * 0.55)

    # -------------------------
    # RULE BOOST / REDUCE
    # -------------------------
    manip = scores.get("emotional manipulation", 0)
    meetup = scores.get("meetup request", 0)
    secrecy = scores.get("secrecy request", 0)

    if trust > 0.85 and manip < 0.5 and meetup < 0.5:
        raw_risk = min(raw_risk, 35)

    if (manip > 0.7 and secrecy > 0.7) or (meetup > 0.75 and manip > 0.6):
        raw_risk = min(100, raw_risk + 15)

    # -------------------------
    # SMOOTHING
    # -------------------------
    prev_risk = sender_data.get("last_risk", 0)
    alpha = 0.55

    risk_score = int(alpha * raw_risk + (1 - alpha) * prev_risk)
    risk_score = max(0, min(100, risk_score))

    # -------------------------
    # STATE
    # -------------------------
    if risk_score >= 75:
        risk_state = "HIGH_RISK"
    elif risk_score >= 40:
        risk_state = "MODERATE_RISK"
    else:
        risk_state = "LOW_RISK"

    # -------------------------
    # UPDATE MEMORY
    # -------------------------
    memory.update(sender_id, trigger_message, risk_score)

    # -------------------------
    # NLP LAYER OUTPUTS
    # -------------------------
    behavior = extract_behavior(scores)
    threats = get_threat_categories(behavior)
    context = infer_context(messages)

    summary = generate_summary(behavior, threats)
    confidence = compute_confidence(scores, behavior, threats, messages)
    confidence = max(0.0, min(1.0, confidence))

    # -------------------------
    # FINAL NORMALIZED PAYLOAD (FIXED FOR P3 + P4)
    # -------------------------
    server_payload = {
        "contact_hash": sender_id,
        "app": "Instagram",

        # 🔥 CORE RISK (P4 EXPECTS THIS)
        "risk_score": risk_score,
        "tripwire_score": risk_score,
        "risk_level": risk_state,

        # 🔥 MODEL INSIGHTS (P4 SAFE STRUCTURE)
        "behavior_scores": scores,
        "risk_breakdown": {
            "raw_risk": raw_risk,
            "smoothed_risk": risk_score
        },

        "relationship_context": context,
        "threat_categories": threats,

        "behavior_summary": summary,
        "summary_confidence": confidence,

        # optional debug (safe for P4)
        "debug": {
            "message_count": len(messages),
            "scores": scores,
            "raw_risk": raw_risk,
            "timestamp": datetime.utcnow().isoformat()
        }
    }

    try:
        response = requests.post(PERSON3_URL, json=server_payload, timeout=5)

        server_response = (
            response.json()
            if response.headers.get("content-type", "").startswith("application/json")
            else {"error": response.text}
        )

    except Exception as e:
        server_response = {
            "error": "Person3 unreachable",
            "details": str(e)
        }

    # -------------------------
    # FINAL OUTPUT (LOCAL DEBUG)
    # -------------------------
    return {
        "contact_hash": sender_id,
        "trigger_message": trigger_message,
        "local_score": risk_score,
        "summary": summary,
        "status": risk_state,
        "server_response": server_response
    }