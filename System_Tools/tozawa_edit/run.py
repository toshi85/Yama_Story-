"""戸沢村の書き出しを常駐実行。段階・実検査・失敗理由を分けて保存する。"""
import argparse,datetime,fcntl,json,os,subprocess,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent

def main():
 if sys.platform=='darwin':subprocess.Popen(['caffeinate','-is','-w',str(os.getpid())],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 p=argparse.ArgumentParser();p.add_argument('work',type=Path);p.add_argument('--tools',type=Path,required=True);p.add_argument('--wait-map-pid',type=int,default=0);p.add_argument('--wait-asr-pid',type=int,default=0);a=p.parse_args();w=a.work.resolve();tools=a.tools.resolve();state=w/'.editing';state.mkdir(exist_ok=True)
 lock=(state/'run.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 def status(stage,**extra):
  v=dict(stage=stage,updated=datetime.datetime.now().astimezone().isoformat(),pid=os.getpid(),**extra);tmp=state/'status.tmp';tmp.write_text(json.dumps(v,ensure_ascii=False,indent=2));tmp.replace(state/'status.json');print(v,flush=True)
 def alive(pid):
  if not pid:return False
  try:os.kill(pid,0);return True
  except ProcessLookupError:return False
 def wait_existing(pid,stage):
  while alive(pid):status(stage);time.sleep(15)
 def command(stage,args,attempts=2,required=True):
  logfile=state/(stage+'.log')
  for trial in range(attempts):
   with logfile.open('a') as log:
    proc=subprocess.Popen([str(x) for x in args],stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
    while proc.poll() is None:
     status(stage,worker_pid=proc.pid,attempt=trial+1,log=logfile.name);time.sleep(15)
   if proc.returncode==0:return True
   status(stage+'_error',exit=proc.returncode,attempt=trial+1,log=logfile.name)
   if trial+1<attempts:time.sleep(30)
  if required:raise RuntimeError(stage+' failed; '+str(logfile))
  return False
 try:
  wait_existing(a.wait_map_pid,'地形映像の生成待ち')
  command('maps',[sys.executable,HERE/'maps.py',w,'--jobs','3'])
  wait_existing(a.wait_asr_pid,'音声の文字起こし待ち')
  if not (w/'asr.json').exists():command('transcribe',[sys.executable,tools/'transcribe.py',w/'音声/仮ナレーション_Kyoko.wav','-o',w/'asr.json'])
  command('sync',[sys.executable,tools/'check_sync.py',w/'shots.json',w/'asr.json'])
  command('render_draft',[sys.executable,tools/'render.py',w/'shots.json','-o',w/'確認用_下書き.mp4','--draft','--jobs','3','--keep-tmp'])
  passed=command('gate_draft',[sys.executable,tools/'gate.py',w/'shots.json',w/'確認用_下書き.mp4'],attempts=1,required=False)
  if not passed:
   status('draft_needs_fix',message='確認用動画と検収シートを保存。GATE未合格。完成とは扱わない。');return 2
  command('render_final',[sys.executable,tools/'render.py',w/'shots.json','-o',w/'out.mp4','--jobs','3','--keep-tmp','--final-preset','fast'])
  command('gate_final',[sys.executable,tools/'gate.py',w/'shots.json',w/'out.mp4'],attempts=1)
  status('review_ready',message='全編の書き出しと自動検査終了。目視検査・GitHub転送は別の状態で管理。')
  return 0
 except Exception as e:
  status('error',message=str(e));return 1
if __name__=='__main__':sys.exit(main())
