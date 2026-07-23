def extract_behavior(scores):

    return {
        "trust_building": scores.get("trust building", 0) > 0.90,
        "secrecy_request": scores.get("secrecy request", 0) > 0.85,
        "image_request": scores.get("image request", 0) > 0.90,
        "meetup_request": scores.get("meetup request", 0) > 0.90,
        "emotional_dependency": scores.get("emotional manipulation", 0) > 0.85
    }


def get_threat_categories(behavior):

    return [
        k for k, v in behavior.items() if v
    ]