def infer_context(messages):

    return {
        "known_friend": False,
        "long_term_contact": len(messages) > 10,
        "online_only_contact": True
    }