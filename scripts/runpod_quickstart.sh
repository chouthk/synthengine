#!/bin/bash
# SynthEngine — RunPod Quick Start (2026-05-29)
# 去 RunPod → clear_yellow_ocelot → Connect → Web Terminal
# Copy paste 以下 5 行：

pip install -q openai pydantic tenacity python-dotenv

curl -s -O https://raw.githubusercontent.com/chouthk/synthengine/main/generate_cot_data.py

echo 'DEEPSEEK_API_KEY=sk-2b92a7c12f3f4efea99fb4d5c8aec2fa' > .env

python generate_cot_data.py --scenario driving

echo "✅ 第一批數據已生成！睇下 ./data/raw/ 目錄"
