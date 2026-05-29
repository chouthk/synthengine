---
license: mit
language:
  - en
  - zh
tags:
  - autonomous-driving
  - robotics
  - edge-cases
  - corner-cases
  - synthetic-data
  - chain-of-thought
  - embodied-ai
datasets:
  - SynthEngine/Autonomous-Driving-Corner-Cases-Bait-v1
---

# SynthEngine — Autonomous Driving Corner Cases

## 📊 Dataset Overview

**High-quality synthetic edge case data for autonomous driving and embodied AI.**

| Property | Value |
|----------|-------|
| Total Samples | 2,000 (Bait) / 100,000 (Full) |
| Data Format | JSONL / Parquet |
| Simulator | CARLA 0.9.15 |
| Sensor Suite | Camera (1920x1080), LiDAR (64ch), IMU, GPS |
| Annotation | CoT reasoning + kinematic labels |
| License | MIT (Bait) / Commercial (Full) |

## 🎯 Use Cases

- **Autonomous Driving**: Extreme weather, ghost pedestrians, cargo drops
- **Home Robotics**: Fragile object handling, pet avoidance, child safety
- **Safety Judge Training**: Alignment datasets for safety-critical decisions

## 📁 Data Structure

Each record contains:
- `scenario_id`: Unique identifier
- `scene_description`: Physical environment description
- `chain_of_thought`: Multi-step reasoning for decision making
- `force_control_action`: Final safe action command
- `kinematic_parameters`: Speed, acceleration, steering angles

## 🚀 Quick Start

```python
import json

# Load the dataset
with open("synthengine_bait_v1.jsonl", "r") as f:
    for line in f:
        data = json.loads(line)
        print(data["scenario_id"], data["chain_of_thought"][:1])
```

## 📈 Quality Metrics

| Metric | Value |
|--------|-------|
| Schema Compliance | 100% |
| CoT Completeness | 100% |
| Multi-modal Sync | <1ms |
| Label Coverage | 99.8% |

## 📬 Contact

For full dataset access: contact@synthengine-data.com
