from transformers import pipeline

# --------------------------------------------------
# Load Zero-Shot Classification Model
# --------------------------------------------------

classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

# Labels used for grooming detection
LABELS = [
    "normal conversation",
    "trust building",
    "secrecy request",
    "image request",
    "meetup request",
    "emotional manipulation"
]


# --------------------------------------------------
# Base Model Inference
# --------------------------------------------------

def base_model_score(messages):
    """
    Performs zero-shot classification on the conversation and
    returns both label probabilities and an initial risk score.
    """

    conversation = " ".join(messages)

    result = classifier(
        conversation,
        LABELS,
        multi_label=True
    )

    scores = {
        label: score
        for label, score in zip(
            result["labels"],
            result["scores"]
        )
    }

    # --------------------------------------------------
    # Weighted Risk Calculation
    # --------------------------------------------------

    risk_score = (
        scores.get("trust building", 0) * 20 +
        scores.get("secrecy request", 0) * 30 +
        scores.get("image request", 0) * 30 +
        scores.get("meetup request", 0) * 15 +
        scores.get("emotional manipulation", 0) * 25
    )

    risk_score = int(min(risk_score, 100))

    return {
        "scores": scores,
        "risk_score": risk_score
    }