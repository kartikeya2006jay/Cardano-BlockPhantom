import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

ALCHEMY_KEY = os.getenv("ALCHEMY_API_KEY")

BASE = (
    f"https://eth-mainnet.g.alchemy.com/v2/{ALCHEMY_KEY}"
    if ALCHEMY_KEY else None
)


def get_eth_transfers(address: str, max_count: int = 50):
    """
    Retrieve ETH asset transfers using Alchemy's `alchemy_getAssetTransfers` RPC.

    If ALCHEMY_API_KEY is missing, returns mock data.
    """
    if not ALCHEMY_KEY:
        return [
            {
                "hash": "0xmock1",
                "from": "0xabc",
                "to": address,
                "value": "1000000000000000000",
                "blockNum": "0xABC",
                "timestamp": 1690000000,
            },
            {
                "hash": "0xmock2",
                "from": address,
                "to": "0xdef",
                "value": "500000000000000000",
                "blockNum": "0xABD",
                "timestamp": 1690100000,
            },
        ]

    url = BASE
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "alchemy_getAssetTransfers",
        "params": [
            {
                "fromBlock": "0x0",
                "toBlock": "latest",
                "fromAddress": address,
                "category": ["external", "erc20", "erc721", "erc1155"],
                "maxCount": str(max_count),
                "withMetadata": True,
            }
        ],
    }

    r = requests.post(url, json=payload, timeout=20)
    r.raise_for_status()
    data = r.json()

    return data.get("result", {}).get("transfers", [])


def get_tx(tx_hash: str):
    """
    Fetch a full ETH transaction object via RPC-JSON call.
    Returns mock response if API key missing.
    """
    if not ALCHEMY_KEY:
        return {"hash": tx_hash, "mock": True}

    url = BASE
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_getTransactionByHash",
        "params": [tx_hash],
    }

    r = requests.post(url, json=payload, timeout=15)
    r.raise_for_status()
