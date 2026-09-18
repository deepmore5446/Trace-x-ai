from blockchain_api import get_ethereum_transactions


def build_blockchain_graph(wallet_address):
    """
    Fetch real blockchain transactions and convert them
    into a graph structure.
    """

    result = get_ethereum_transactions(
        wallet_address
    )

    if result["status"] != "success":
        return {
            "status": "error",
            "message": result.get(
                "message",
                "Unable to fetch blockchain data"
            ),
            "nodes": [],
            "edges": []
        }

    transactions = result.get(
        "transactions",
        []
    )

    node_ids = set()
    edges = []

    for tx in transactions:

        sender = tx.get(
            "sender"
        )

        receiver = tx.get(
            "receiver"
        )

        if not sender or not receiver:
            continue

        # Add wallets as nodes
        node_ids.add(sender)
        node_ids.add(receiver)

        # Add transaction as directed edge
        edges.append({

            "source": sender,

            "target": receiver,

            "amount": tx.get(
                "amount",
                0
            ),

            "txid": tx.get(
                "txid",
                ""
            ),

            "timestamp": tx.get(
                "timestamp",
                ""
            )

        })

    nodes = []

    for node_id in sorted(node_ids):

        nodes.append({
            "id": node_id
        })

    return {
        "status": "success",

        "wallet": wallet_address,

        "nodes": nodes,

        "edges": edges,

        "total_nodes": len(nodes),

        "total_edges": len(edges)
    }