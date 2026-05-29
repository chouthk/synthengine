"""
SynthEngine — Continuous Batch Production Pipeline
====================================================
Runs on RunPod cloud GPU to continuously generate edge case data.
Auto-compresses and prepares data for delivery.

Usage:
    python batch_generate.py --type all --count 1000
    python batch_generate.py --type driving --count 500 --continuous
"""

import os, json, time, gzip, argparse, logging
from datetime import datetime
from pathlib import Path
from generate_cot_data import run_single, OUTPUT_DIR

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("synth-batch")

SCENARIO_TYPES = ["home_safety", "driving"]

def compress_jsonl(jsonl_path: str) -> str:
    """Compress a JSONL file to .gz for delivery."""
    gz_path = jsonl_path + ".gz"
    with open(jsonl_path, "rb") as f_in:
        with gzip.open(gz_path, "wb") as f_out:
            f_out.writelines(f_in)
    os.remove(jsonl_path)
    log.info(f"🗜️ Compressed → {gz_path}")
    return gz_path

def run_pipeline(scenario_types: list[str], count_per_type: int, continuous: bool = False):
    """Main production pipeline."""
    log.info(f"🏭 SynthEngine Batch Pipeline Started")
    log.info(f"   Scenarios: {scenario_types}")
    log.info(f"   Count/type: {count_per_type}")
    log.info(f"   Continuous: {continuous}")

    iteration = 0
    while True:
        iteration += 1
        batch_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        log.info(f"\n{'='*60}")
        log.info(f"📦 Batch #{iteration} | ID: {batch_id}")

        for scenario in scenario_types:
            log.info(f"\n--- {scenario} ---")
            for i in range(count_per_type):
                try:
                    run_single(scenario)
                    log.info(f"   [{i+1}/{count_per_type}] ✅")
                except Exception as e:
                    log.error(f"   [{i+1}/{count_per_type}] ❌ {e}")
                    time.sleep(5)

        # Compress output
        log.info("\n🗜️ Compressing batch output...")
        for f in Path(OUTPUT_DIR).glob("*.jsonl"):
            compress_jsonl(str(f))

        if not continuous:
            break

        log.info(f"⏳ Waiting 60s before next batch...")
        time.sleep(60)

    log.info("🎉 Pipeline complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SynthEngine Batch Pipeline")
    parser.add_argument("--type", "-t", nargs="+", choices=SCENARIO_TYPES + ["all"],
                        default=["all"], help="Scenario types")
    parser.add_argument("--count", "-c", type=int, default=10, help="Scenes per type")
    parser.add_argument("--continuous", action="store_true", help="Run continuously")

    args = parser.parse_args()
    types = SCENARIO_TYPES if "all" in args.type else args.type

    run_pipeline(types, args.count, args.continuous)
