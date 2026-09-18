from data_loader import load_transactions


def build_evidence(wallet):

    transactions = load_transactions()

    evidence = []

    for tx in transactions:

        if tx["sender"] == wallet:

            evidence.append({
                "type": "OUTGOING_TRANSACTION",
                "description": (
                    f"{wallet} sent "
                    f"{tx['amount']} to "
                    f"{tx['receiver']}"
                ),
                "txid": tx["txid"],
                "timestamp": tx["timestamp"]
            })

        elif tx["receiver"] == wallet:

            evidence.append({
                "type": "INCOMING_TRANSACTION",
                "description": (
                    f"{wallet} received "
                    f"{tx['amount']} from "
                    f"{tx['sender']}"
                ),
                "txid": tx["txid"],
                "timestamp": tx["timestamp"]
            })

    return {
        "wallet": wallet,
        "total_evidence": len(evidence),
        "items": evidence
    }