import pathlib, re, subprocess, json, os, sys
P=pathlib.Path(__file__).resolve().parent.parent
s=(P/'Master.md').read_text()
counts={int(m[1]):sum(len(l.removeprefix('ナレーター: ').strip()) for l in m[2].splitlines() if l.startswith('ナレーター:')) for m in re.finditer(r'^## (\d+)\.(.*?)(?=^## \d+\.|\Z)',s,re.M|re.S)}
src={int(m[1]):sorted(set(map(int,re.findall(r'#(\d+)',m[2])))) for m in re.finditer(r'^## (\d+)\.(.*?)(?=^## \d+\.|\Z)',s,re.M|re.S)}
plot=(P/'Plot_Sheet_せたな町.md').read_text()
def row(m):
 a=m[0].split('|'); n=int(a[1]); a[6]=' '+str(counts[n])+' ';a[7]=' '+','.join(map(str,src[n]))+' ';return '|'.join(a)
plot=re.sub(r'^\| \d+.*$',row,plot,flags=re.M)
(P/'Plot_Sheet_せたな町.md').write_text(plot)
results=[]
root=next(x for x in P.parents if (x/'System_Tools/review_script_gemini.py').exists())
for tool in ['validate_yama_safety','validate_yama_structure','validate_yama_narrative','validate_yama_facts','audit_numeric_facts','validate_yama_intro','validate_yama_consistency','validate_yama_coherence','validate_yama_plot']:
 target=P/('Plot_Sheet_せたな町.md' if tool.endswith('_plot') else 'Master.md')
 script=root/'Yama_Story/System_Tools'/f'{tool}.py'
 # Redirect only the validator's hardcoded append log, preserving its checks.
 wrapper="import builtins,runpy,sys; original=builtins.open; src,dst,script,target=sys.argv[1:]; builtins.open=lambda file,*a,**kw:original(dst if str(file)==src else file,*a,**kw); sys.argv=[script,target]; runpy.run_path(script,run_name='__main__')"
 argv=['python3','-B','-c',wrapper,str(root/'Yama_Story/yama_safety_validation.log'),str(P/'check/v2_safety_append.log'),str(script),str(target)]
 r=subprocess.run(argv,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
 output=r.stdout+r.stderr
 log=P/'check'/f'v2_{sys.argv[1]}_{tool}.log';log.write_text(output)
 results.append({'tool':tool,'exit':r.returncode,'last':output.strip().splitlines()[-1],'log':str(log),'argv':argv})
 print(tool,r.returncode,results[-1]['last'])
 if r.returncode:print('\n'.join(l for l in output.splitlines() if l.startswith(('  x','  ✗','  ❌','Line ','[Structure','[BLOCKADE]'))))
(P/'check'/f'v2_{sys.argv[1]}_results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
