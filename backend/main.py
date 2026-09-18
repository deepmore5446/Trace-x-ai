from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from data_loader import load_transactions
from blockchain_api import get_ethereum_transactions
from blockchain_graph import build_blockchain_graph

from graph import get_graph_summary
from risk import calculate_risk_scores
from ml_anomaly import detect_anomalies
from tracing import trace_wallet
from evidence import build_evidence
from entity_resolution import find_related_wallets
from leads import generate_investigative_leads
from cases import create_case, get_cases, get_case
from investigation import (
    run_full_investigation,
    create_investigation_summary
)


# =====================================================
# APP
# =====================================================

app = FastAPI(
    title="TRACE-X AI",
    description="Explainable Crypto-Fraud Tracing & Investigation System",
    version="1.0.0"
)


# =====================================================
# CORS
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# HOME
# =====================================================

@app.get("/")
def home():
    return {
        "system": "TRACE-X AI",
        "status": "running",
        "message": "Crypto investigation backend is working"
    }


# =====================================================
# HEALTH
# =====================================================

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# =====================================================
# CSV TRANSACTIONS
# =====================================================

@app.get("/transactions")
def get_transactions():

    transactions = load_transactions()

    return {
        "status": "success",
        "total": len(transactions),
        "transactions": transactions
    }


# =====================================================
# GRAPH SUMMARY
# =====================================================

@app.get("/graph")
def get_graph():

    summary = get_graph_summary()

    return {
        "status": "success",
        "graph": summary
    }


# =====================================================
# BASIC WALLET INVESTIGATION
# =====================================================

@app.get("/investigate/{wallet}")
def investigate_wallet(wallet: str):

    return trace_wallet(wallet)


# =====================================================
# RISK ANALYSIS
# =====================================================

@app.get("/risk")
def get_risk_analysis():

    results = calculate_risk_scores()

    return {
        "status": "success",
        "risk_analysis": results
    }


# =====================================================
# MACHINE LEARNING ANOMALIES
# =====================================================

@app.get("/ml/anomalies")
def get_ml_anomalies():

    results = detect_anomalies()

    return {
        "status": "success",
        "model": "Isolation Forest",
        "results": results
    }


# =====================================================
# INVESTIGATIVE LEADS
# =====================================================

@app.get("/leads")
def get_investigative_leads():

    results = generate_investigative_leads()

    return {
        "status": "success",
        "total_leads": len(results),
        "leads": results
    }


# =====================================================
# WALLET EVIDENCE
# =====================================================

@app.get("/evidence/{wallet}")
def get_wallet_evidence(wallet: str):

    result = build_evidence(wallet)

    return {
        "status": "success",
        "evidence": result
    }


# =====================================================
# RELATED WALLETS
# =====================================================

@app.get("/entity-links/{wallet}")
def get_entity_links(wallet: str):

    result = find_related_wallets(wallet)

    return {
        "status": "success",
        "entity_links": result
    }


# =====================================================
# CASE MANAGEMENT
# =====================================================

class CaseRequest(BaseModel):

    wallet: str
    description: str = ""


@app.post("/cases")
def create_new_case(request: CaseRequest):

    case = create_case(
        request.wallet,
        request.description
    )

    return {
        "status": "success",
        "case": case
    }


@app.get("/cases")
def list_cases():

    cases = get_cases()

    return {
        "status": "success",
        "total_cases": len(cases),
        "cases": cases
    }


@app.get("/cases/{case_id}")
def get_single_case(case_id: str):

    case = get_case(case_id)

    if case is None:

        return {
            "status": "error",
            "message": "Case not found"
        }

    return {
        "status": "success",
        "case": case
    }


# =====================================================
# REAL BLOCKCHAIN DATA
# =====================================================

@app.get("/blockchain/{wallet}")
def get_blockchain_data(wallet: str):

    result = get_ethereum_transactions(wallet)

    return {
        "status": result.get("status"),
        "wallet": wallet,
        "total_transactions": result.get(
            "total",
            0
        ),
        "transactions": result.get(
            "transactions",
            []
        ),
        "message": result.get(
            "message",
            ""
        )
    }


# =====================================================
# REAL BLOCKCHAIN GRAPH
# =====================================================

@app.get("/blockchain-graph/{wallet}")
def get_blockchain_graph(wallet: str):

    result = build_blockchain_graph(wallet)

    if result["status"] != "success":

        return {
            "status": "error",
            "message": result.get(
                "message",
                "Graph generation failed"
            )
        }

    return {
        "status": "success",
        "wallet": wallet,
        "graph": {
            "nodes": result["nodes"],
            "edges": result["edges"]
        },
        "summary": {
            "nodes": result["total_nodes"],
            "edges": result["total_edges"]
        }
    }


# =====================================================
# REAL BLOCKCHAIN INVESTIGATION
# =====================================================

@app.get("/investigate-real/{wallet}")
def investigate_real_wallet(wallet: str):

    blockchain_data = get_ethereum_transactions(wallet)

    if blockchain_data["status"] != "success":

        return {
            "status": "error",
            "message": blockchain_data.get(
                "message",
                "Blockchain data fetch failed"
            )
        }

    transactions = blockchain_data["transactions"]

    return {
        "status": "success",
        "wallet": wallet,
        "total_transactions": len(transactions),
        "transactions": transactions
    }


# =====================================================
# FULL INVESTIGATION
# =====================================================

@app.get("/investigate-full/{wallet}")
def full_investigation(wallet: str):

    result = run_full_investigation(wallet)

    return {
        "status": "success",
        "investigation": result
    }


# =====================================================
# INVESTIGATION SUMMARY
# =====================================================

@app.get("/investigation-summary/{wallet}")
def investigation_summary(wallet: str):

    result = create_investigation_summary(wallet)

    return {
        "status": "success",
        "investigation": result
    }