import requests, re

r = requests.get('https://australdrone.cl', timeout=15)
html = r.text

# Find all script tags with src
scripts = re.findall(r'<script[^>]+src=[^>]+>', html, re.IGNORECASE)
print("=== SCRIPT TAGS ===")
for s in scripts:
    print(s[:200])

# Search specifically for vibe-copilot loader
print("\n=== SEARCHING FOR VIBE-COPILOT or CHATBOT-AD ===")
idx = html.lower().find('vibe-copilot')
if idx >= 0:
    print("FOUND vibe-copilot at char", idx, "->", html[max(0, idx-100):idx+200])
else:
    print("vibe-copilot NOT found in page HTML")

idx2 = html.lower().find('chatbot-ad')
if idx2 >= 0:
    print("FOUND chatbot-ad at char", idx2, "->", html[max(0, idx2-100):idx2+200])
else:
    print("chatbot-ad NOT found in page HTML")

# Search for webhook
idx3 = html.lower().find('webhook')
if idx3 >= 0:
    print("FOUND webhook at char", idx3, "->", html[max(0, idx3-100):idx3+200])
else:
    print("webhook NOT found in page HTML")
