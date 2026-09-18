import os
import requests

from dotenv import load_dotenv


# =====================================================
# LOAD ENVIRONMENT VARIABLES
# =====================================================

load_dotenv()


ETHERSCAN_API_KEY = os.getenv(
    "ETHERSCAN_API_KEY"
)


# =====================================================
# GET ETHEREUM TRANSACTIONS
# =====================================================

def get_ethereum_transactions(wallet_address):

    if not ETHERSCAN_API_KEY:

        return {
            "status": "error",
            "message": (
                "ETHERSCAN_API_KEY is not configured "
                "in .env file."
            ),
            "transactions": []
        }


    url = "https://api.etherscan.io/v2/api"


    params = {

        "chainid": "1",

        "module": "account",

        "action": "txlist",

        "address": wallet_address,

        "startblock": 0,

        "endblock": 99999999,

        "page": 1,

        "offset": 100,

        "sort": "asc",

        "apikey": ETHERSCAN_API_KEY

    }


    try:

        response = requests.get(
            url,
            params=params,
            timeout=15
        )


        response.raise_for_status()


        data = response.json()


        if data.get("status") != "1":

            return {
                "status": "error",
                "message": data.get(
                    "message",
                    "Unable to fetch transactions."
                ),
                "transactions": []
            }


        transactions = []


        for tx in data.get(
            "result",
            []
        ):

            transactions.append({

                "timestamp":
                    tx.get("timeStamp"),

                "txid":
                    tx.get("hash"),

                "sender":
                    tx.get("from"),

                "receiver":
                    tx.get("to"),

                "amount":
                    int(
                        tx.get(
                            "value",
                            "0"
                        )
                    ) / 10**18

            })


        return {

            "status":
                "success",

            "total":
                len(transactions),

            "transactions":
                transactions

        }


    except requests.RequestException as error:

        return {

            "status":
                "error",

            "message":
                str(error),

            "transactions":
                []

        }


# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":

    print(
        "Blockchain API module loaded."
    )

    if ETHERSCAN_API_KEY:

        print(
            "Etherscan API key detected."
        )

    else:

        print(
            "Etherscan API key NOT detected."
        )