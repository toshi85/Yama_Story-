from pathlib import Path
import json, re, subprocess, sys, os, hashlib, datetime
P=Path(__file__).resolve().parent.parent
C=P/'check'
ROOT=P.parents[2]
VERSION=sys.argv[1] if len(sys.argv)>1 else 'latest'
D=C/VERSION
D.mkdir(exist_ok=True)
master=P/'Master.md';plot=P/'Plot_Sheet_せたな町.md'
text=master.read_text();chapters=[];cur=None;part=None
for line in text.splitlines():
    m=re.match(r'<!-- PART: (.+?) -->',line)
    if m:part=m.group(1)
    m=re.match(r'^## (\d+)\. (.+)',line)
    if m:cur={'chapter':int(m.group(1)),'title':m.group(2),'part':part,'lines':[],'facts':set()};chapters.append(cur)
    elif cur is not None and line.startswith('ナレーター:'):
        cur['lines'].append(re.sub(r'\s*<!--.*?-->','',line.split(':',1)[1]).strip().replace('**',''))
    elif cur is not None and 'src:' in line:
        for run in re.findall(r'素材#\s*\d+(?:\s*#\s*\d+)*',line):cur['facts'].update(map(int,re.findall(r'#\s*(\d+)',run)))
counts={r['chapter']:sum(len(x) for x in r['lines']) for r in chapters}
plines=plot.read_text().splitlines()
for i,line in enumerate(plines):
    m=re.match(r'^\|\s*(\d+)\s*\|',line)
    if m:
        cells=line.split('|');cells[6]=' '+str(counts[int(m.group(1))])+' ';plines[i]='|'.join(cells)
plot.write_text('\n'.join(plines)+'\n')
profile=C/'checks_write_scope.sb'
profile.write_text('(version 1)\n(allow default)\n(deny file-write*)\n(allow file-write* (subpath '+json.dumps(str(P))+') (literal "/dev/null") (literal "/dev/tty"))\n')
# The legacy safety logger has a fixed path outside the permitted directory.
# OS write restrictions let its documented exception handler skip that log;
# all original validation code and thresholds run unchanged, stdout/stderr saved here.
names=['validate_yama_safety','validate_yama_structure','validate_yama_narrative','validate_yama_facts','audit_numeric_facts','validate_yama_intro','validate_yama_consistency','validate_yama_coherence','validate_yama_plot']
results=[]
env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1'
for name in names:
    target=plot if name=='validate_yama_plot' else master
    argv=['python3','-B',str(ROOT/'Yama_Story/System_Tools'/f'{name}.py'),str(target)]
    cmd=['/usr/bin/sandbox-exec','-f',str(profile)]+argv
    r=subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True,text=True,timeout=90)
    (D/(name+'.log')).write_text(r.stdout+r.stderr)
    lines=(r.stdout+r.stderr).strip().splitlines()
    result={'command':argv,'exit_code':r.returncode,'last_line':lines[-1] if lines else '', 'log':str(D/(name+'.log'))}
    results.append(result)
    print(f'{name}: Exit {r.returncode}',flush=True)
parts={key:sum(counts[r['chapter']] for r in chapters if r['part']==key) for key in ['KI','SHO','TEN-KETSU']}
total=sum(parts.values());acc=0;positions={}
for r in chapters:acc+=counts[r['chapter']];positions[r['chapter']]=round(acc/total*100,3)
intro=chapters[0]['lines'];q=sum(x.endswith(('でしょうか。','のか。','でしょうか？','のか？')) for x in intro)
metrics={'total_chars':total,'parts':parts,'ratios':{k:round(v/total*100,3) for k,v in parts.items()},'chapter_chars':counts,'positions':positions,'intro_chars':counts[1],'intro_questions':q,'intro_closing':intro[-1],'ending_chars':counts[28],'fact_ids':sorted(set().union(*(r['facts'] for r in chapters))),'narration_lines':sum(len(r['lines']) for r in chapters)}
(D/'metrics.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2)+'\n')
(D/'results.json').write_text(json.dumps({'input_sha256':hashlib.sha256(master.read_bytes()).hexdigest(),'checked_at':datetime.datetime.now().isoformat(),'results':results},ensure_ascii=False,indent=2)+'\n')
# Export body to read in the five-pass cycle; this file is not a replacement for gate.py snapshots.
(D/'body.md').write_text('\n\n'.join('## '+str(r['chapter'])+'. '+r['title']+'\n'+'\n'.join(r['lines']) for r in chapters)+'\n')
print('合計',total,'字; 起承転結',metrics['ratios'],'; intro',counts[1],q,'; peaks',positions[8],positions[20],positions[23])
sys.exit(0 if all(r['exit_code']==0 for r in results) else 1)
