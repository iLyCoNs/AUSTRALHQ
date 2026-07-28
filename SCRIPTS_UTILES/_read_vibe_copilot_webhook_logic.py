import re

def search_in_file(fp, patterns):
    with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        for idx, line in enumerate(lines):
            for p in patterns:
                if p in line.lower():
                    print(f"[{os.path.basename(fp)} L{idx+1}]: {line.strip()[:180]}")

import os
ai_dir = r"c:\Users\LyCoNs\Desktop\AI CHABOT"
for root, dirs, files in os.walk(ai_dir):
    for file in files:
        if file in ['vibe-copilot.js', 'chat.js', 'log.js']:
            search_in_file(os.path.join(root, file), ['webhook', 'telegram', 'fetch(', 'australhq'])
