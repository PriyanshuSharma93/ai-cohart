
"""
build_knowledge_base.py - Day 6

Turns Day 4's structured plan data and Day 5's extracted policy text into a
single unified, chunked knowledge base: knowledge_base.jsonl (one JSON
object per line), ready for embedding in later days.
"""

import json
import re
import sqlite3
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter

RAW_TEXT_DIR = Path("raw_text")
DB_PATH = "coverage.db"
OUT_PATH = "knowledge_base.jsonl"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

SOURCE_META = {
    "benefits.txt": {"source_type": "summary_of_benefits", "plan_type": "PPO"},
    "claims_process.txt": {"source_type": "claims_process_guide", "plan_type": None},
    "enrollment.txt": {"source_type": "enrollment_form", "plan_type": "PPO"},
    "provider_faq.txt": {"source_type": "provider_faq", "plan_type": None},
}

SECTION_PATTERNS = [
    (re.compile(r"exclusion", re.IGNORECASE), "exclusions"),
    (re.compile(r"prior authorization", re.IGNORECASE), "prior_authorization"),
    (re.compile(r"covered services", re.IGNORECASE), "covered_services"),
    (re.compile(r"appeals? process", re.IGNORECASE), "appeals"),
    (re.compile(r"file a claim|submit your claim|claims submission", re.IGNORECASE), "claims_filing"),
    (re.compile(r"enrollment form|member enrollment", re.IGNORECASE), "enrollment"),
    (re.compile(r"frequently asked questions|faq", re.IGNORECASE), "faq"),
]


def guess_section(text: str) -> str:
    for pattern, label in SECTION_PATTERNS:
        if pattern.search(text):
            return label
    return "general"


def chunk_policy_documents() -> list[dict]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    records = []
    for txt_file in sorted(RAW_TEXT_DIR.glob("*.txt")):
        text = txt_file.read_text(encoding="utf-8")
        meta = SOURCE_META.get(txt_file.name, {"source_type": "unknown", "plan_type": None})

        chunks = splitter.split_text(text)
        for i, chunk in enumerate(chunks):
            record = {
                "id": f"{txt_file.stem}_chunk{i:03d}",
                "text": chunk,
                "record_type": "policy_text_chunk",
                "source_file": txt_file.name,
                "source_type": meta["source_type"],
                "plan_type": meta["plan_type"],
                "section": guess_section(chunk),
                "chunk_index": i,
                "chunk_size": len(chunk),
            }
            records.append(record)

    return records


def build_plan_summaries() -> list[dict]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.execute("SELECT * FROM plans")
    rows = cur.fetchall()
    conn.close()

    records = []
    for row in rows:
        text = (
            f"{row['plan_name']} is a {row['plan_type']} plan in the {row['tier']} tier. "
            f"Monthly premium: ${row['monthly_premium']:.2f}. "
            f"Annual deductible: ${row['deductible']:.0f}. "
            f"Out-of-pocket maximum: ${row['out_of_pocket_max']:.0f}."
        )
        record = {
            "id": f"plan_{row['plan_id']}",
            "text": text,
            "record_type": "plan_summary",
            "source_file": "data/plans.csv",
            "source_type": "structured_plan_data",
            "plan_type": row["plan_type"],
            "section": "plan_overview",
            "chunk_index": 0,
            "chunk_size": len(text),
        }
        records.append(record)

    return records


def sanity_check(records: list[dict]) -> None:
    exclusion_chunks = [r for r in records if r["section"] == "exclusions"]
    print(f"\nSanity check: {len(exclusion_chunks)} chunk(s) tagged as 'exclusions'")
    for r in exclusion_chunks:
        print(f"  - [{r['id']}] {r['text'][:120]!r}...")

    total_chunks = len(records)
    avg_len = sum(r["chunk_size"] for r in records) / total_chunks if total_chunks else 0
    print(f"\nTotal records: {total_chunks}")
    print(f"Average chunk size: {avg_len:.0f} chars")

    by_type = {}
    for r in records:
        by_type[r["record_type"]] = by_type.get(r["record_type"], 0) + 1
    print(f"Record type breakdown: {by_type}")


def main() -> None:
    policy_records = chunk_policy_documents()
    plan_records = build_plan_summaries()

    all_records = policy_records + plan_records

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        for record in all_records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Wrote {len(all_records)} records to {OUT_PATH}")
    print(f"  - {len(policy_records)} policy text chunks")
    print(f"  - {len(plan_records)} plan summary records")

    sanity_check(all_records)


if __name__ == "__main__":
    main()