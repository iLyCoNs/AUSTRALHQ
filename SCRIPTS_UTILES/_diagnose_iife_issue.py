import os, re

fp = r"c:\Users\LyCoNs\Desktop\AI CHABOT\vibe-copilot.js"
with open(fp, 'r', encoding='utf-8') as f:
    content = f.read()

# El problema: la funcion _triggerN8nActionEvent no cierra su } antes de })();
# Buscar la funcion y verificar
idx = content.find('async function _triggerN8nActionEvent(eventType, payloadData) {')
if idx >= 0:
    # Encontrar donde esta el cierre del IIFE })();
    iife_end = content.rfind('})();')
    trigger_func_end = content.rfind('}', idx, iife_end)
    print(f"_triggerN8nActionEvent starts at char: {idx}")
    print(f"Last }} before })(); at char: {trigger_func_end}")
    print(f"})(); ends at char: {iife_end}")
    
    # Mostrar las ultimas 200 chars antes de })(); 
    print("\nLast 300 chars before })();:")
    print(content[iife_end-300:iife_end+10])
