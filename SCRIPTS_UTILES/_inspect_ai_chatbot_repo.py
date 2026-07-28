import os

ai_dir = r"c:\Users\LyCoNs\Desktop\AI CHABOT"

for root, dirs, files in os.walk(ai_dir):
    for f in files:
        if f.endswith(('.js', '.json', '.html', '.md')):
            fp = os.path.join(root, f)
            with open(fp, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
                if 'telegram' in content.lower() or 'webhook' in content.lower() or 'onrender' in content.lower() or '8080' in content:
                    print(f"FOUND MATCH IN: {fp}")
