from data_loader import load_transactions


def get_graph_summary():
    """
    Build a transaction graph from the local
    transaction dataset.
    """

    transactions = load_transactions()

    node_ids = set()
    edges = []

    for tx in transactions:

        sender = tx.get("sender")
        receiver = tx.get("receiver")

        if not sender or not receiver:
            continue

        node_ids.add(sender)
        node_ids.add(receiver)

        edges.append({
            "source": sender,
            "target": receiver,
            "amount": tx.get("amount", 0),
            "txid": tx.get("txid", ""),
            "timestamp": tx.get("timestamp", "")
        })

    nodes = []

    for node_id in sorted(node_ids):
        nodes.append({
            "id": node_id
        })

    return {
        "nodes": nodes,
        "edges": edges
    }