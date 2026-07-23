def get_tripwire(score):

    if score >= 80:
        return "HIGH_RISK"
    elif score >= 50:
        return "SUSPICIOUS"
    return "SAFE"