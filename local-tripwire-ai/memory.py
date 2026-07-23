class SenderMemory:
    def __init__(self):
        self.data = {}

    # -----------------------------
    # INIT SENDER MEMORY
    # -----------------------------
    def init(self, sender_id):
        if sender_id not in self.data:
            self.data[sender_id] = {
                "messages": [],
                "risk_history": [],
                "last_risk": 0,
                "seen_messages": set()
            }

    # -----------------------------
    # CHECK IF SENDER EXISTS
    # -----------------------------
    def exists(self, sender_id):
        return sender_id in self.data

    # -----------------------------
    # CHECK DUPLICATE MESSAGE
    # -----------------------------
    def is_duplicate(self, sender_id, message):
        if sender_id not in self.data:
            return False
        return message in self.data[sender_id]["seen_messages"]

    # -----------------------------
    # UPDATE MEMORY
    # -----------------------------
    def update(self, sender_id, message, score):

        if sender_id not in self.data:
            self.init(sender_id)

        memory = self.data[sender_id]

        # mark message as seen
        memory["seen_messages"].add(message)

        # store history
        memory["messages"].append(message)
        memory["risk_history"].append(score)

        # update latest risk
        memory["last_risk"] = score

        # -----------------------------
        # KEEP MEMORY BOUNDED
        # -----------------------------
        if len(memory["messages"]) > 15:
            memory["messages"].pop(0)

        if len(memory["risk_history"]) > 15:
            memory["risk_history"].pop(0)

    # -----------------------------
    # GET MEMORY
    # -----------------------------
    def get(self, sender_id):
        return self.data.get(sender_id, {
            "messages": [],
            "risk_history": [],
            "last_risk": 0,
            "seen_messages": set()
        })