from data_loader import load_transactions


def find_related_wallets(wallet):

    transactions = load_transactions()

    related = {}

    for tx in transactions:

        if tx["sender"] == wallet:

            receiver = tx["receiver"]

            if receiver.startswith("EXCHANGE"):
                continue

            related[receiver] = related.get(
                receiver,
                0
            ) + 1

        elif tx["receiver"] == wallet:

            sender = tx["sender"]

            related[sender] = related.get(
                sender,
                0
            ) + 1

    results = []

    for address, count in related.items():

        similarity = min(
            0.95,
            0.2 + (count * 0.2)
        )

        results.append({
            "wallet": address,
            "similarity": round(
                similarity,
                2
            )
        })

    return results