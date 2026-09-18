from graph_engine import build_transaction_graph
from data_loader import load_transactions


def build_evidence(wallet, max_hops=5):
    graph = build_transaction_graph()
    transactions = load_transactions()

    if wallet not in graph:
        return {
            "wallet": wallet,
            "found": False,
            "message": "Wallet not found in transaction graph"
        }

    transaction_map = {}

    for transaction in transactions:
        key = (
            transaction["sender"],
            transaction["receiver"]
        )

        transaction_map[key] = transaction

    paths = []

    def explore(current_wallet, path):

        if len(path) > max_hops + 1:
            return

        if len(path) > 1:

            evidence_steps = []

            for i in range(len(path) - 1):

                sender = path[i]
                receiver = path[i + 1]

                transaction = transaction_map.get(
                    (sender, receiver)
                )

                if transaction:
                    evidence_steps.append({
                        "from": sender,
                        "to": receiver,
                        "txid": transaction["txid"],
                        "amount": transaction["amount"],
                        "timestamp": transaction["timestamp"]
                    })

            paths.append({
                "path": path.copy(),
                "hops": len(path) - 1,
                "transactions": evidence_steps
            })

        for next_wallet in graph.successors(current_wallet):

            if next_wallet not in path:
                explore(
                    next_wallet,
                    path + [next_wallet]
                )

    explore(wallet, [wallet])

    exchange_paths = []

    for path_data in paths:

        final_wallet = path_data["path"][-1]

        if final_wallet.startswith("EXCHANGE_"):
            exchange_paths.append(path_data)

    return {
        "wallet": wallet,
        "found": True,
        "total_paths": len(paths),
        "exchange_paths": exchange_paths,
        "all_paths": paths
    }


if __name__ == "__main__":

    wallet = "WALLET_A"

    result = build_evidence(wallet)

    print("TRACE-X AI - Evidence & Fund Flow")
    print("---------------------------------")

    print("Wallet:", wallet)
    print("Found:", result["found"])

    print("\nExchange Paths:")

    for path in result["exchange_paths"]:

        print()
        print("Path:", " -> ".join(path["path"]))
        print("Hops:", path["hops"])

        for transaction in path["transactions"]:

            print(
                transaction["from"],
                "->",
                transaction["to"],
                "|",
                transaction["amount"],
                "BTC",
                "|",
                transaction["txid"]
            )