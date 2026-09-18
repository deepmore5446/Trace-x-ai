from data_loader import load_transactions


def calculate_risk_scores():
    transactions = load_transactions()

    results = []

    for tx in transactions:
        sender = tx.get("sender")
        receiver = tx.get("receiver")
        amount = float(tx.get("amount", 0))

        score = 0
        reasons = []

        # Large transaction
        if amount >= 4:
            score += 30
            reasons.append("Large transaction detected")

        # Exchange destination
        if receiver and receiver.startswith("EXCHANGE"):
            score += 20
            reasons.append("Funds transferred to known exchange")

        # Multiple outgoing transactions
        outgoing = [
            item for item in transactions
            if item.get("sender") == sender
        ]

        if len(outgoing) >= 3:
            score += 25
            reasons.append(
                "Fan-out transaction pattern detected"
            )

        # Keep score within 0-100
        score = min(score, 100)

        if score >= 70:
            level = "HIGH"
        elif score >= 40:
            level = "MEDIUM"
        else:
            level = "LOW"

        results.append({
            "wallet": sender,
            "risk": {
                "score": score,
                "level": level,
                "reasons": reasons
            }
        })

    return results