from graph_engine import build_transaction_graph
from pattern_detector import detect_patterns


def calculate_risk_scores():
    graph = build_transaction_graph()
    patterns = detect_patterns()

    scores = {}

    # Start every wallet with zero risk points
    for wallet in graph.nodes:
        scores[wallet] = {
            "wallet": wallet,
            "score": 0,
            "reasons": []
        }

    # Add risk points based on detected patterns
    for pattern in patterns:

        wallet = pattern["wallet"]

        if wallet not in scores:
            continue

        if pattern["type"] == "FAN_OUT":
            scores[wallet]["score"] += 25
            scores[wallet]["reasons"].append(
                "Fan-out transaction pattern detected"
            )

        elif pattern["type"] == "FAN_IN":
            scores[wallet]["score"] += 25
            scores[wallet]["reasons"].append(
                "Fan-in transaction pattern detected"
            )

        elif pattern["type"] == "EXCHANGE_CASH_OUT":
            scores[wallet]["score"] += 35
            scores[wallet]["reasons"].append(
                "Funds transferred to a known exchange destination"
            )

    # Convert numerical score into a simple category
    for wallet in scores:

        score = scores[wallet]["score"]

        if score >= 60:
            scores[wallet]["risk_level"] = "HIGH"

        elif score >= 30:
            scores[wallet]["risk_level"] = "MEDIUM"

        else:
            scores[wallet]["risk_level"] = "LOW"

    return list(scores.values())


if __name__ == "__main__":
    results = calculate_risk_scores()

    print("TRACE-X AI Risk Analysis")
    print("------------------------")

    for result in results:

        if result["score"] > 0:
            print()
            print("Wallet:", result["wallet"])
            print("Risk Score:", result["score"])
            print("Risk Level:", result["risk_level"])
            print("Reasons:")

            for reason in result["reasons"]:
                print("-", reason)