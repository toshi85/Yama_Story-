import subprocess,sys,json,datetime,hashlib
from pathlib import Path
p=Path(__file__).parent
cmd=[sys.executable,str(p/'analyze_single_attempt.py'),'--url','https://www.youtube.com/watch?v=1TyA4Vxy7pE','--duration','530','--out',str(p/'1TyA4Vxy7pE_resume_gemini.json')]
s=p/'1TyA4Vxy7pE_resume_execution.json'
d={'command':cmd,'started_at':datetime.datetime.now().astimezone().isoformat(),'input_sha256':hashlib.sha256(Path(cmd[1]).read_bytes()).hexdigest(),'status':'running','retry_basis':'Official AI Studio status observed All Systems Operational on 2026-09-08; one request only','next':'Check AV coverage and full transcript before further videos'}
s.write_text(json.dumps(d,ensure_ascii=False,indent=2))
r=subprocess.run(cmd)
d.update(exit_code=r.returncode,finished_at=datetime.datetime.now().astimezone().isoformat(),status='output_ready' if r.returncode==0 else 'needs_review')
s.write_text(json.dumps(d,ensure_ascii=False,indent=2))
