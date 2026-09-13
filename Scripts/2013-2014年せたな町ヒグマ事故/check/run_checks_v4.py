from pathlib import Path
import os, sys, subprocess, json, hashlib
P=Path(__file__).resolve().parent.parent
ROOT=P.parents[2]
CHECK=P/'check'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
wrapper="""import builtins,runpy,sys,subprocess
original=builtins.open
log,script,*args=sys.argv[1:]
builtins.open=lambda file,*a,**kw:original(log if str(file).endswith('/Yama_Story/yama_safety_validation.log') else file,*a,**kw)
run=subprocess.run
code='import builtins,runpy,sys; orig=builtins.open; log,script,*args=sys.argv[1:]; builtins.open=lambda file,*a,**kw:orig(log if str(file).endswith("/Yama_Story/yama_safety_validation.log") else file,*a,**kw); sys.argv=[script]+args; runpy.run_path(script,run_name="__main__")'
def safe_run(argv,*a,**kw):
 if isinstance(argv,list) and len(argv)>1 and argv[1].endswith('validate_yama_safety.py'):
  argv=[argv[0],'-B','-c',code,log]+argv[1:]
 return run(argv,*a,**kw)
subprocess.run=safe_run
sys.argv=[script]+args
runpy.run_path(script,run_name='__main__')
"""
results=[]
for name in ['validate_yama_safety','validate_yama_structure','validate_yama_narrative','validate_yama_facts','audit_numeric_facts','validate_yama_intro','validate_yama_consistency','validate_yama_coherence','validate_yama_plot','check_calibration']:
 script=ROOT/'Yama_Story/System_Tools'/f'{name}.py'
 target=[] if name=='check_calibration' else [str(P/('Plot_Sheet_せたな町.md' if name=='validate_yama_plot' else 'Master.md'))]
 argv=[sys.executable,'-B','-c',wrapper,str(CHECK/'v4_safety_append.log'),str(script)]+target
 r=subprocess.run(argv,capture_output=True,text=True)
 log=CHECK/f'v4_{name}.log';log.write_text(r.stdout+r.stderr)
 results.append({'tool':name,'exit':r.returncode,'log':str(log),'argv':argv,'script_sha256':hashlib.sha256(script.read_bytes()).hexdigest()})
 print(name,r.returncode,flush=True)
 if r.returncode:print((r.stdout+r.stderr)[-2600:],flush=True)
(CHECK/'v4_check_results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
