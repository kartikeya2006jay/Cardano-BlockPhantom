import os
import requests
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

API_KEY = os.getenv("BLOCKFROST_API_KEY")
NETWORK = os.getenv("BLOCKFROST_NETWORK", "mainnet")

BASE = (
    "https://cardano-mainnet.blockfrost.io/api/v0"
    if NETWORK == "mainnet"
    else "https://cardano-testnet.blockfrost.io/api/v0"
)

HEADERS = {"project_id": API_KEY} if API_KEY else {}


def get_address_txs(address: str, count: int = 50):
    """
    Fetch list of transaction hashes for a Cardano address using Blockfrost API.

    If BLOCKFROST_API_KEY is not set, returns mock data.
    """
    if not API_KEY:
        # Mock example when API key is missing
        return [
            {
                "tx_hash": "mock_tx_1",
                "time": 1690000000,
                "amount": [{"unit": "lovelace", "quantity": "1000000"}],
                "direction": "in"
            },
            {
                "tx_hash": "mock_tx_2",
                "time": 1690100000,
                "amount": [{"unit": "lovelace", "quantity": "5000000"}],
                "direction": "out"
            }
        ]

    url = f"{BASE}/addresses/{address}/transactions?order=desc&count={count}"
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.raise_for_status()

    items = r.json()
    return items  # Blockfrost returns simplified TX objects


def get_tx(tx_hash: str):
    """
    Fetch detailed transaction info for a given transaction hash.
    Returns mock JSON if no API key.
    """
    if not API_KEY:
        return {"tx_hash": tx_hash, "mock": True}

    url = f"{BASE}/txs/{tx_hash}"
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.raise_for_status()
    return r.json()
