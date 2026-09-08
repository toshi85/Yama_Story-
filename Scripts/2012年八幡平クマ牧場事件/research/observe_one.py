import sys,subprocess,json,datetime,hashlib
from pathlib import Path
p=Path(__file__).parent
v,d=sys.argv[1:3]
cmd=[sys.executable,'.codex/skills/video-reference-analysis/scripts/analyze.py','--url','https://www.youtube.com/watch?v='+v,'--duration',d,'--out',str(p/(v+'_gemini.json'))]
state={'command':cmd,'started_at':datetime.datetime.now().astimezone().isoformat(),'input_sha256':hashlib.sha256(Path(cmd[1]).read_bytes()).hexdigest(),'output':str(p/(v+'_gemini.json')),'status':'running','next':'Codex reads and checks AV transcript and competition report'}
s=p/(v+'_execution.json')
s.write_text(json.dumps(state,ensure_ascii=False,indent=2))
with (p/(v+'_gemini.log')).open('w') as f:
 r=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT)
state.update(exit_code=r.returncode,finished_at=datetime.datetime.now().astimezone().isoformat(),status='output_ready' if r.returncode==0 else 'needs_review')
s.write_text(json.dumps(state,ensure_ascii=False,indent=2))
