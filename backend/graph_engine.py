import networkx as nx

from data_loader import load_transactions


def build_transaction_graph():
    transactions = load_transactions()

    graph = nx.DiGraph()

    for transaction in transactions:
        sender = transaction["sender"]
        receiver = transaction["receiver"]

        graph.add_node(sender)
        graph.add_node(receiver)

        graph.add_edge(
            sender,
            receiver,
            txid=transaction["txid"],
            amount=transaction["amount"],
            timestamp=transaction["timestamp"]
        )

    return graph


def get_graph_summary():
    graph = build_transaction_graph()

    return {
        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges()
    }


if __name__ == "__main__":
    summary = get_graph_summary()

    print("Transaction Graph")
    print("-----------------")
    print(f"Wallet/Entity Nodes: {summary['nodes']}")
    print(f"Transaction Edges: {summary['edges']}")