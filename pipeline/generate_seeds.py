"""
SynthEngine — Scene Seed Generator (Module 1)
Generates structured edge case scene parameters based on physical boundary conditions.

Output: seeds_pool.json — structured scene seed pool
"""

import json, os, uuid, logging
from datetime import datetime
from typing import Optional

log = logging.getLogger("synth-seeds")

# Scene categories with physical parameter ranges
SCENE_TEMPLATES = {
    "autonomous_driving": [
        {
            "scene_id": "driving_extreme_rain_001",
            "category": "adverse_weather",
            "description": "暴雨夜間行車 — 能見度低於50米，路面積水",
            "parameters": {
                "rain_intensity": {"min": 0.8, "max": 1.0, "unit": "relative"},
                "wetness": {"min": 0.9, "max": 1.0},
                "fog_density": {"min": 0.3, "max": 0.6},
                "sun_altitude": -5,
                "time_of_day": "night",
                "visibility_meters": {"min": 30, "max": 50}
            },
            "trigger": "前車突然剎車 + 路面標線模糊"
        },
        {
            "scene_id": "driving_ghost_pedestrian_001",
            "category": "unexpected_obstacle",
            "description": "市區窄路 — 行人從停泊車輛之間突然衝出",
            "parameters": {
                "vehicle_speed_kmh": {"min": 40, "max": 60},
                "pedestrian_speed_ms": {"min": 4, "max": 6},
                "occlusion_angle_deg": {"min": 25, "max": 45},
                "road_width_m": {"min": 6, "max": 10}
            },
            "trigger": "行人從視線盲區鬼探頭式衝出"
        },
        {
            "scene_id": "driving_cargo_drop_001",
            "category": "falling_object",
            "description": "高速公路 — 前車掉落大型貨物",
            "parameters": {
                "speed_kmh": 80,
                "object_size_m": {"min": 0.8, "max": 1.5},
                "object_weight_kg": {"min": 50, "max": 200},
                "distance_to_impact_m": {"min": 15, "max": 30}
            },
            "trigger": "前車貨物綁紮鬆脫，瞬間跌落路面"
        },
        {
            "scene_id": "driving_motorcycle_cutin_001",
            "category": "aggressive_cut_in",
            "description": "電單車在車流中突然切入本車前方",
            "parameters": {
                "motorcycle_speed_kmh": {"min": 60, "max": 80},
                "cut_in_distance_m": {"min": 5, "max": 15},
                "relative_angle_deg": {"min": 20, "max": 40}
            },
            "trigger": "外賣電單車在視線死角超速切入"
        }
    ],
    "home_robot": [
        {
            "scene_id": "home_fragile_grasp_001",
            "category": "fragile_object_handling",
            "description": "機械臂抓取易碎玻璃杯 — 需精準力控",
            "parameters": {
                "object_material": "glass",
                "wall_thickness_mm": {"min": 1.5, "max": 3.0},
                "fill_level_pct": {"min": 30, "max": 100},
                "surface_friction": {"min": 0.2, "max": 0.5}
            },
            "trigger": "機械臂需以 <2N 力控抓取，防止夾碎"
        },
        {
            "scene_id": "home_pet_avoidance_001",
            "category": "sudden_obstacle",
            "description": "寵物突然穿越機器人路徑",
            "parameters": {
                "pet_speed_ms": {"min": 3, "max": 6},
                "pet_mass_kg": {"min": 3, "max": 12},
                "reaction_time_s": 0.05,
                "floor_friction": {"min": 0.3, "max": 0.7}
            },
            "trigger": "機械臂需在 0.05 秒內觸發緊急制動"
        },
        {
            "scene_id": "home_child_safety_001",
            "category": "child_protection",
            "description": "兒童在高溫危險源附近 — 需安全推理",
            "parameters": {
                "hazard_temp_c": {"min": 80, "max": 200},
                "child_distance_m": {"min": 0.5, "max": 2.0},
                "surface_instability": {"min": 0.3, "max": 0.7}
            },
            "trigger": "偵測到高溫危險 + 兒童接近 → 啟動保護 CoT"
        }
    ]
}


def generate_seeds_pool(output_path: str = "config/seeds_pool.json", count: Optional[int] = None) -> dict:
    """Generate the complete seeds pool from templates."""
    seeds_pool = {
        "metadata": {
            "version": "1.0",
            "generated_at": datetime.now().isoformat(),
            "total_scenes": 0
        },
        "seeds": []
    }

    scene_id_counter = 0
    for category, scenes in SCENE_TEMPLATES.items():
        for scene in scenes:
            seeds_pool["seeds"].append(scene)
            scene_id_counter += 1

    seeds_pool["metadata"]["total_scenes"] = scene_id_counter
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(seeds_pool, f, indent=2, ensure_ascii=False)

    log.info(f"✅ Generated {scene_id_counter} seed scenes → {output_path}")
    return seeds_pool


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    generate_seeds_pool()
