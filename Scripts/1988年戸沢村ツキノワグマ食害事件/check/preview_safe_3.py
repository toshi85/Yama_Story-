"""Run existing preview_cut/render with check-only work files and no cleanup."""
import sys, os, pathlib, types, io, contextlib, subprocess, shutil
sys.dont_write_bytecode=True
os.environ['PYTHONDONTWRITEBYTECODE']='1'
ROOT=pathlib.Path(__file__).resolve().parents[1]
CHECK=ROOT/'check'
REPO=pathlib.Path.cwd()
EDIT=REPO/'System_Tools/edit'
sys.path.insert(0,str(EDIT))
# Refuse Python writes outside check, deletion, and network connections.
def audit(event,args):
 if event=='open':
  path,mode,flags=args
  if isinstance(path,(str,bytes,os.PathLike)) and ((mode and any(x in mode for x in 'wax+')) or flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC)):
   dest=pathlib.Path(os.fsdecode(path)).resolve()
   if not dest.is_relative_to(CHECK):raise PermissionError(f'Outside check: {dest}')
 if event in ('os.remove','os.rmdir'):raise PermissionError('Deletion prohibited')
 if event in ('socket.connect','socket.getaddrinfo'):raise PermissionError('Network prohibited')
sys.addaudithook(audit)
os.remove=lambda *a,**k:None
os.unlink=lambda *a,**k:None
shutil.rmtree=lambda *a,**k:None
import ff, render
from concurrent.futures import ThreadPoolExecutor
render.ProcessPoolExecutor=ThreadPoolExecutor
# Source path stays original, so media/font lookups stay identical.
source=(EDIT/'render.py').read_text()
source=source.replace('base = os.path.dirname(os.path.abspath(args.shots))',f'base = {str(ROOT)!r}')
exec(compile(source,str(EDIT/'render.py'),'exec'),render.__dict__)
render.ProcessPoolExecutor=ThreadPoolExecutor
original=ff.run_hidden
sid=int(sys.argv[1]); work=CHECK/'preview_work_3'/str(sid);work.mkdir(parents=True,exist_ok=True)
# Preserve any prior preview outputs and lock files; use a fresh output directory.
outdir=CHECK/'preview_3';outdir.mkdir(exist_ok=True)
def run(cmd,**kwargs):
 if len(cmd)>1 and cmd[1]==str(EDIT/'render.py'):
  cmd=list(cmd)+['--keep-tmp','--jobs','1']
  stream=io.StringIO();prev=sys.argv;sys.argv=cmd[1:];code=0
  try:
   with contextlib.redirect_stdout(stream),contextlib.redirect_stderr(stream):render.main()
  except SystemExit as e:code=e.code if isinstance(e.code,int) else 1;stream.write(str(e))
  finally:sys.argv=prev
  return subprocess.CompletedProcess(cmd,code,stream.getvalue(),'')
 return original(cmd,**kwargs)
ff.run_hidden=run
source=(EDIT/'preview_cut.py').read_text()
source=source.replace('os.path.join(root, ".preview_shots.json")',repr(str(work/'preview_shots.json')))
source=source.replace('os.path.join(root, ".render_cache_preview")',repr(str(work/'cache')))
source=source.replace('os.path.join(root, "check", "preview")',repr(str(outdir)))
mod=types.ModuleType('safe_preview');mod.__file__=str(EDIT/'preview_cut.py')
exec(compile(source,str(EDIT/'preview_cut.py'),'exec'),mod.__dict__)
sys.argv=[str(EDIT/'preview_cut.py'),str(ROOT),str(sid)]
mod.main()
