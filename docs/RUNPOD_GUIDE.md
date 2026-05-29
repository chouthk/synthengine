# SynthEngine — Complete RunPod Deployment Guide

## Prerequisites
- RunPod account with funded balance
- RTX 4090 pod: `clear_yellow_ocelot` (or create new one)
- DeepSeek API Key ready

---

## Step 1: Start the RunPod Pod

1. Go to https://www.runpod.io/console/pods
2. Find `clear_yellow_ocelot` (or create new: RTX 4090, PyTorch template)
3. Click ▶ **Start** if stopped
4. Wait for green **Running** status
5. Click **Connect** → **Web Terminal**

---

## Step 2: One-Command Setup

Copy and paste this ENTIRE block into the RunPod web terminal:

```bash
# ===== SynthEngine Auto-Setup =====
echo "🚀 SynthEngine Auto-Setup Starting..."

# Install dependencies
pip install -q openai pydantic tenacity python-dotenv

# Download all pipeline modules
curl -s -O https://raw.githubusercontent.com/chouthk/synthengine/main/pipeline/generate_seeds.py
curl -s -O https://raw.githubusercontent.com/chouthk/synthengine/main/pipeline/generate_trajectories.py
curl -s -O https://raw.githubusercontent.com/chouthk/synthengine/main/pipeline/generate_cot_data.py
curl -s -O https://raw.githubusercontent.com/chouthk/synthengine/main/pipeline/sanitize_dataset.py
curl -s -O https://raw.githubusercontent.com/chouthk/synthengine/main/pipeline/finalize_dataset.py
curl -s -O https://raw.githubusercontent.com/chouthk/synthengine/main/pipeline/verify_data.py
curl -s -O https://raw.githubusercontent.com/chouthk/synthengine/main/pipeline/aggregate_and_analyze.py
curl -s -O https://raw.githubusercontent.com/chouthk/synthengine/main/pipeline/run_pipeline.py

# Create directories
mkdir -p data/raw data/compressed data/output config

# Download seeds
curl -s -o config/seeds_pool.json https://raw.githubusercontent.com/chouthk/synthengine/main/config/seeds_pool.json

# Set DeepSeek API Key
echo 'DEEPSEEK_API_KEY=sk-2b9b6c4becf3ad6d25b4b8a184f21b583a33c2fa' > .env

echo ""
echo "✅ Setup complete!"
echo ""
```

---

## Step 3: Generate First Data Batch

```bash
python pipeline/run_pipeline.py
```

Expected output (5 phases):
```
📋 Phase 1/5: Generating scene seeds...  ✅ 7 seeds
🧠 Phase 2/5: Generating CoT data...    ✅ 7 records
🧹 Phase 3/5: Sanitizing dataset...     ✅ 7 records
📦 Phase 4/5: Finalizing dataset...     ✅ Compressed
✅ Phase 5/5: Verifying & analyzing...  ✅ Reports
🎉 Pipeline Complete!
```

---

## Step 4: Batch Production (24/7 Mode)

```bash
# Generate 1000 data points
python -c "
from pipeline.generate_cot_data import load_seeds, generate_batch
seeds = load_seeds('config/seeds_pool.json')
# Rotate through seeds to generate more variety
for i in range(143):  # 7 seeds * 143 = ~1000 records
    generate_batch(seeds, 'data/raw', f'batch_{i:04d}')
"
```

---

## Step 5: Check Your Data

```bash
# Check raw data
ls -la data/raw/

# Check compressed output
ls -la data/compressed/

# Check quality reports
cat data/output/Kinematics_Validation_Report.txt
cat data/output/SynthEngine_Data_Quality_Report.md
```

---

## 📊 What You Get

After running the pipeline, you'll have:

| Output | Location | Format |
|--------|----------|--------|
| Raw CoT Data | `data/raw/` | JSONL |
| Standard Dataset | `data/compressed/` | JSONL.GZ |
| Premium Dataset | `data/compressed/` | JSONL.GZ |
| Validation Report | `data/output/` | TXT |
| Quality Report | `data/output/` | Markdown |

---

## 💰 Cost Estimate

- RTX 4090: $0.69/hr
- DeepSeek API: ~¥2/100K tokens
- 10,000 records: ~$5-10 total
- Full 100K production run: ~$50-100
