import os, re

# Buscar en todos los directorios del Desktop el HTML con VibeCopilotConfig
desktop = r"c:\Users\LyCoNs\Desktop"
bad_token = 'ODk3NzE5NjA0NzpBQUZweFFSU19fZzRQRzBIZXROazIydmdPalF1ZDVLaTlFQQ=='
bad_token_decoded = '8977196047:AAFpxQRS__g4PG0HetNk22vgOjQud5Ki9EA'
good_token = '8977196047:AAFpxQRS__g4pG0HetNk22vgOjqud5Ki9EA'
good_token_b64 = 'ODk3NzE5NjA0NzpBQUZweFFSU19fZzRQRzBIZXROazIydmdPalFF...'  # not needed

files_found = []
for root, dirs, files in os.walk(desktop):
    # Skip node_modules and .git
    dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', 'dist', '.gemini']]
    for f in files:
        if f.endswith(('.html', '.js', '.json')):
            fp = os.path.join(root, f)
            try:
                with open(fp, 'r', encoding='utf-8', errors='ignore') as fh:
                    content = fh.read()
                    if bad_token in content or bad_token_decoded in content or 'VibeCopilotConfig' in content:
                        files_found.append(fp)
                        print(f"FOUND: {fp}")
            except:
                pass

print(f"\nTotal: {len(files_found)} files with VibeCopilotConfig or bad token")
