from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_contract():
    file_name = "sample_contract.pdf"
    c = canvas.Canvas(file_name, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "MASTER SERVICE AGREEMENT (MSA) - 2024")

    c.setFont("Helvetica", 12)
    text_y = height - 80

    # Content designed for your 4 Agents
    lines = [
        "BETWEEN: TechFlow Solutions (Provider) AND Global Corp (Client)",
        "DATE: December 5, 2025",
        "",
        "1. SCOPE OF SERVICES (OPERATIONS)",
        "The Provider shall deliver cloud infrastructure maintenance and 24/7 monitoring.",
        "System uptime is guaranteed at 99.9% (SLA).",
        "If uptime drops below 99.5%, a service credit of 10% will be applied.",
        "Support requests must be resolved within 4 hours for critical issues.",
        "",
        "2. PAYMENT TERMS (FINANCE)",
        "The Client agrees to pay a monthly retainer of $15,000 USD.",
        "Invoices will be issued on the 1st of each month.",
        "Payment terms are Net 30 days.",
        "Late payments shall incur an interest fee of 1.5% per month.",
        "The Total Contract Value (TCV) for the 12-month term is $180,000 USD.",
        "",
        "3. DATA PROTECTION (COMPLIANCE)",
        "The Provider acts as a Data Processor under GDPR regulations.",
        "All customer data shall be encrypted at rest (AES-256) and in transit.",
        "The Client has the right to conduct a security audit once per year.",
        "Any data breach must be reported within 72 hours.",
        "",
        "4. TERMINATION & LIABILITY (LEGAL)",
        "Either party may terminate this agreement with 60 days' written notice.",
        "Immediate termination is permitted for material breach of contract.",
        "The Provider's total liability shall not exceed the value of 6 months of fees ($90,000).",
        "The Provider shall indemnify the Client against IP infringement claims.",
        "",
        "5. GOVERNING LAW",
        "This agreement shall be governed by the laws of the State of New York.",
    ]

    # Write text to PDF
    for line in lines:
        c.drawString(50, text_y, line)
        text_y -= 20  # Move down for next line

    c.save()
    print(f"✅ Created file: {file_name}")

if __name__ == "__main__":
    create_contract()