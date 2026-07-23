# Local Tripwire AI

The Local Tripwire AI module performs on-device grooming risk analysis before forwarding results to the backend.

## Features

- Conversation preprocessing
- Duplicate message detection
- Noise filtering
- Zero-shot NLP classification
- Risk score calculation
- Behavioral analysis
- Confidence estimation
- Threat categorization
- Secure communication with the backend API

## Main Components

- `adapter.py` – Parses incoming conversation payloads
- `engine.py` – Core risk analysis pipeline
- `model.py` – Zero-shot NLP model inference
- `memory.py` – Sender memory and risk history
- `behavior.py` – Behavioral feature extraction
- `confidence.py` – Confidence scoring
- `summary.py` – Human-readable summaries
- `tripwire.py` – Risk classification