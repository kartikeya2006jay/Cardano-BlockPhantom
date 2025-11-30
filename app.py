from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
import random
import tempfile

app = FastAPI()

# CORS (allow frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# SMART RANDOM RISK GENERATOR
# ---------------------------

def generate_random_risk():

    # RANDOM SCORE 1–99
    score = random.randint(1, 99)

    # ----- SMART PROBABILITY -----
    # LOW (0–30)
    if score <= 30:
        probability = round(random.uniform(0.01, 0.30), 3)

    # MEDIUM (31–60)
    elif score <= 60:
        probability = round(random.uniform(0.30, 0.60), 3)

    # HIGH (61–99)
    else:
        probability = round(random.uniform(0.60, 0.99), 3)

    # ----- RISK LEVEL -----
    level = (
        "low" if score <= 30 else
        "medium" if score <= 60 else
        "high"
    )

    # ----- RANDOM STATS -----
    avg = round(random.uniform(0.01, 5.0), 4)
    std = round(random.uniform(0.01, 2.0), 4)
    count = random.randint(1, 50)

    return {
        "score": score,
        "probability": probability,
        "level": level,
        "details": {
            "avg": avg,
            "std": std,
            "count": count
        },
        "demo": False
    }


def generate_random_transactions(n=10):
    txs = []
    for _ in range(n):
        txs.append({
            "hash": f"tx_{random.randint(10000, 99999)}",
            "amount": round(random.uniform(0.1, 3.0), 4)
        })
    return txs


# ---------------------------
# API ENDPOINTS
# ---------------------------

@app.get("/wallet/{chain}/{address}/risk")
def risk(chain: str, address: str, demo: bool = False):
    return generate_random_risk()


@app.get("/wallet/{chain}/{address}/history")
def history(chain: str, address: str, demo: bool = False):
    count = random.randint(3, 12)
    return {"transactions": generate_random_transactions(count)}


@app.get("/wallet/{chain}/{address}/pdf")
def pdf(chain: str, address: str):
    data = generate_random_risk()

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(temp.name, pagesize=letter)
    styles = getSampleStyleSheet()

    story = [
        Paragraph("<b>BlockPhantom Smart Random Risk Report</b>", styles["Title"]),
        Paragraph(f"Chain: {chain}", styles["Normal"]),
        Paragraph(f"Address: {address}", styles["Normal"]),
        Paragraph(f"Risk Score: {data['score']}", styles["Normal"]),
        Paragraph(f"Probability: {data['probability']}", styles["Normal"]),
        Paragraph(f"Level: {data['level']}", styles["Normal"]),
        Paragraph(f"Tx Count: {data['details']['count']}", styles["Normal"]),
    ]

    doc.build(story)
    return FileResponse(temp.name, filename="risk_report.pdf")
