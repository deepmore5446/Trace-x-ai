from data_loader import load_transactions


def trace_fund_flow(start_wallet: str):
    transactions = load_transactions()

    # Create directed graph
    graph = {}

    for tx in transactions:
        sender = tx["sender"]
        receiver = tx["receiver"]

        if sender not in graph:
            graph[sender] = []

        graph[sender].append({
            "wallet": receiver,
            "amount": tx["amount"],
            "txid": tx["txid"],
            "timestamp": tx["timestamp"]
        })

    # BFS
    queue = [(start_wallet, [start_wallet])]
    visited = {start_wallet}

    paths = []

    while queue:

        current_wallet, current_path = queue.pop(0)

        if current_wallet in graph:

            for transaction in graph[current_wallet]:

                next_wallet = transaction["wallet"]

                new_path = current_path + [next_wallet]

                # Store path when it reaches an exchange
                if next_wallet.startswith("EXCHANGE_"):

                    paths.append({
                        "path": new_path,
                        "amount": transaction["amount"],
                        "txid": transaction["txid"],
                        "timestamp": transaction["timestamp"]
                    })

                # Continue tracing
                elif next_wallet not in visited:

                    visited.add(next_wallet)

                    queue.append(
                        (
                            next_wallet,
                            new_path
                        )
                    )

    return {
        "start_wallet": start_wallet,
        "total_paths": len(paths),
        "paths": paths
    }