"""
SynthEngine — Finalize Dataset (Module 5)
Converts clean JSONL to high-performance .parquet format.
Packages datasets for B2B delivery (Standard / Premium / Safety Judge).
"""

import json, os, logging, gzip
from pathlib import Path
from datetime import datetime

log = logging.getLogger("synth-finalize")

def to_parquet(input_path: str, output_dir: str = "data/compressed") -> dict:
    """
    Convert sanitized JSONL to compressed Parquet-like format.
    For now: GZip compressed JSONL + metadata.
    Future: fully structured .parquet via pyarrow.
    """
    os.makedirs(output_dir, exist_ok=True)
    base_name = Path(input_path).stem.replace("_sanitized", "")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Read all records
    records = []
    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    
    # Classify by type
    standard = []
    premium = []
    for r in records:
        if r.get("severity") == "critical":
            premium.append(r)
        else:
            standard.append(r)
    
    results = {}
    
    # Standard dataset
    standard_path = os.path.join(output_dir, f"synthengine_dataset_standard_{timestamp}.jsonl.gz")
    with gzip.open(standard_path, "wt", encoding="utf-8") as f:
        for r in standard:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    results["standard"] = standard_path
    log.info(f"📦 Standard dataset: {len(standard)} records → {standard_path}")
    
    # Premium dataset (with CoT)
    premium_path = os.path.join(output_dir, f"synthengine_dataset_premium_{timestamp}.jsonl.gz")
    with gzip.open(premium_path, "wt", encoding="utf-8") as f:
        for r in premium:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    results["premium"] = premium_path
    log.info(f"💎 Premium dataset: {len(premium)} records → {premium_path}")
    
    # Generate metadata
    meta = {
        "dataset": "SynthEngine",
        "version": "1.0",
        "generated_at": datetime.now().isoformat(),
        "total_records": len(records),
        "standard": len(standard),
        "premium": len(premium),
        "files": results
    }
    meta_path = os.path.join(output_dir, "dataset_metadata.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
    log.info(f"📋 Metadata → {meta_path}")
    
    return results

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    import sys
    input_file = sys.argv[1] if len(sys.argv) > 1 else "data/raw/synthengine_cot_v1_sanitized.jsonl"
    if os.path.exists(input_file):
        to_parquet(input_file)
    else:
        log.warning(f"Input file not found: {input_file}")
