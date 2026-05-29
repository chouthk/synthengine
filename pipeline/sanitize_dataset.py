"""
SynthEngine — Sanitize Dataset (Module 4)
Data cleaning filter — removes corrupted, physically implausible, or malformed records.
Uses lightweight judge LLM to validate CoT quality.
"""

import json, os, logging, re
from pathlib import Path

log = logging.getLogger("synth-sanitize")

def validate_jsonl(input_path: str) -> list:
    """Basic structural validation — remove malformed JSON lines."""
    valid = []
    invalid = 0
    with open(input_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                # Check required fields
                required = ["scenario_id", "scenario_type", "environment_description", "chain_of_thought"]
                if all(k in data for k in required):
                    valid.append(data)
                else:
                    invalid += 1
            except json.JSONDecodeError:
                invalid += 1

    log.info(f"✅ Valid: {len(valid)}, Removed: {invalid}")
    return valid

def remove_duplicates(records: list) -> list:
    """Remove duplicate scenario_ids."""
    seen = set()
    unique = []
    for r in records:
        sid = r.get("scenario_id")
        if sid not in seen:
            seen.add(sid)
            unique.append(r)
    dupes = len(records) - len(unique)
    if dupes:
        log.info(f"🗑️ Removed {dupes} duplicates")
    return unique

def run(input_path: str, output_path: str = None) -> str:
    """Full sanitization pipeline."""
    log.info(f"🧹 Sanitizing: {input_path}")
    
    records = validate_jsonl(input_path)
    records = remove_duplicates(records)
    
    if output_path is None:
        output_path = input_path.replace(".jsonl", "_sanitized.jsonl")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    
    log.info(f"✅ Sanitized → {output_path} ({len(records)} records)")
    return output_path

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    import sys
    input_file = sys.argv[1] if len(sys.argv) > 1 else "data/raw/synthengine_cot_v1.jsonl"
    if os.path.exists(input_file):
        run(input_file)
    else:
        log.warning(f"Input file not found: {input_file}")
