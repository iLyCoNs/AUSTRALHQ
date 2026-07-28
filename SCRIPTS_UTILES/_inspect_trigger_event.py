import os

fp = r"c:\Users\LyCoNs\Desktop\AI CHABOT\vibe-copilot.js"
with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()
    for idx, line in enumerate(lines):
        if 'function _triggern8nactionevent' in line.lower() or 'webhookurl' in line.lower() or '_triggern8nactionevent' in line.lower():
            print(f"L{idx+1}: {line.strip()}")
