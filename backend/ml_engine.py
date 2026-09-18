from sklearn.ensemble import IsolationForest

from graph_engine import build_transaction_graph


def create_wallet_features():
    graph = build_transaction_graph()

    features = []
    wallets = []

    for wallet in graph.nodes:

        incoming = graph.in_degree(wallet)
        outgoing = graph.out_degree(wallet)

        total_connections = incoming + outgoing

        wallets.append(wallet)

        features.append([
            incoming,
            outgoing,
            total_connections
        ])

    return wallets, features


def detect_anomalies():
    wallets, features = create_wallet_features()

    if len(wallets) < 3:
        return []

    model = IsolationForest(
        n_estimators=100,
        contamination="auto",
        random_state=42
    )

    predictions = model.fit_predict(features)
    anomaly_scores = model.decision_function(features)

    results = []

    for index, wallet in enumerate(wallets):

        prediction = predictions[index]
        score = anomaly_scores[index]

        results.append({
            "wallet": wallet,
            "ml_prediction": (
                "ANOMALY"
                if prediction == -1
                else "NORMAL"
            ),
            "anomaly_score": round(float(score), 4)
        })

    return results


if __name__ == "__main__":
    results = detect_anomalies()

    print("TRACE-X AI - ML Anomaly Detection")
    print("----------------------------------")

    for result in results:
        print(
            result["wallet"],
            "|",
            result["ml_prediction"],
            "| Score:",
            result["anomaly_score"]
        )