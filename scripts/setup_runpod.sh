#!/bin/bash
# SynthEngine — One-click RunPod setup with DeepSeek
# Run this on a fresh RunPod PyTorch pod:
#   curl -s https://raw.githubusercontent.com/chouthk/synthengine/main/scripts/setup_runpod.sh | bash

set -e

echo "============================================"
echo " 🚀 SynthEngine — RunPod Environment Setup"
echo "============================================"

# Install packages
pip install -q openai pydantic python-dotenv tenacity

# Create dirs
mkdir -p /workspace/data/raw /workspace/data/compressed /workspace/config

# Download code
curl -s -o /workspace/generate_cot_data.py \
  https://raw.githubusercontent.com/chouthk/synthengine/main/generate_cot_data.py

# Create .env
echo ""
echo "Set your DeepSeek API key:"
echo "  echo 'DEEPSEEK_API_KEY=sk-your-key-here' > /workspace/.env"
echo ""
echo "Then run:"
echo "  cd /workspace && python generate_cot_data.py --scenario driving"
echo "  cd /workspace && python generate_cot_data.py --batch 100"
echo ""
echo "✅ Setup complete!"
