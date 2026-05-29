# SynthEngine — Synthetic Edge Case Data Factory

香港一人公司，專注為自動駕駛及具身智能（Embodied AI）生產高品質 Corner Cases 合成數據集。

## 🚀 Quick Start

### Local Dev
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set your API key
cp .env.example .env
# Edit .env with your DeepSeek API key

# Run data generation
python generate_cot_data.py
```

### RunPod Cloud (SSH)
```bash
# 1. Deploy PyTorch pod on RunPod
# 2. SSH in:
ssh -p YOUR_PORT root@YOUR_POD_IP

# 3. One-command setup:
curl -s https://raw.githubusercontent.com/chouthk/synthengine/main/scripts/setup_runpod.sh | bash

# 4. Generate data:
cd /workspace && python generate_cot_data.py
```

## 📁 Project Structure
```
synthengine/
├── .env.example          # Environment template
├── .gitignore            # Security rules
├── requirements.txt      # Python dependencies
├── setup.py
├── README.md
├── generate_cot_data.py  # Core generation script
├── batch_generate.py     # Batch production pipeline
├── scripts/
│   └── setup_runpod.sh   # One-click RunPod setup
├── data/
│   ├── raw/              # Raw generated JSONL
│   └── compressed/       # Compressed .parquet/.tar.gz
└── config/
    └── scenarios.yaml    # Scene definitions
```

## 🧠 Supported Models
- DeepSeek-V3 / DeepSeek-R1 (recommended for HK, no region lock)
- OpenAI GPT-4o / GPT-4o-mini
- SiliconFlow hosted models
