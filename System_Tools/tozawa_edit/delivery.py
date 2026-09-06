"""別PCで専用編集ツールを開ける検収セットを作る。認証・履歴・キャッシュは収録しない。"""
import argparse,hashlib,json,os,subprocess,zipfile
from pathlib import Path

def digest(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()

def main():
 p=argparse.ArgumentParser();p.add_argument('work',type=Path);p.add_argument('--tools',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();w=a.work.resolve();tools=a.tools.resolve();a.out.mkdir(exist_ok=True,parents=True)
 gate=w/'check/GATE.md'
 if not gate.exists():raise SystemExit('検収シート・検査結果が必要')
 doc=json.loads((w/'shots.json').read_text());video=w/'out.mp4'
 if not video.exists():video=w/'確認用_下書き.mp4'
 if not video.exists():raise SystemExit('動画なし')
 for s in doc['shots']:
  for field in ('asset_file','background_file'):
   if s.get(field) and not (w/s[field]).is_file():raise SystemExit('素材不足 '+s[field])
 prefix='Tozawa_Edit/'
 instructions='''# 別のパソコンで編集を確認する\n\nGitHubに本人のアカウントでログインし、戸沢村の下書きReleaseから Tozawa_Edit_Materials.zip と Tozawa_Edit_Review.zip を両方ダウンロードしてください。両方の中にある Tozawa_Edit フォルダを同じ場所へ展開・統合します。フォルダ全体を移動でき、元のパソコンの絶対パスは不要です。\n\nMacは「編集を開く.command」、Windowsは「編集を開く.bat」を開きます。Python 3が使えるPCで開いてください。初回は必要なPython環境をセットアップします。専用ツールがブラウザに開き、各カットの調整・再生ができます。既存の専用ツールからこの素材フォルダを指定しても構いません。\n\nAIへの修正依頼には、そのPC側のCodexログインが必要です。閲覧と手動調整に生成APIキーは不要です。追加の有料生成は操作しない限り発注しません。\n\n動画をすぐ見る場合は out.mp4（無い場合は確認用_下書き.mp4）。全カット一覧は check/sheet.html です。機械音声の確認版であり、本人の最終確認は未実施。未完了の演出と確認ポイントは編集確認メモ.md、自動検査はcheck/GATE.mdを参照してください。\n'''
 launcher='''#!/bin/zsh
set -e
cd "$(dirname "$0")"
if [[ ! -x .venv-edit/bin/python ]]; then
  python3 検収環境を準備.py
fi
.venv-edit/bin/python System_Tools/edit/open_editor.py . --port 8795
'''
 bat='''@echo off\r\nchcp 65001 >nul\r\ncd /d "%~dp0"\r\nif not exist ".venv-edit\\Scripts\\python.exe" (\r\n  py -3 検収環境を準備.py\r\n  if errorlevel 1 (pause & exit /b 1)\r\n)\r\n.venv-edit\\Scripts\\python.exe System_Tools\\edit\\open_editor.py . --port 8795\r\npause\r\n'''
 (w/'別PCで確認する.md').write_text(instructions)
 entries={}
 def add(z,src,rel):
  z.write(src,prefix+rel);entries[rel]={'bytes':src.stat().st_size,'sha256':digest(src)}
 material_paths=sorted({w/s[k] for s in doc['shots'] for k in ('asset_file','background_file') if s.get(k)})
 material_paths += list((w/'地形図').glob('*.json'))
 material_paths += [w/doc['audio'],w/'音声/仮ナレーション_Kyoko.wav']
 if (w/'音声/終章BGM.mp3').exists():material_paths.append(w/'音声/終章BGM.mp3')
 material_paths += list((w/'画像/キャライラスト').glob('*.png'))
 archives=[]
 for name,group in [('Tozawa_Edit_Materials.zip',list(dict.fromkeys(material_paths))),('Tozawa_Edit_Review.zip',[])]:
  target=a.out/name
  with zipfile.ZipFile(target,'w',zipfile.ZIP_STORED,allowZip64=True) as z:
   for src in group:add(z,src,str(src.relative_to(w)))
   if not group:
    for fname in ['shots.json','asr.json','Master.md','Asset_Prompts_Full.md','編集用素材台本.md','編集確認メモ.md','別PCで確認する.md','Image_Completion_Manifest.json','音声/仮音声_生成時刻.json','音声/音響編集記録.md','音声/音量検査.txt','画像目視確認記録.md','編集目視確認記録.md']:
     src=w/fname
     if src.exists():add(z,src,fname)
    add(z,video,video.name)
    for src in (w/'check').rglob('*'):
     if src.is_file() and src.suffix in ('.html','.css','.js','.jpg','.png','.mp4','.json','.md','.txt') and not src.name.endswith('.source.json'):
      rel=str(src.relative_to(w))
      if src.name=='last_video.txt':z.writestr(prefix+rel,video.name+'\n')
      else:add(z,src,rel)
    for src in tools.rglob('*'):
     if src.is_file() and '__pycache__' not in src.parts and src.suffix in ('.py','.md','.js','.css','.command','.bat','.svg'):
      add(z,src,'System_Tools/edit/'+str(src.relative_to(tools)))
    for src in [x for x in Path(__file__).resolve().parent.iterdir() if x.suffix in ('.py','.md')]:
     add(z,src,'System_Tools/tozawa_edit/'+src.name)
    z.writestr(prefix+'検収環境を準備.py', 'import sys\nsys.path.insert(0, \"System_Tools/edit\")\nimport setup\nsys.exit(0 if setup.setup_venv() and setup.setup_fonts() else 1)\n')
    z.writestr(prefix+'編集を開く.bat',bat)
    zi=zipfile.ZipInfo(prefix+'編集を開く.command');zi.external_attr=0o755<<16;z.writestr(zi,launcher)
    z.writestr(prefix+'編集セット対応表.json',json.dumps(entries,ensure_ascii=False,indent=2))
  with zipfile.ZipFile(target) as z:
   bad=z.testzip()
   if bad:raise RuntimeError('ZIP破損 '+bad)
  archives.append({'name':name,'bytes':target.stat().st_size,'sha256':digest(target)})
  print('保存',name,round(target.stat().st_size/1e6),'MB',flush=True)
 manifest={'project':w.name,'video':video.name,'gate':gate.read_text().splitlines()[0],'human_review':'pending','packages':archives}
 (w/'編集セット保存記録.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(manifest,ensure_ascii=False))
if __name__=='__main__':main()
