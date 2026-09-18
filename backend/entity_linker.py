from graph_engine import build_transaction_graph


def calculate_wallet_similarity(wallet1, wallet2, graph):
    incoming_1 = set(graph.predecessors(wallet1))
    outgoing_1 = set(graph.successors(wallet1))

    incoming_2 = set(graph.predecessors(wallet2))
    outgoing_2 = set(graph.successors(wallet2))

    connections_1 = incoming_1 | outgoing_1
    connections_2 = incoming_2 | outgoing_2

    if not connections_1 or not connections_2:
        return 0

    intersection = connections_1 & connections_2
    union = connections_1 | connections_2

    similarity = len(intersection) / len(union)

    return round(similarity, 4)


def find_related_wallets(target_wallet, threshold=0.2):
    graph = build_transaction_graph()

    if target_wallet not in graph:
        return {
            "wallet": target_wallet,
            "found": False,
            "related_wallets": []
        }

    results = []

    for wallet in graph.nodes:

        if wallet == target_wallet:
            continue

        similarity = calculate_wallet_similarity(
            target_wallet,
            wallet,
            graph
        )

        if similarity >= threshold:
            results.append({
                "wallet": wallet,
                "similarity": similarity
            })

    results.sort(
        key=lambda item: item["similarity"],
        reverse=True
    )

    return {
        "wallet": target_wallet,
        "found": True,
        "related_wallets": results
    }


if __name__ == "__main__":

    target_wallet = "WALLET_A"

    result = find_related_wallets(target_wallet)

    print("TRACE-X AI - Entity Linking")
    print("---------------------------")

    print("Target Wallet:", target_wallet)

    print("\nPotentially Related Wallets:")

    for wallet in result["related_wallets"]:
        print(
            wallet["wallet"],
            "| Similarity:",
            wallet["similarity"]
        )