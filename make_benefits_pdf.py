"""
make_benefits_pdf.py - Day 5
Generates a SYNTHETIC "Summary of Benefits" PDF (fake plan, not real member data).
"""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

OUT_PATH = "source_docs/benefits.pdf"


def draw_header_footer(c, page_num):
    c.setFont("Helvetica", 8)
    c.drawString(0.75 * inch, 10.6 * inch, "CONFIDENTIAL - Synthetic Demo Plan Document (not real member data)")
    c.drawString(0.75 * inch, 0.5 * inch, f"Page {page_num} | SampleCare Health Plans - Synthetic Data")


def build_pdf():
    c = canvas.Canvas(OUT_PATH, pagesize=letter)

    draw_header_footer(c, 1)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(0.75 * inch, 10 * inch, "Summary of Benefits - Gold PPO Plan")

    c.setFont("Helvetica", 11)
    lines = [
        "",
        "Plan Name: Gold PPO 2026",
        "Plan Type: PPO",
        "Monthly Premium: $612.50",
        "Annual Deductible: $1,500 (individual) / $3,000 (family)",
        "Out-of-Pocket Maximum: $6,000 (individual) / $12,000 (family)",
        "",
        "Covered Services:",
        "  - Primary Care Visit: $25 copay",
        "  - Specialist Visit: $50 copay",
        "  - Emergency Room: $250 copay, then plan pays 80%",
        "  - Urgent Care: $75 copay",
        "  - Preventive Care: $0 copay (covered in full)",
        "  - Prescription Drugs (generic): $10 copay",
        "  - Prescription Drugs (brand): $40 copay",
        "  - Lab Work: 20% coinsurance after deductible",
        "  - Imaging (MRI/CT): 20% coinsurance after deductible",
        "  - Physical Therapy: $40 copay per visit",
    ]
    y = 9.6 * inch
    for line in lines:
        c.drawString(0.75 * inch, y, line)
        y -= 0.22 * inch

    c.showPage()

    draw_header_footer(c, 2)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(0.75 * inch, 10 * inch, "Exclusions and Limitations")

    c.setFont("Helvetica", 11)
    lines2 = [
        "",
        "This plan does not cover:",
        "  - Cosmetic procedures not deemed medically necessary",
        "  - Experimental treatments not approved by the FDA",
        "  - Services received outside the network without prior authorization",
        "",
        "Prior Authorization Required For:",
        "  - Inpatient hospital admissions (non-emergency)",
        "  - Advanced imaging (MRI, CT, PET scans)",
        "  - Certain specialty medications",
        "",
        "Member Services: 1-800-555-0182",
        "Website: www.samplecarehealth-demo.com",
    ]
    y = 9.6 * inch
    for line in lines2:
        c.drawString(0.75 * inch, y, line)
        y -= 0.22 * inch

    c.showPage()
    c.save()
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    build_pdf()