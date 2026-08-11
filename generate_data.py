"""
generate_data.py - Day 4

Generates SYNTHETIC (fake) healthcare coverage data: plans.csv and claims.csv.
This is not real member data - just realistic-looking fake data to practice
pandas cleaning, SQLite loading, and SQL querying.

Intentionally includes some messiness (nulls, duplicate rows, inconsistent
casing/types) so the ingestion lab has real cleaning work to do.
"""

import csv
import random

random.seed(42)

# ---------------------------------------------------------------------------
# PLANS
# ---------------------------------------------------------------------------
PLAN_TYPES = ["HMO", "PPO", "EPO", "HDHP"]
PLAN_TIERS = ["Bronze", "Silver", "Gold", "Platinum"]

plans = []
for i in range(1, 21):
    plan_id = f"PLN{i:03d}"
    plan_type = random.choice(PLAN_TYPES)
    tier = random.choice(PLAN_TIERS)
    monthly_premium = round(random.uniform(150, 900), 2)
    deductible = random.choice([500, 1000, 1500, 2500, 5000])
    out_of_pocket_max = random.choice([3000, 6000, 8000, None])
    plans.append({
        "plan_id": plan_id,
        "plan_name": f"{tier} {plan_type} {i}",
        "plan_type": plan_type,
        "tier": tier,
        "monthly_premium": monthly_premium,
        "deductible": deductible,
        "out_of_pocket_max": out_of_pocket_max,
    })

plans.append(dict(plans[2]))
plans.append(dict(plans[7]))

# ---------------------------------------------------------------------------
# CLAIMS
# ---------------------------------------------------------------------------
CLAIM_STATUSES = ["approved", "denied", "pending", "Approved", "APPROVED"]
SERVICE_TYPES = [
    "Primary Care Visit", "Specialist Visit", "Emergency Room",
    "Lab Work", "Imaging (MRI/CT)", "Physical Therapy",
    "Prescription Drug", "Urgent Care", "Preventive Care", "Surgery",
]

member_ids = [f"MBR{i:04d}" for i in range(1, 61)]
plan_ids = [p["plan_id"] for p in plans[:20]]

claims = []
claim_counter = 1
for member_id in member_ids:
    n_claims = random.randint(0, 6)
    assigned_plan = random.choice(plan_ids)
    for _ in range(n_claims):
        claim_id = f"CLM{claim_counter:05d}"
        claim_counter += 1
        service_type = random.choice(SERVICE_TYPES)
        billed_amount = round(random.uniform(50, 8000), 2)
        status = random.choice(CLAIM_STATUSES)
        if status.lower() == "denied":
            approved_amount = None
        elif status.lower() == "pending":
            approved_amount = None
        else:
            approved_amount = round(billed_amount * random.uniform(0.5, 1.0), 2)

        claim_date = f"2025-{random.randint(1,12):02d}-{random.randint(1,28):02d}"

        claims.append({
            "claim_id": claim_id,
            "member_id": member_id,
            "plan_id": assigned_plan,
            "service_type": service_type,
            "claim_date": claim_date,
            "billed_amount": billed_amount,
            "approved_amount": approved_amount,
            "status": status,
        })

if len(claims) > 5:
    claims.append(dict(claims[3]))
    claims.append(dict(claims[10]))

if len(claims) > 20:
    claims[15]["plan_id"] = None
    claims[20]["member_id"] = None

# ---------------------------------------------------------------------------
# WRITE CSVs
# ---------------------------------------------------------------------------
with open("data/plans.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(plans[0].keys()))
    writer.writeheader()
    writer.writerows(plans)

with open("data/claims.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(claims[0].keys()))
    writer.writeheader()
    writer.writerows(claims)

print(f"Wrote {len(plans)} plan rows -> data/plans.csv")
print(f"Wrote {len(claims)} claim rows -> data/claims.csv")