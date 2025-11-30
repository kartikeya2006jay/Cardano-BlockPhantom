import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def generate_pdf_report(chain, address, risk_result, tx_samples=None):
    """Return (bytes, filename) of a PDF report."""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(72, height - 72, "BlockPhantom — Wallet Risk Report")

    c.setFont("Helvetica", 12)
    c.drawString(72, height - 100, f"Chain: {chain}")
    c.drawString(72, height - 118, f"Address: {address}")
    c.drawString(72, height - 136, f"Risk Score: {risk_result.get('score')}")
    c.drawString(72, height - 154, f"Risk Level: {risk_result.get('level')}")
    c.drawString(72, height - 172, f"Probability: {risk_result.get('probability')}")

    # Details section
    c.drawString(72, height - 200, "Details:")
    y = height - 218

    for k, v in risk_result.get("details", {}).items():
        c.drawString(84, y, f"- {k}: {v}")
        y -= 16
        if y < 72:
            c.showPage()
            y = height - 72
            c.setFont("Helvetica", 12)

    # Sample transactions
    if tx_samples:
        c.drawString(72, y - 8, "Sample Transactions:")
        y -= 26

        for tx in tx_samples[:10]:
            txt = str(tx)
            c.drawString(84, y, txt[:90])
            y -= 14

            if y < 72:
                c.showPage()
                y = height - 72
                c.setFont("Helvetica", 12)

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer.read(), f"report_{chain}_{address[:10]}.pdf"
