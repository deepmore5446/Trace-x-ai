from graph_engine import build_transaction_graph
from risk_engine import calculate_risk_scores
from ml_engine import detect_anomalies
from evidence_engine import build_evidence
from entity_linker import find_related_wallets


def run_full_investigation(wallet):
    graph = build_transaction_graph()

    if wallet not in graph:
        return {
            "found": False,
            "message": "Wallet not found in transaction graph"
        }

    # Risk analysis
    risk_results = calculate_risk_scores()

    wallet_risk = None

    for result in risk_results:
        if result["wallet"] == wallet:
            wallet_risk = result
            break

    # ML analysis
    ml_results = detect_anomalies()

    wallet_ml = None

    for result in ml_results:
        if result["wallet"] == wallet:
            wallet_ml = result
            break

    # Evidence / fund flow
    evidence = build_evidence(wallet)

    # Entity linking
    entity_links = find_related_wallets(wallet)

    return {
        "found": True,
        "wallet": wallet,

        "risk_analysis": wallet_risk,

        "ml_analysis": wallet_ml,

        "fund_flow_evidence": evidence,

        "entity_links": entity_links,

        "investigation_note": (
            "Results are investigative leads based on "
            "transaction and graph evidence. "
            "Human investigator verification is required."
        )
    }


if __name__ == "__main__":

    wallet = "WALLET_A"

    result = run_full_investigation(wallet)

    print("TRACE-X AI - Full Investigation")
    print("--------------------------------")

    print("Wallet:", result["wallet"])

    print("\nRisk Analysis:")
    print(result["risk_analysis"])

    print("\nML Analysis:")
    print(result["ml_analysis"])

    print("\nExchange Paths:")
    for path in result["fund_flow_evidence"]["exchange_paths"]:
        print(
            " -> ".join(path["path"])
        )

    print("\nEntity Links:")
    print(result["entity_links"]["related_wallets"])
def create_investigation_summary(wallet):
    result = run_full_investigation(wallet)

    if not result["found"]:
        return result

    risk = result["risk_analysis"]
    ml = result["ml_analysis"]
    evidence = result["fund_flow_evidence"]
    entity_links = result["entity_links"]

    exchange_paths = evidence.get("exchange_paths", [])

    exchange_destinations = []

    for path in exchange_paths:
        if path["path"]:
            exchange_destinations.append(
                path["path"][-1]
            )

    return {
        "wallet": wallet,

        "risk": {
            "score": risk["score"],
            "level": risk["risk_level"],
            "reasons": risk["reasons"]
        },

        "machine_learning": {
            "prediction": ml["ml_prediction"],
            "anomaly_score": ml["anomaly_score"]
        },

        "fund_flow": {
            "total_paths": evidence["total_paths"],
            "exchange_paths": len(exchange_paths),
            "exchange_destinations": exchange_destinations
        },

        "related_wallets": entity_links["related_wallets"],

        "investigative_lead": {
            "status": "REQUIRES_VERIFICATION",
            "message": (
                "This result identifies a potential investigative "
                "lead based on transaction and graph evidence. "
                "It does not establish the identity of a person."
            )
        }
    }    