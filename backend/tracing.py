from data_loader import load_transactions


def trace_wallet(wallet):

    transactions = load_transactions()

    related = []

    for tx in transactions:

        if (
            tx["sender"] == wallet
            or tx["receiver"] == wallet
        ):
            related.append(tx)

    return {
        "status": "success",
        "wallet": wallet,
        "transactions": related,
        "total_transactions": len(related)
    }