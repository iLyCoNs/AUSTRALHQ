import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_btn = """  <button onclick="window.openTVSubPlatform()" style="background:linear-gradient(135deg, #0284c7, #66fcf1); color:#000; border:none; padding:4px 12px; border-radius:16px; font-size:9px; font-weight:900; cursor:pointer; display:flex; align-items:center; gap:4px; box-shadow:0 0 12px rgba(102,252,241,0.4); transition:transform 0.15s;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='none'">
    🛸 WAR ROOM 360°
  </button>"""

new_btns = """  <button onclick="window.openTVSubPlatform()" style="background:linear-gradient(135deg, #0284c7, #66fcf1); color:#000; border:none; padding:4px 12px; border-radius:16px; font-size:9px; font-weight:900; cursor:pointer; display:flex; align-items:center; gap:4px; box-shadow:0 0 12px rgba(102,252,241,0.4); transition:transform 0.15s;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='none'">
    🛸 WAR ROOM 360°
  </button>

  <button onclick="window.open('/WAR_ROOM_EXECUTIVE.html','_blank')" style="background:linear-gradient(135deg, #f472b6, #ec4899); color:#fff; border:none; padding:4px 12px; border-radius:16px; font-size:9px; font-weight:900; cursor:pointer; display:flex; align-items:center; gap:4px; box-shadow:0 0 12px rgba(244,114,182,0.4); transition:transform 0.15s;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='none'">
    🚀 WAR ROOM PRO MAX
  </button>"""

if old_btn in content:
    content = content.replace(old_btn, new_btns)
    print("SUCCESS: Added WAR ROOM PRO MAX button to top navbar in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('PHASER_OFFICE.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: Updated index.html and PHASER_OFFICE.html!")
