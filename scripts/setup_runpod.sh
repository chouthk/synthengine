#!/bin/bash
# SynthEngine — One-click RunPod setup script
# Run this on a fresh RunPod PyTorch pod:
#   curl -s https://raw.githubusercontent.com/chouthk/synthengine/main/scripts/setup_runpod.sh | bash

set -e

echo "============================================"
echo " 🚀 SynthEngine — RunPod Environment Setup"
echo "============================================"

echo ""
echo "📦 Installing Python packages..."
pip install -q openai pydantic python-dotenv tenacity pyyaml jsonschema
echo "✅ Packages installed"

echo ""
echo "📁 Creating project structure..."
mkdir -p /workspace/data/raw /workspace/data/compressed /workspace/config
echo "✅ Directories ready"

echo ""
echo "📝 Creating .env template..."
cat > /workspace/.env << 'EOF'
DEEPSEEK_API_KEY=***
OPENAI_BASE_URL=https://api.deepseek.com/v1
LLM_MODEL=deepseek-chat
OUTPUT_DIR=./data/raw
ENV_STATUS=production
EOF
echo "✅ .env created — edit it with your API key: nano /workspace/.env"

echo ""
echo "📝 Creating scenarios config..."
cat > /workspace/config/scenarios.yaml << 'YAMLEOF'
scenarios:
  home_safety:
    description: "Home robot safety edge cases"
    prompts:
      - "嬰兒接近熱水壺"
      - "寵物絆倒電線"
      - "地板積水滑倒風險"
  driving:
    description: "Autonomous driving corner cases"
    prompts:
      - "暴雨夜間鬼探頭"
      - "前車掉落貨物"
      - "大霧中行人衝出"
YAMLEOF
echo "✅ Config created"

echo ""
echo "📥 Downloading generate_cot_data.py..."
curl -s -o /workspace/generate_cot_data.py \
  https://raw.githubusercontent.com/chouthk/synthengine/main/generate_cot_data.py
echo "✅ Script downloaded"

echo ""
echo "============================================"
echo " ✅ SynthEngine RunPod Setup Complete!"
echo "============================================"
echo ""
echo "Next steps:"
echo "  1. nano /workspace/.env   # Add your DEEPSEEK_API_KEY"
echo "  2. cd /workspace && python generate_cot_data.py"
echo "  3. For batch: python batch_generate.py --count 100"
echo ""
