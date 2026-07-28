fp = r"c:\Users\LyCoNs\Desktop\AI CHABOT\vibe-copilot.js"
with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()
    for idx in range(430, 600):
        if idx < len(lines):
            print(f"L{idx+1}: {lines[idx].strip()}")
