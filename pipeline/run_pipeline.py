"""
SynthEngine — Main Pipeline Orchestrator
Runs the complete data production pipeline end-to-end.
"""

import os, sys, logging, time, json
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")
log = logging.getLogger("synth-orchestrator")

BASE_DIR = Path(__file__).parent.parent

def run():
    log.info("🚀 SynthEngine Pipeline Starting")
    log.info("=" * 60)
    
    # Phase 1: Generate seeds
    log.info("\n📋 Phase 1/5: Generating scene seeds...")
    from pipeline.generate_seeds import generate_seeds_pool
    seeds_path = os.path.join(BASE_DIR, "config", "seeds_pool.json")
    generate_seeds_pool(seeds_path)
    
    # Phase 2: Generate CoT data
    log.info("\n🧠 Phase 2/5: Generating CoT data...")
    from pipeline.generate_cot_data import load_seeds, generate_batch
    seeds = load_seeds(seeds_path)
    cot_output = generate_batch(seeds, os.path.join(BASE_DIR, "data", "raw"))
    
    # Phase 3: Sanitize
    log.info("\n🧹 Phase 3/5: Sanitizing dataset...")
    from pipeline.sanitize_dataset import run as sanitize
    sanitized = sanitize(cot_output, cot_output.replace(".jsonl", "_sanitized.jsonl"))
    
    # Phase 4: Finalize
    log.info("\n📦 Phase 4/5: Finalizing dataset...")
    from pipeline.finalize_dataset import to_parquet
    results = to_parquet(sanitized, os.path.join(BASE_DIR, "data", "compressed"))
    
    # Phase 5: Verify & Analyze
    log.info("\n✅ Phase 5/5: Verifying & analyzing...")
    from pipeline.verify_data import verify_dataset
    verify_dataset(sanitized, os.path.join(BASE_DIR, "data", "output"))
    from pipeline.aggregate_and_analyze import analyze
    analyze(sanitized, os.path.join(BASE_DIR, "data", "output"))
    
    log.info("=" * 60)
    log.info("🎉 Pipeline Complete!")
    log.info(f"   Outputs: {json.dumps(results, indent=2)}")

if __name__ == "__main__":
    run()
