from graph_engine import build_transaction_graph

from risk import calculate_risk_scores
from ml_anomaly import detect_anomalies
from evidence import build_evidence
from entity_resolution import find_related_wallets
from data_loader import load_transactions


def trace_wallet(start_wallet, max_hops=5):
    graph = build_transaction_graph()

    if start_wallet not in graph:
        return {
            "start_wallet": start_wallet,
            "found": False,
            "message": "Wallet not found in transaction graph"
        }

    paths = []

    def explore(current_wallet, path):
        if len(path) > max_hops + 1:
            return

        paths.append(path.copy())

        for next_wallet in graph.successors(current_wallet):
            if next_wallet not in path:
                explore(
                    next_wallet,
                    path + [next_wallet]
                )

    explore(start_wallet, [start_wallet])

    return {
        "start_wallet": start_wallet,
        "found": True,
        "paths": paths
    }


def get_wallet_risk(wallet):
    results = calculate_risk_scores()

    for item in results:

        if item.get("wallet") == wallet:

            return {
                "score": item.get("score", 0),
                "level": item.get("level", "UNKNOWN"),
                "reasons": item.get("reasons", [])
            }

    return {
        "score": 0,
        "level": "UNKNOWN",
        "reasons": []
    }


def get_wallet_anomaly(wallet):
    results = detect_anomalies()

    for item in results:

        if item.get("wallet") == wallet:

            return {
                "prediction": item.get(
                    "prediction",
                    "NO_DATA"
                ),
                "anomaly_score": item.get(
                    "anomaly_score",
                    0
                )
            }

    return {
        "prediction": "NO_DATA",
        "anomaly_score": 0
    }


def get_fund_flow(wallet):

    transactions = load_transactions()

    total_paths = 0
    exchange_paths = 0
    exchange_destinations = []

    for tx in transactions:

        if tx.get("sender") == wallet:

            total_paths += 1

            receiver = tx.get("receiver", "")

            if receiver.startswith("EXCHANGE"):

                exchange_paths += 1

                exchange_destinations.append(
                    receiver
                )

    return {
        "total_paths": total_paths,
        "exchange_paths": exchange_paths,
        "exchange_destinations": exchange_destinations
    }


def run_full_investigation(wallet):

    tracing = trace_wallet(wallet)

    risk = get_wallet_risk(wallet)

    anomaly = get_wallet_anomaly(wallet)

    evidence = build_evidence(wallet)

    related_wallets = find_related_wallets(wallet)

    fund_flow = get_fund_flow(wallet)

    return {
        "wallet": wallet,

        "risk": risk,

        "machine_learning": anomaly,

        "fund_flow": fund_flow,

        "related_wallets": related_wallets,

        "tracing": tracing,

        "evidence": evidence,

        "investigative_lead": {
            "status": "REQUIRES_VERIFICATION",
            "message": (
                "This result identifies a potential "
                "investigative lead based on transaction "
                "and graph evidence. It does not establish "
                "the identity of a person."
            )
        }
    }


def create_investigation_summary(wallet):

    result = run_full_investigation(wallet)

    return result