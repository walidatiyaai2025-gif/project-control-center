from pathlib import Path
import json,sys
root=Path(__file__).resolve().parents[1]
required=['README.md','START_HERE.md','portfolio/projects.yml','portfolio/priorities.yml','dashboard/index.html']
errors=[]
for p in required:
    if not (root/p).exists(): errors.append(f'missing {p}')
metadata=['PROMPT_ID','VERSION','APPLIES_TO','PREVIOUS_STEP','NEXT_STEP','REQUIRES_WRITE_ACCESS','CONTROL_PLANE_VERSION']
prompts=sorted((root/'prompts').glob('**/*.md')) if (root/'prompts').exists() else []
for p in prompts:
    text=p.read_text()
    for key in metadata:
        if f'{key}:' not in text: errors.append(f'{p.relative_to(root)} missing {key}')
for p in ['portfolio/projects.yml','portfolio/priorities.yml']:
    try: json.loads((root/p).read_text())
    except Exception as e: errors.append(f'{p} invalid JSON-compatible YAML: {e}')
print(f'prompts={len(prompts)} errors={len(errors)}')
for e in errors: print('ERROR',e)
sys.exit(1 if errors else 0)
