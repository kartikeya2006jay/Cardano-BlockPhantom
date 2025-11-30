# backend/masumi_client.py
import os, requests, time
from dotenv import load_dotenv

load_dotenv()

REGISTRY_BASE = os.getenv("MASUMI_REGISTRY_URL", "https://registry.masumi.network/api/v1")
PAYMENT_BASE = os.getenv("MASUMI_PAYMENT_URL", "https://payment.masumi.network/api/v1")
API_KEY = os.getenv("MASUMI_API_KEY")
AGENT_ID = os.getenv("MASUMI_AGENT_ID")  # optional: set after registration

HEADERS = {"token": API_KEY} if API_KEY else {}

def register_agent(payload: dict):
    """
    Register a service/agent in Masumi registry. Returns registry entry JSON.
    payload example: {"agent_identifier": "blockphantom", "name":"BlockPhantom Risk", "description":"Wallet risk analysis", "endpoint":"https://api.yourdomain.com/..." }
    """
    url = f"{REGISTRY_BASE}/agents"
    r = requests.post(url, json=payload, headers=HEADERS, timeout=15)
    r.raise_for_status()
    return r.json()

def get_agents(query_params=None):
    url = f"{REGISTRY_BASE}/agents"
    r = requests.get(url, params=query_params or {}, headers=HEADERS, timeout=10)
    r.raise_for_status()
    return r.json()

def create_payment_request(amount_lovelace_or_cents: int, currency: str, metadata: dict):
    """
    Create a payment request in Masumi Payment service.
    - amount_lovelace_or_cents: integer representing smallest unit (e.g., lovelace for Cardano)
    - currency: 'ADA' or 'USD' (depends on Masumi deployment)
    - metadata: arbitrary dict (e.g. {"service":"blockphantom","address":"..."})
    Returns: payment object with id and payment_url or on-chain instructions.
    """
    url = f"{PAYMENT_BASE}/payments"
    payload = {
        "amount": int(amount_lovelace_or_cents),
        "currency": currency,
        "metadata": metadata,
        "callback_url": metadata.get("callback_url")  # optional
    }
    r = requests.post(url, json=payload, headers=HEADERS, timeout=15)
    r.raise_for_status()
    return r.json()

def get_payment_status(payment_id: str):
    url = f"{PAYMENT_BASE}/payments/{payment_id}"
    r = requests.get(url, headers=HEADERS, timeout=10)
    r.raise_for_status()
    return r.json()

def log_decision(agent_id: str, event: dict):
    """
    Post a decision/event to Masumi's logging/registry (or a custom endpoint).
    event example: {"address":"0x..","score":72,"level":"high","timestamp": 1234567890}
    """
    url = f"{REGISTRY_BASE}/agents/{agent_id}/decisions"
    r = requests.post(url, json=event, headers=HEADERS, timeout=10)
    r.raise_for_status()
    return r.json()
