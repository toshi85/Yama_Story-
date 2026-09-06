"""全編の自動検査後、検収セットを既存の下書きReleaseへ保存する。"""
import argparse,datetime,json,os,shutil,subprocess,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
GH=shutil.which('gh') or ('/opt/homebrew/bin/gh' if Path('/opt/homebrew/bin/gh').exists() else 'gh')

def run(args,**kwargs):return subprocess.run([str(x) for x in args],check=True,**kwargs)
def main():
 if sys.platform=='darwin':subprocess.Popen(['caffeinate','-is','-w',str(os.getpid())],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 p=argparse.ArgumentParser();p.add_argument('work',type=Path);p.add_argument('--tools',type=Path,required=True);p.add_argument('--repo',type=Path,required=True);p.add_argument('--wait',action='store_true');a=p.parse_args();w=a.work.resolve();repo=a.repo.resolve();state=w/'.editing';state.mkdir(exist_ok=True);out=w/'.imagegen/export'
 def status(stage,**extra):
  v=dict(stage=stage,updated=datetime.datetime.now().astimezone().isoformat(),**extra);temp=state/'delivery_status.tmp';temp.write_text(json.dumps(v,ensure_ascii=False,indent=2));temp.replace(state/'delivery_status.json');print(v,flush=True)
 while a.wait:
  try:s=json.loads((state/'status.json').read_text()).get('stage')
  except Exception:s=None
  if s=='review_ready':break
  status('waiting_for_checks',edit_stage=s);time.sleep(30)
 if not (w/'check/GATE.md').read_text().startswith('PASS'):raise SystemExit('未合格の動画を完成扱いで転送しない')
 # 検査済み動画と検収クリップを保存した後、再生成可能な中間動画だけ整理する。
 for cached in (w/'.render_cache').glob('clip_[0-9]*.mp4'):cached.unlink()
 joined=w/'.render_cache/_joined.mp4'
 if joined.exists():joined.unlink()
 status('packaging')
 run([sys.executable,HERE/'delivery.py',w,'--tools',a.tools,'--out',out])
 status('uploading')
 release='tozawa-images-20260906';remote='toshi85/Yama_Story-'
 manifest=json.loads((w/'編集セット保存記録.json').read_text())
 for package in manifest['packages']:
  before=json.loads(subprocess.check_output([GH,'release','view',release,'--repo',remote,'--json','assets,url']))
  matching=next((x for x in before['assets'] if x['name']==package['name'] and x['size']==package['bytes'] and x.get('digest')=='sha256:'+package['sha256']),None)
  if matching:
   data=before
   continue
  for attempt in range(3):
   try:
    run([GH,'release','upload',release,out/package['name'],'--repo',remote,'--clobber']);break
   except subprocess.CalledProcessError:
    if attempt==2:raise
    status('retry_upload',file=package['name'],attempt=attempt+1);time.sleep(30)
  data=json.loads(subprocess.check_output([GH,'release','view',release,'--repo',remote,'--json','assets,url']))
  asset=next(x for x in data['assets'] if x['name']==package['name'])
  if asset['state']!='uploaded' or asset['size']!=package['bytes'] or asset.get('digest')!='sha256:'+package['sha256']:raise RuntimeError('転送後のSHA-256不一致')
 status('committing_records')
 target=repo/'Scripts'/w.name;target.mkdir(exist_ok=True,parents=True)
 names=['shots.json','asr.json','編集用素材台本.md','編集確認メモ.md','別PCで確認する.md','画像目視確認記録.md','編集セット保存記録.json','check/GATE.md','音声/音響編集記録.md','音声/音量検査.txt','編集目視確認記録.md']
 staged=[]
 for name in names:
  src=w/name
  if src.exists():dst=target/name;dst.parent.mkdir(exist_ok=True,parents=True);shutil.copy2(src,dst);staged.append(str(dst.relative_to(repo)))
 dest=repo/'System_Tools/tozawa_edit';dest.mkdir(exist_ok=True,parents=True)
 for src in [x for x in HERE.iterdir() if x.suffix in ('.py','.md')]:shutil.copy2(src,dest/src.name);staged.append(str((dest/src.name).relative_to(repo)))
 (target/'GitHubで編集を確認.md').write_text('# 編集確認セット\n\n本人のGitHubアカウントでログインして、[下書きRelease]('+data['url']+')を開いてください。`Tozawa_Edit_Materials.zip` と `Tozawa_Edit_Review.zip` を同じ場所へ展開・統合します。`Tozawa_Edit/編集を開く.command`（Mac）または `.bat`（Windows）を開くと専用編集ツールが起動します。\n\n仮の機械音声を使った確認版です。検査結果は `check/GATE.md`、残る演出と確認事項は `編集確認メモ.md` に記録。本人の最終確認は未実施です。\n')
 staged.append(str((target/'GitHubで編集を確認.md').relative_to(repo)))
 run(['git','add','--',*staged],cwd=repo)
 if subprocess.run(['git','diff','--cached','--quiet'],cwd=repo).returncode:
  run(['git','commit','-m','戸沢村の全編確認動画と別PC用編集セットを保存'],cwd=repo)
 try:run(['git','push','origin','HEAD:main'],cwd=repo)
 except subprocess.CalledProcessError:
  run(['git','pull','--rebase','origin','main'],cwd=repo)
  run(['git','push','origin','HEAD:main'],cwd=repo)
 sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()
 actual=subprocess.check_output(['git','ls-remote','origin','refs/heads/main'],cwd=repo,text=True).split()[0]
 if actual!=sha:raise RuntimeError('GitHub mainの反映確認不一致')
 status('uploaded',commit=sha,release=data['url'],human_review='pending')
 run(['osascript','-e','display notification "GitHubへ画像・全編確認動画・別PC用編集セットを保存しました。本人確認待ちです。" with title "戸沢村の編集確認セット"'])
 print('GitHub転送確認済み',data['url'],flush=True)
if __name__=='__main__':
 try:main()
 except Exception as exc:
  if len(sys.argv)>1:
   state=Path(sys.argv[1])/'.editing';state.mkdir(exist_ok=True,parents=True)
   (state/'delivery_status.json').write_text(json.dumps(dict(stage='error',updated=datetime.datetime.now().astimezone().isoformat(),message=str(exc)),ensure_ascii=False,indent=2))
  raise
