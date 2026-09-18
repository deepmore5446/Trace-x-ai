from data_loader import load_transactions


def detect_anomalies():

    transactions = load_transactions()

    wallet_activity = {}

    for tx in transactions:

        sender = tx["sender"]

        if sender not in wallet_activity:
            wallet_activity[sender] = {
                "count": 0,
                "volume": 0
            }

        wallet_activity[sender]["count"] += 1
        wallet_activity[sender]["volume"] += float(
            tx["amount"]
        )

    results = []

    for wallet, data in wallet_activity.items():

        count = data["count"]
        volume = data["volume"]

        if count >= 3 or volume >= 4:
            prediction = "ANOMALY"
            anomaly_score = -0.16
        else:
            prediction = "NORMAL"
            anomaly_score = 0.12

        results.append({
            "wallet": wallet,
            "prediction": prediction,
            "anomaly_score": anomaly_score
        })

    return results