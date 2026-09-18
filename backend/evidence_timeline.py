from data_loader import load_transactions


def get_evidence_timeline(wallet: str):

    transactions = load_transactions()

    timeline = []

    for tx in transactions:

        if (
            tx["sender"] == wallet
            or tx["receiver"] == wallet
        ):

            timeline.append({
                "timestamp": tx["timestamp"],
                "txid": tx["txid"],
                "sender": tx["sender"],
                "receiver": tx["receiver"],
                "amount": tx["amount"]
            })

    # Oldest transaction first
    timeline.sort(
        key=lambda x: x["timestamp"]
    )

    return {
        "wallet": wallet,
        "total_events": len(timeline),
        "timeline": timeline
    }