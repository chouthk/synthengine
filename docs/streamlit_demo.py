"""SynthEngine — Streamlit Demo Dashboard
B2B facing demo to showcase synthetic edge case data.
Deploy to Vercel or Streamlit Cloud.
Usage: streamlit run streamlit_demo.py
"""
import streamlit as st
import json, random, os
from datetime import datetime

st.set_page_config(page_title="SynthEngine — AI Data Factory", layout="wide")

st.markdown("""
<style>
.big-font { font-size: 38px !important; font-weight: 700; color: #0f172a; }
.metric { background: #f8fafc; border-radius: 8px; padding: 12px; text-align: center; border: 1px solid #e2e8f0; }
.metric .v { font-size: 28px; font-weight: bold; color: #1e40af; }
.metric .l { font-size: 11px; color: #64748b; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">🏭 SynthEngine — AI Data Factory</p>', unsafe_allow_html=True)
st.markdown("High-quality synthetic edge case data for autonomous driving & embodied AI")

# Metrics row
cols = st.columns(4)
metrics = [
    ("10,000+", "Scenes Generated"),
    ("99.8%", "Label Coverage"),
    ("<1ms", "Sync Accuracy"),
    ("50Hz", "Capture Rate"),
]
for i, (v, l) in enumerate(metrics):
    with cols[i]:
        st.markdown(f'<div class="metric"><div class="v">{v}</div><div class="l">{l}</div></div>', unsafe_allow_html=True)

st.markdown("---")

# Demo section
st.subheader("📡 Sample Edge Case — Real-Time Visualization")
col1, col2 = st.columns([3, 2])

with col1:
    scene_type = st.selectbox("Scenario Type", 
        ["暴雨夜間鬼探頭", "前車掉落貨物", "電單車突然切入", "機械臂抓取易碎物", "寵物突然穿越"])
    
    st.markdown("**Sensor Feed Simulation**")
    st.markdown("```")
    st.markdown("Frame   Time    Speed   Steering  Brake   AccelX")
    st.markdown("-----   ----    -----   -------   -----   ------")
    for i in range(10):
        t = i * 0.02
        s = round(60 - i * 4 + random.uniform(-2, 2), 1)
        st.markdown(f"  {i+1:3d}   {t:.2f}s   {s:5.1f}   {random.uniform(-0.3,0.3):+.2f}   {random.uniform(0,0.8):.2f}   {random.uniform(-6,0):+.1f}")
    st.markdown("```")
    
    st.markdown("**🧠 Chain of Thought Reasoning**")
    cot = [
        "1. [感知] 偵測到前方障礙物，距離15米",
        "2. [分析] 當前速度60km/h，剎停距離需25米",
        "3. [決策] 無法完全剎停，啟動緊急制動+轉向避讓",
        "4. [執行] 制動壓力100%，轉向角度15°，檢查盲點",
    ]
    for c in cot:
        st.markdown(f"- {c}")

with col2:
    st.markdown("**📊 Scene Distribution**")
    chart_data = {
        "自動駕駛": 45,
        "家用機器人": 25,
        "工業安全": 15,
        "醫療": 10,
        "其他": 5,
    }
    for label, pct in chart_data.items():
        st.markdown(f"{label}  {pct}%")
        st.progress(pct / 100)
    
    st.markdown("---")
    st.markdown("**📦 Dataset Summary**")
    st.markdown(f"- 🟢 Standard: 8,000 records")
    st.markdown(f"- 💎 Premium CoT: 2,000 records")
    st.markdown(f"- 🔒 Safety Judge: 500 records")
    st.markdown(f"- 📅 Updated: {datetime.now().strftime('%Y-%m-%d')}")

st.markdown("---")
st.markdown("### 📬 聯絡我們")
st.markdown("電郵：**contact@synthengine-data.com**")
st.markdown("🔒 完整 100K Premium CoT Dataset 可供商業授權")
