def compute_confidence(scores, behavior, threats, messages):

    # -----------------------------
    # SAFETY CHECKS
    # -----------------------------
    if not scores:
        return 0.0

    # -----------------------------
    # NORMALIZED MODEL STRENGTH
    # -----------------------------
    model_strength = sum(scores.values()) / len(scores)
    model_strength = max(0.0, min(1.0, model_strength))

    # -----------------------------
    # BEHAVIOR COMPLEXITY SCORE
    # -----------------------------
    behavior_count = sum(1 for v in behavior.values() if v)
    behavior_score = min(behavior_count / 5.0, 1.0)

    # -----------------------------
    # THREAT DENSITY SCORE
    # -----------------------------
    threat_score = min(len(threats) / 4.0, 1.0)

    # -----------------------------
    # CONTEXT DEPTH (MESSAGE CONSISTENCY)
    # -----------------------------
    message_score = min(len(messages) / 10.0, 1.0)

    # -----------------------------
    # BASE CONFIDENCE
    # -----------------------------
    confidence = (
        model_strength * 0.4 +
        behavior_score * 0.2 +
        threat_score * 0.2 +
        message_score * 0.2
    )

    # -----------------------------
    # FIX 1: STRONG SIGNAL ALIGNMENT BOOST
    # -----------------------------
    strong_signals = (
        behavior_count >= 2 and len(threats) >= 2
    )

    if strong_signals:
        confidence += 0.12

    # -----------------------------
    # FIX 2: VERY LOW DATA PENALTY (NOISE CONTROL)
    # -----------------------------
    if len(messages) < 2:
        confidence *= 0.7

    # -----------------------------
    # FIX 3: HIGH RISK CONSISTENCY BOOST
    # (helps align confidence with serious grooming patterns)
    # -----------------------------
    high_risk_pattern = (
        "secrecy request" in threats and
        "image request" in threats
    )

    if high_risk_pattern:
        confidence += 0.08

    # -----------------------------
    # FINAL CLAMP
    # -----------------------------
    confidence = max(0.0, min(confidence, 1.0))

    return round(confidence, 2)