import json
import hashlib
from person2.engine import process


def generate_contact_hash(identifier):

    return hashlib.sha256(
        identifier.encode("utf-8")
    ).hexdigest()


def run_whatsapp_payload(payload_json):

    # -----------------------------
    # PARSE INPUT SAFELY
    # -----------------------------
    try:
        data = json.loads(payload_json)

    except json.JSONDecodeError:
        return {
            "error": "Invalid JSON payload"
        }

    # -----------------------------
    # VALIDATE STRUCTURE
    # -----------------------------
    if "message_history" not in data:
        return {
            "error": "Missing message_history field"
        }

    history = data.get("message_history", [])

    if not history:
        return {
            "error": "Empty message history"
        }

    # -----------------------------
    # EXTRACT MESSAGES SAFELY
    # -----------------------------
    messages = []

    for m in history:
        if isinstance(m, dict) and "message_body" in m:
            messages.append(m["message_body"])

    if not messages:
        return {
            "error": "No valid message_body found"
        }

    # -----------------------------
    # TRIGGER MESSAGE
    # -----------------------------
    trigger_message = messages[-1]

    # -----------------------------
    # GENERATE CONTACT HASH
    # -----------------------------
    sender_identifier = data.get(
        "contact_name",
        data.get(
            "contact_id",
            "unknown_sender"
        )
    )

    contact_hash = generate_contact_hash(
        sender_identifier
    )

    # -----------------------------
    # CALL CORE NLP ENGINE
    # -----------------------------
    result = process(
        sender_id=contact_hash,
        messages=messages,
        trigger_message=trigger_message
    )

    # -----------------------------
    # ENSURE PERSON 3 FIELDS EXIST
    # -----------------------------
    result["contact_hash"] = contact_hash

    if "trigger_message" not in result:
        result["trigger_message"] = trigger_message

    # -----------------------------
    # OPTIONAL DEBUG INFO
    # -----------------------------
    result["debug"] = {
        "message_count": len(messages),
        "unique_senders": len(set(
            m.get("sender_name", "unknown")
            for m in history
            if isinstance(m, dict)
        ))
    }

    return result