"""
ingest.py - Day 4

Loads plans.csv and claims.csv with pandas, cleans the data
(nulls, type coercion, deduplication, inconsistent casing), and
writes the cleaned tables into a local SQLite database: coverage.db
"""

import sqlite3
import pandas as pd

DB_PATH = "coverage.db"


def load_and_clean_plans() -> pd.DataFrame:
    df = pd.read_csv("data/plans.csv")

    before = len(df)
    df = df.drop_duplicates()
    print(f"plans: dropped {before - len(df)} duplicate rows")

    df["monthly_premium"] = pd.to_numeric(df["monthly_premium"], errors="coerce")
    df["deductible"] = pd.to_numeric(df["deductible"], errors="coerce")
    df["out_of_pocket_max"] = pd.to_numeric(df["out_of_pocket_max"], errors="coerce")

    median_oopm = df["out_of_pocket_max"].median()
    missing_count = df["out_of_pocket_max"].isna().sum()
    df["out_of_pocket_max"] = df["out_of_pocket_max"].fillna(median_oopm)
    print(f"plans: filled {missing_count} missing out_of_pocket_max values with median ({median_oopm})")

    df["plan_type"] = df["plan_type"].str.strip().str.upper()
    df["tier"] = df["tier"].str.strip().str.title()

    return df


def load_and_clean_claims() -> pd.DataFrame:
    df = pd.read_csv("data/claims.csv")

    before = len(df)
    df = df.drop_duplicates()
    print(f"claims: dropped {before - len(df)} duplicate rows")

    before = len(df)
    df = df.dropna(subset=["member_id"])
    print(f"claims: dropped {before - len(df)} rows with missing member_id")

    before = len(df)
    df = df.dropna(subset=["plan_id"])
    print(f"claims: dropped {before - len(df)} rows with missing plan_id")

    df["status"] = df["status"].str.strip().str.lower()

    df["billed_amount"] = pd.to_numeric(df["billed_amount"], errors="coerce")
    df["approved_amount"] = pd.to_numeric(df["approved_amount"], errors="coerce")
    df["claim_date"] = pd.to_datetime(df["claim_date"], errors="coerce")

    return df


def main() -> None:
    plans_df = load_and_clean_plans()
    claims_df = load_and_clean_claims()

    conn = sqlite3.connect(DB_PATH)
    plans_df.to_sql("plans", conn, if_exists="replace", index=False)
    claims_df.to_sql("claims", conn, if_exists="replace", index=False)
    conn.close()

    print(f"\nLoaded {len(plans_df)} plans and {len(claims_df)} claims into {DB_PATH}")


if __name__ == "__main__":
    main()