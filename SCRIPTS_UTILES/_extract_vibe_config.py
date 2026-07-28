import requests, json, re

r = requests.get('https://australdrone.cl', timeout=15)
html = r.text
start = html.find('window.VibeCopilotConfig = {')
if start >= 0:
    end = html.find('</script>', start)
    block = html[start:end].strip()
    # Write to file to avoid encoding issues
    with open('SCRIPTS_UTILES/_vibe_config_extracted.txt', 'w', encoding='utf-8') as f:
        f.write(block[:3000])
    print("WRITTEN TO _vibe_config_extracted.txt")
    # Extract telegramToken and telegramChatId
    tg_token_match = re.search(r'"telegramToken"\s*:\s*"([^"]+)"', block)
    tg_chat_match = re.search(r'"telegramChatId"\s*:\s*"([^"]+)"', block)
    webhook_match = re.search(r'"webhookUrl"\s*:\s*"([^"]+)"', block)
    print("WEBHOOK URL:", webhook_match.group(1) if webhook_match else "NOT FOUND")
    print("TELEGRAM TOKEN:", tg_token_match.group(1)[:20] + "..." if tg_token_match else "NOT FOUND")
    print("TELEGRAM CHAT ID:", tg_chat_match.group(1) if tg_chat_match else "NOT FOUND")
