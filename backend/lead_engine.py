from risk_engine import calculate_risk_scores
from ml_engine import detect_anomalies
from investigation import trace_wallet


def generate_investigative_leads():
    risk_results = calculate_risk_scores()
    ml_results = detect_anomalies()

    ml_map = {
        item["wallet"]: item
        for item in ml_results
    }

    leads = []

    for risk in risk_results:
        wallet = risk["wallet"]
        risk_score = risk["score"]

        ml_data = ml_map.get(wallet, {})

        ml_prediction = ml_data.get(
            "ml_prediction",
            "NORMAL"
        )

        anomaly_score = ml_data.get(
            "anomaly_score",
            0
        )

        lead_score = risk_score

        evidence = list(risk["reasons"])

        if ml_prediction == "ANOMALY":
            lead_score += 30
            evidence.append(
                "Machine learning model detected abnormal wallet behavior"
            )

        if lead_score >= 70:
            priority = "HIGH"
        elif lead_score >= 40:
            priority = "MEDIUM"
        else:
            priority = "LOW"

        leads.append({
            "wallet": wallet,
            "lead_score": lead_score,
            "priority": priority,
            "risk_score": risk_score,
            "ml_prediction": ml_prediction,
            "anomaly_score": anomaly_score,
            "evidence": evidence,
            "investigation_note": (
                "This wallet is a primary investigative lead "
                "and requires investigator verification."
            )
        })

    leads.sort(
        key=lambda item: item["lead_score"],
        reverse=True
    )

    return leads


if __name__ == "__main__":
    results = generate_investigative_leads()

    print("TRACE-X AI - Primary Investigative Leads")
    print("----------------------------------------")

    for lead in results:
        if lead["lead_score"] > 0:
            print()
            print("Wallet:", lead["wallet"])
            print("Lead Score:", lead["lead_score"])
            print("Priority:", lead["priority"])
            print("Risk Score:", lead["risk_score"])
            print("ML:", lead["ml_prediction"])
            print("Evidence:")

            for evidence in lead["evidence"]:
                print("-", evidence)