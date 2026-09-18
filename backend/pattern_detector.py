from graph_engine import build_transaction_graph
from data_loader import load_transactions


def detect_patterns():
    graph = build_transaction_graph()
    transactions = load_transactions()

    patterns = []

    # 1. Fan-out detection
    for wallet in graph.nodes:
        outgoing_count = graph.out_degree(wallet)

        if outgoing_count >= 3:
            patterns.append({
                "type": "FAN_OUT",
                "wallet": wallet,
                "detail": f"{wallet} sends funds to {outgoing_count} different wallets"
            })

    # 2. Fan-in detection
    for wallet in graph.nodes:
        incoming_count = graph.in_degree(wallet)

        if incoming_count >= 3:
            patterns.append({
                "type": "FAN_IN",
                "wallet": wallet,
                "detail": f"{wallet} receives funds from {incoming_count} different wallets"
            })

    # 3. Exchange destination detection
    for transaction in transactions:
        receiver = transaction["receiver"]

        if receiver.startswith("EXCHANGE_"):
            patterns.append({
                "type": "EXCHANGE_CASH_OUT",
                "wallet": transaction["sender"],
                "destination": receiver,
                "amount": transaction["amount"],
                "txid": transaction["txid"]
            })

    return patterns


if __name__ == "__main__":
    detected_patterns = detect_patterns()

    print("Detected Suspicious Patterns")
    print("----------------------------")

    for pattern in detected_patterns:
        print(pattern)