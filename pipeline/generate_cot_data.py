"""
SynthEngine — CoT Data Generator (Module 3)
Generates Chain-of-Thought reasoning data from scene parameters using LLM API.
Previously created as generate_cot_data.py — now integrated into pipeline.
"""

import os, json, logging, time
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field
from tenacity import retry, stop_after_attempt, wait_random_exponential

load_dotenv()
log = logging.getLogger("synth-cot")

API_KEY = ***"DEEPSEEK_API_KEY") or os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com/v1")
MODEL = "deepseek-chat"

class EdgeCaseData(BaseModel):
    scenario_id: str
    scenario_type: str
    environment_description: str
    chain_of_thought: list[str]
    force_control_action: str
    severity: str = "high"

def load_seeds(seeds_path: str = "config/seeds_pool.json") -> list:
    with open(seeds_path, "r", encoding="utf-8") as f:
        pool = json.load(f)
    log.info(f"📂 Loaded {len(pool['seeds'])} seeds from {seeds_path}")
    return pool["seeds"]

@retry(wait=wait_random_exponential(min=1, max=30), stop=stop_after_attempt(3))
def generate_for_seed(seed: dict) -> dict:
    """Generate CoT data from a single seed."""
    if not API_KEY or "your_" in API_KEY:
        return generate_mock(seed)

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    prompt = f"Generate a detailed edge case scenario for: {seed['description']}. Parameters: {json.dumps(seed['parameters'], ensure_ascii=False)}"

    response = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a synthetic edge case data engineer. Output structured JSON only."},
            {"role": "user", "content": prompt}
        ],
        response_format=EdgeCaseData,
        temperature=0.7,
        max_tokens=2000,
    )
    return json.loads(response.choices[0].message.content)

def generate_mock(seed: dict) -> dict:
    """Mock generator when no API key."""
    return {
        "scenario_id": seed.get("scene_id", f"mock_{int(time.time())}"),
        "scenario_type": seed.get("category", "generic"),
        "environment_description": seed.get("description", ""),
        "chain_of_thought": [
            "1. [感知] 偵測到異常環境變化，啟動高優先級物理推理",
            "2. [分析] 評估邊界參數，計算最佳響應策略",
            "3. [決策] 執行安全優先嘅物理干預動作",
            "4. [驗證] 確認動作執行成功，記錄數據點"
        ],
        "force_control_action": "EXECUTE: 啟動安全干預協議，限制力矩輸出，發出警報",
        "severity": "high"
    }

def generate_batch(seeds: list, output_dir: str = "data/raw", label: str = "v1") -> str:
    """Generate CoT data for all seeds."""
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"synthengine_cot_{label}.jsonl")
    total = len(seeds)
    
    for i, seed in enumerate(seeds):
        try:
            data = generate_for_seed(seed)
            with open(output_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(data, ensure_ascii=False) + "\n")
            log.info(f"  [{i+1}/{total}] ✅ {data.get('scenario_id', 'unknown')}")
        except Exception as e:
            log.error(f"  [{i+1}/{total}] ❌ {e}")
    
    log.info(f"✅ Generated {total} CoT records → {output_file}")
    return output_file

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    seeds = load_seeds()
    generate_batch(seeds)
