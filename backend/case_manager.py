import json
import os
from datetime import datetime


CASES_FILE = os.path.join(
    os.path.dirname(__file__),
    "cases.json"
)


def load_cases():
    if not os.path.exists(CASES_FILE):
        return []

    with open(CASES_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_cases(cases):
    with open(CASES_FILE, "w", encoding="utf-8") as file:
        json.dump(cases, file, indent=4)


def create_case(wallet, description=""):
    cases = load_cases()

    case_id = f"CASE-{len(cases) + 1:04d}"

    case = {
        "case_id": case_id,
        "wallet": wallet,
        "description": description,
        "status": "OPEN",
        "created_at": datetime.now().isoformat()
    }

    cases.append(case)
    save_cases(cases)

    return case


def get_cases():
    return load_cases()


def get_case(case_id):
    cases = load_cases()

    for case in cases:
        if case["case_id"] == case_id:
            return case

    return None


if __name__ == "__main__":

    case = create_case(
        "WALLET_A",
        "Suspected fraud-linked wallet"
    )

    print("TRACE-X AI - Case Management")
    print("-----------------------------")
    print("Case Created:")
    print(case)