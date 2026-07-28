import os

fp = r"c:\Users\LyCoNs\Desktop\AI CHABOT\vibe-copilot.js"
with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()
    for idx, line in enumerate(lines):
        if 'prospecto de alta prioridad' in line.lower() or 'score 100' in line.lower() or 'vip_lead_90' in line.lower() or 'telegram' in line.lower():
            print(f"L{idx+1}: {line.strip()[:160]}")
