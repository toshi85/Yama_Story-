import subprocess,sys,json,datetime,hashlib
from pathlib import Path
p=Path(__file__).parent
cmd=[sys.executable,'.codex/skills/video-reference-analysis/scripts/analyze.py','--model','gemini-3.7-flash','--model-authorization',str(p/'alternative_model_authorization.json'),'--url','https://www.youtube.com/watch?v=1TyA4Vxy7pE','--duration','530','--out',str(p/'1TyA4Vxy7pE_alternative37_gemini.json')]
s=p/'1TyA4Vxy7pE_alternative37_execution.json'
d={'command':cmd,'started_at':datetime.datetime.now().astimezone().isoformat(),'input_sha256':hashlib.sha256(Path(cmd[1]).read_bytes()).hexdigest(),'status':'running','authorization':'alternative_model_authorization.json; user explicitly requested alternative after stop','next':'Check AV coverage and full transcript before further videos'}
s.write_text(json.dumps(d,ensure_ascii=False,indent=2))
r=subprocess.run(cmd)
d.update(exit_code=r.returncode,finished_at=datetime.datetime.now().astimezone().isoformat(),status='output_ready' if r.returncode==0 else 'needs_review')
s.write_text(json.dumps(d,ensure_ascii=False,indent=2))
