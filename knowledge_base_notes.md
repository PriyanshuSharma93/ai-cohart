# Knowledge Base Notes — Day 6

## What this builds

`build_knowledge_base.py` reads:
- `raw_text/*.txt` (Day 5 extracted policy documents)
- `coverage.db` plans table (Day 4 structured data)

...and writes a single unified `knowledge_base.jsonl` — one JSON object per
line, ready to be embedded in a later day.

## Chunking strategy

Policy text is split with **`RecursiveCharacterTextSplitter`**
(`langchain-text-splitters`), using:
- `chunk_size=500`
- `chunk_overlap=50`
- separators tried in order: `\n\n`, `\n`, `. `, ` `, `""`

Recursive splitting tries to break on paragraph boundaries first, then
sentences, then words — only falling back to a hard character cut if
nothing else fits. This keeps most chunks semantically coherent instead of
slicing mid-sentence.

The 50-character overlap means each chunk carries a bit of the previous
chunk's tail, protecting against a key fact landing right at a chunk
boundary and getting orphaned from its context.

## Metadata attached to every chunk

| Field | Purpose |
|---|---|
| `id` | unique id, e.g. `benefits_chunk002` |
| `record_type` | `policy_text_chunk` or `plan_summary` |
| `source_file` | which raw file the chunk came from |
| `source_type` | document category |
| `plan_type` | e.g. `PPO`, or `null` if not plan-specific |
| `section` | heuristic label (`exclusions`, `prior_authorization`, etc.) |
| `chunk_index` | position within its source document |
| `chunk_size` | character length |

## Unifying structured + unstructured data

Day 4's `plans` table rows are turned into short natural-language summary
chunks using the same JSONL schema (`record_type: plan_summary`), so
downstream retrieval doesn't need to know whether a fact came from SQL or
a PDF.

## Sanity check: exclusion clause coherence

The exclusions section in `benefits.txt` landed entirely in one chunk, not
split across two, because paragraph-level separators were tried before
falling back to word-level splitting.

## Run it

\`\`\`bash
pip install langchain-text-splitters
python build_knowledge_base.py
\`\`\`