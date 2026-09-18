from data_loader import load_transactions


def generate_investigative_leads():

    transactions = load_transactions()

    leads = []

    exchange_wallets = set()

    for tx in transactions:

        if tx["receiver"].startswith("EXCHANGE"):
            exchange_wallets.add(
                tx["receiver"]
            )

    for exchange in exchange_wallets:

        incoming = [
            tx for tx in transactions
            if tx["receiver"] == exchange
        ]

        for tx in incoming:

            leads.append({
                "wallet": tx["sender"],
                "destination": exchange,
                "amount": tx["amount"],
                "reason": (
                    "Funds reached a known "
                    "exchange destination"
                ),
                "status": "REQUIRES_VERIFICATION"
            })

    return leads