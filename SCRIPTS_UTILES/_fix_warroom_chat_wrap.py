import os

with open('WAR_ROOM_EXECUTIVE.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_css = """.chat-msg {
      display: flex;
      gap: 8px;
      line-height: 1.5;
    }"""

new_css = """.chat-msg {
      display: block;
      gap: 8px;
      line-height: 1.5;
      word-break: break-word;
      white-space: pre-wrap;
    }"""

if old_css in content:
    content = content.replace(old_css, new_css)
    print("SUCCESS: Updated .chat-msg CSS styling!")

with open('WAR_ROOM_EXECUTIVE.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: Saved WAR_ROOM_EXECUTIVE.html!")
