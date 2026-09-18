import uuid
from datetime import datetime


cases_db = {}


def create_case(wallet, description=""):

    case_id = "CASE-" + str(uuid.uuid4())[:8].upper()

    case = {
        "case_id": case_id,
        "wallet": wallet,
        "description": description,
        "status": "OPEN",
        "created_at": datetime.now().isoformat()
    }

    cases_db[case_id] = case

    return case


def get_cases():

    return list(cases_db.values())


def get_case(case_id):

    return cases_db.get(case_id)