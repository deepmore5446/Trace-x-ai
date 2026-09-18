from data_loader import load_transactions


def build_transaction_graph():
    transactions = load_transactions()

    nodes = set()
    edges = []

    for tx in transactions:
        sender = tx["sender"]
        receiver = tx["receiver"]

        # Add wallets as nodes
        nodes.add(sender)
        nodes.add(receiver)

        # Add transaction as directed edge
        edges.append({
            "source": sender,
            "target": receiver,
            "amount": tx["amount"],
            "txid": tx["txid"],
            "timestamp": tx["timestamp"]
        })

    return {
        "nodes": [
            {"id": node}
            for node in sorted(nodes)
        ],
        "edges": edges
    }