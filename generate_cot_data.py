"""
SynthEngine — Core Synthetic Data Generator
=============================================
Generates structured JSONL synthetic edge case data for autonomous driving
and embodied AI training, using DeepSeek/OpenAI compatible APIs.

Usage:
    python generate_cot_data.py                    # Single scene generation
    python generate_cot_data.py --scenario kitchen  # Specific scenario
    python generate_cot_data.py --batch 100         # Batch mode
"""

import os
import json
import argparse
import logging
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field
from tenacity import retry, stop_after_attempt, wait_random_exponential

# ── Configure logging ──
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("synthengine")

# ── Load environment ──
load_dotenv()

# ── Configuration ──
API_KEY = os.getenv("DEEPSEEK_API_KEY") or os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com/v1")
MODEL = os.getenv("LLM_MODEL", "deepseek-chat")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./data/raw")
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))

# ── Scene definitions (from scenarios.yaml equivalent) ──
SCENARIOS = {
    "home": {
        "description": "家用機器人家居安全場景",
        "prompt": "生成一個家用機器人在香港典型住宅中遇到的極端安全場景數據。"
    },
    "kitchen": {
        "description": "廚房高溫危險場景",
        "prompt": "生成一個廚房環境中機器人需防止兒童接觸高溫煮食器具的場景。"
    },
    "driving": {
        "description": "自動駕駛極端天氣場景",
        "prompt": "生成一個暴雨夜間行車中，前車突然掉落障礙物的 corner case 場景。"
    },
    "pedestrian": {
        "description": "鬼探頭場景",
        "prompt": "生成一個市區行車中，行人從視線盲區突然衝出的極端場景。"
    }
}


# ── Pydantic Schema (enforces structured JSON output) ──
class EdgeCaseData(BaseModel):
    """Standard SynthEngine data schema for embodied AI / autonomous driving."""
    scenario_id: str = Field(description="Unique scenario identifier, e.g. home_safe_001")
    scenario_type: str = Field(description="Category: home_safety / driving / pedestrian / kitchen")
    environment_description: str = Field(description="Detailed physical environment description of the edge case")
    chain_of_thought: list[str] = Field(description="Internal reasoning steps the AI/robot should follow")
    force_control_action: str = Field(description="Final safe action command for the robot/vehicle")
    severity: str = Field(default="high", description="Risk severity: low / medium / high / critical")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())


# ── Mock data generator (for testing without API key) ──
def generate_mock(scenario_id: str, scenario_type: str) -> dict:
    """Generate realistic mock data when no API key is configured."""
    mocks = {
        "home_safety": {
            "scenario_id": scenario_id,
            "scenario_type": "home_safety",
            "environment_description": "幼兒（約14個月）正在客廳地板上爬行，距離2米處有一個剛使用完的電熨斗放置在不穩定的矮桌上，電線懸垂至地面。",
            "chain_of_thought": [
                "1. [感知] 檢測到人類幼兒，年齡估計<2歲，移動速度約0.3m/s，方向為西南方。",
                "2. [危險識別] 右前方偵測到高溫物體（電熨斗），底板溫度約180°C，位置不穩定。",
                "3. [風險評估] 電線懸垂，幼兒有85%機率拉扯電線導致熨斗墜落，將造成重度燙傷。",
                "4. [決策] 必須在3秒內干預：先移開電線，再以柔順力控引導幼兒轉向。"
            ],
            "force_control_action": "EXECUTE: 1) 啟動機械臂輕柔地將電線移至幼兒無法觸及範圍。2) 在幼兒前方0.5米處建立物理屏障。3) 向監護人發送語音警報。",
            "severity": "critical"
        },
        "driving": {
            "scenario_id": scenario_id,
            "scenario_type": "driving",
            "environment_description": "暴雨夜間，能見度低於50米，車輛以60km/h行駛於雙線公路。前方15米處一輛貨車突然掉落大型木箱。",
            "chain_of_thought": [
                "1. [感知] 暴雨環境，LiDAR信噪比下降30%，視覺鏡頭受雨滴干擾。",
                "2. [物體檢測] 偵測到未知障礙物（木箱），尺寸約1.2m×0.8m，位於本車行駛路線正前方。",
                "3. [風險評估] 當前速度60km/h，煞停距離需約25米，但障礙物僅15米，無法完全煞停。",
                "4. [決策] 啟動緊急制動＋轉向避讓，同時檢測鄰近車道是否有碰撞風險。"
            ],
            "force_control_action": "EXECUTE: 1) 全力制動（煞車壓力100%）。2) 轉向角度15°向右避讓。3) 同時檢測右側盲點。4) 啟動危險警告燈。",
            "severity": "critical"
        }
    }
    return mocks.get(scenario_type, mocks["home_safety"])


# ── AI call with retry logic ──
@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(MAX_RETRIES))
def generate_scene(prompt: str) -> Optional[str]:
    """Call the AI model to generate structured edge case data."""

    # Fallback to mock if no API key
    if not API_KEY or API_KEY == "***" or "your_" in API_KEY:
        log.info("⚠️ No valid API key — using mock data generator")
        return None

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    response = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": "你是一個專業的合成數據工程師，專注於為自動駕駛和具身智能生成高品質邊緣場景（Edge Case）數據。輸出必須嚴格依照指定的 JSON Schema。"},
            {"role": "user", "content": prompt}
        ],
        response_format=EdgeCaseData,
        temperature=0.7,
        max_tokens=2000,
    )

    return response.choices[0].message.content


def save_to_jsonl(data: dict, filename: str = "synthengine_data.jsonl"):
    """Append a single data point to the JSONL file."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")

    log.info(f"📝 Appended to {filepath}")


def run_single(scenario_type: str = "home_safety"):
    """Generate a single edge case data point."""
    scenario = SCENARIOS.get(scenario_type, SCENARIOS["home"])
    log.info(f"🚀 Generating {scenario['description']}...")

    result = generate_scene(scenario["prompt"])

    if result:
        parsed = json.loads(result)
        log.info(f"✅ AI generated: {parsed.get('scenario_id', 'unknown')}")
    else:
        # Use mock
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        parsed = generate_mock(f"{scenario_type}_{timestamp}", scenario_type)
        log.info(f"✅ Mock generated: {parsed['scenario_id']}")

    # Pretty print
    print(json.dumps(parsed, indent=2, ensure_ascii=False))

    # Save to JSONL
    save_to_jsonl(parsed)
    return parsed


def run_batch(count: int = 10, scenario_type: str = "home_safety"):
    """Generate multiple edge case data points in sequence."""
    log.info(f"🏭 Batch generating {count}x {scenario_type} scenarios...")

    for i in range(count):
        log.info(f"  [{i+1}/{count}] Generating...")
        run_single(scenario_type)

    log.info(f"✅ Batch complete! Generated {count} data points.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SynthEngine Data Generator")
    parser.add_argument("--scenario", "-s", choices=list(SCENARIOS.keys()) + ["home_safety", "driving"],
                        default="home_safety", help="Scenario type")
    parser.add_argument("--batch", "-b", type=int, default=0,
                        help="Batch count (0 = single generation)")
    args = parser.parse_args()

    scenario_map = {
        "home": "home_safety",
        "kitchen": "home_safety",
        "driving": "driving",
        "pedestrian": "driving"
    }
    stype = scenario_map.get(args.scenario, "home_safety")

    if args.batch > 0:
        run_batch(args.batch, stype)
    else:
        run_single(stype)

    log.info("🎉 Done!")
