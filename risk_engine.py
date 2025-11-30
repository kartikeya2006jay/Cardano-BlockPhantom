@app.get("/wallet/{chain}/{address}/risk")
def risk(chain: str, address: str, demo: bool = False):

    # User forced demo
    if demo:
        return demo_data()

    result, txs = (None, None)

    if chain == "ethereum":
        result, txs = fetch_eth(address)

    elif chain == "cardano":
        result, txs = fetch_cardano(address)

    # If chain invalid or result empty → ALWAYS DEMO
    if not result or result["details"].get("count", 0) == 0:
        return demo_data()

    return result
