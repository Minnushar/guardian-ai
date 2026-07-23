def generate_summary(behavior, threats):

    # normalize threats (IMPORTANT FIX - prevents mismatch bugs)
    normalized = set(t.lower().replace("_", " ") for t in threats)

    # -----------------------------
    # HIGH RISK (SEXUAL + ESCALATION)
    # -----------------------------
    if (
        "photo requests" in normalized or
        "image request" in normalized
    ) and (
        "trust building" in normalized or
        "emotional manipulation" in normalized
    ):
        return "High-risk grooming pattern involving media requests combined with trust-building behavior"

    # -----------------------------
    # SEXUAL BOUNDARY TESTING
    # -----------------------------
    if "photo requests" in normalized or "image request" in normalized:
        return "Possible sexual boundary testing detected"

    # -----------------------------
    # MEETUP / PHYSICAL ESCALATION
    # -----------------------------
    if "meetup request" in normalized:
        return "Physical meetup attempt detected with potential safety risk"

    # -----------------------------
    # SECRECY / CONTROL BEHAVIOR
    # -----------------------------
    if "secrecy request" in normalized:
        return "Manipulative behavior involving secrecy and control tactics"

    # -----------------------------
    # TRUST + DEPENDENCY PATTERN
    # -----------------------------
    if (
        "trust building" in normalized and
        "emotional manipulation" in normalized
    ):
        return "Emotional grooming pattern involving trust building and manipulation signals"

    # -----------------------------
    # GENERAL TRUST BUILDING
    # -----------------------------
    if "trust building" in normalized:
        return "Trust-building behavior detected (monitor for escalation)"

    # -----------------------------
    # DEFAULT SAFE CASE
    # -----------------------------
    return "No significant risk indicators detected in current conversation"