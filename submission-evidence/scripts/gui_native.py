"""Native macOS event helper; refuses input unless PacketTracer is foreground.
No security changes, installations, or proprietary file generation.
Coordinates use macOS logical screen points, not Retina pixels.
"""
import ctypes,subprocess,time,json,sys,hashlib
from pathlib import Path
from datetime import datetime
from PIL import Image
R=Path(__file__).resolve().parents[1]
Q=ctypes.CDLL('/System/Library/Frameworks/CoreGraphics.framework/CoreGraphics')
C=ctypes.CDLL('/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation')
class Point(ctypes.Structure): _fields_=[('x',ctypes.c_double),('y',ctypes.c_double)]
Q.CGPreflightPostEventAccess.restype=ctypes.c_bool
Q.CGEventCreateMouseEvent.argtypes=[ctypes.c_void_p,ctypes.c_uint32,Point,ctypes.c_uint32];Q.CGEventCreateMouseEvent.restype=ctypes.c_void_p
Q.CGEventCreateKeyboardEvent.argtypes=[ctypes.c_void_p,ctypes.c_uint16,ctypes.c_bool];Q.CGEventCreateKeyboardEvent.restype=ctypes.c_void_p
Q.CGEventSetFlags.argtypes=[ctypes.c_void_p,ctypes.c_uint64]
Q.CGEventKeyboardSetUnicodeString.argtypes=[ctypes.c_void_p,ctypes.c_ulong,ctypes.POINTER(ctypes.c_uint16)]
Q.CGEventPost.argtypes=[ctypes.c_uint32,ctypes.c_void_p];C.CFRelease.argtypes=[ctypes.c_void_p]
def guard():
 if not Q.CGPreflightPostEventAccess(): raise RuntimeError('Event access unavailable')
 r=subprocess.run(['osascript','-e','tell application "System Events" to get unix id of first application process whose frontmost is true'],capture_output=True,text=True,timeout=8)
 if r.returncode or r.stdout.strip()!='30530':raise RuntimeError('Refusing input; foreground not PacketTracer: '+r.stdout+r.stderr)
def emit(e):Q.CGEventPost(0,e);C.CFRelease(e)
CONTEXT='main'
def click(x,y,absolute=False):
 guard()
 if not absolute and CONTEXT=='main':
  y+=int(ax('get position of button "New" of window 1').strip().split(',')[1])-34
 for typ in [5,1,2]:emit(Q.CGEventCreateMouseEvent(None,typ,Point(x,y),0));time.sleep(.06)
 time.sleep(.25)
def drag(x1,y1,x2,y2):
 guard()
 if CONTEXT=='main':
  delta=int(ax('get position of button "New" of window 1').strip().split(',')[1])-34
  y1+=delta;y2+=delta
 emit(Q.CGEventCreateMouseEvent(None,5,Point(x1,y1),0));time.sleep(.1)
 emit(Q.CGEventCreateMouseEvent(None,1,Point(x1,y1),0));time.sleep(.15)
 for step in range(1,16):
  emit(Q.CGEventCreateMouseEvent(None,6,Point(x1+(x2-x1)*step/15,y1+(y2-y1)*step/15),0));time.sleep(.04)
 emit(Q.CGEventCreateMouseEvent(None,2,Point(x2,y2),0));time.sleep(.7)
def key(code,flags=0):
 guard()
 mods=[]
 for mask,name in [(1048576,'command down'),(131072,'shift down'),(262144,'control down'),(524288,'option down')]:
  if flags & mask:mods.append(name)
 script='tell application "System Events" to tell (first application process whose unix id is 30530) to key code '+str(code)
 if mods:script+=' using {'+', '.join(mods)+'}'
 subprocess.run(['osascript','-e',script],check=True,capture_output=True,text=True,timeout=8)
 time.sleep(.15)
def text(value):
 guard()
 script='tell application "System Events" to tell (first application process whose unix id is 30530) to keystroke '+json.dumps(value)
 subprocess.run(['osascript','-e',script],check=True,capture_output=True,text=True,timeout=10)
 time.sleep(.15)
def paste_button(value,x=1417,y=862):
 guard()
 prior=subprocess.run(['pbpaste'],capture_output=True,timeout=8).stdout
 subprocess.run(['pbcopy'],input=value.encode('utf-8'),check=True,timeout=8)
 ax('click button "Paste" of group 1 of window 1');time.sleep(.6)
 subprocess.run(['pbcopy'],input=prior,check=True,timeout=8)
def ax(statement):
 guard()
 script='tell application "System Events" to tell (first application process whose unix id is 30530) to '+statement
 for attempt in range(3):
  r=subprocess.run(['osascript','-e',script],capture_output=True,text=True,timeout=10)
  if r.returncode==0:return r.stdout
  if attempt<2 and ('-1719' in r.stderr or '-1728' in r.stderr):time.sleep(.35);continue
  raise RuntimeError(r.stderr.strip())
def tab(name):
 ax('click radio button '+json.dumps(name)+' of tab group 1 of window 1');time.sleep(.4)
 try:
  pos=ax('get position of tab group 1 of window 1').strip()
  (R/'logs/current-tab-position.json').write_text(json.dumps({'position':pos,'observed_at':time.time()}))
 except RuntimeError:pass
def close_device():
 # Qt sometimes omits early tab labels from AX although the tabs remain visible.
 # Read the tab group's real position, then click its first (Physical) tab.
 try:pos=ax('get position of tab group 1 of window 1').strip()
 except RuntimeError:
  state=json.loads((R/'logs/current-tab-position.json').read_text())
  assert time.time()-state['observed_at']<300,'Stale tab position; inspect GUI before continuing'
  pos=state['position']
 x,y=map(int,pos.split(','));click(x+30,y+12,absolute=True);key(53);time.sleep(1)
 global CONTEXT
 CONTEXT='main'
def command(value):
 guard()
 script='tell application "System Events" to tell (first application process whose unix id is 30530)\nkeystroke '+json.dumps(value)+'\nkey code 36\nend tell'
 subprocess.run(['osascript','-e',script],check=True,capture_output=True,text=True,timeout=10)
def read_console(rel):
 guard()
 script='tell application "System Events" to tell (first application process whose unix id is 30530) to get value of text area 1 of group 1 of window 1'
 v=subprocess.run(['osascript','-e',script],check=True,capture_output=True,text=True,timeout=10)
 (R/rel).write_text(v.stdout);print(v.stdout[-1800:])
def console_value():
 return ax('get value of text area 1 of group 1 of window 1')
def ping(target,rel):
 command('ping '+target);time.sleep(.8)
 deadline=time.monotonic()+45
 while time.monotonic()<deadline:
  value=console_value()
  if value.rstrip().endswith('C:\\>') and ('Ping statistics for '+target+':') in value.rsplit('C:\\>ping '+target,1)[-1]:
   (R/rel).write_text(value)
   print(value.rsplit('C:\\>ping '+target,1)[-1]);return value
  time.sleep(1.5)
 raise RuntimeError('Ping did not complete within bounded wait: '+target)
def snap(rel):
 p=R/rel;p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists():raise RuntimeError('Refusing screenshot overwrite: '+str(p))
 subprocess.run(['screencapture','-x',str(p)],check=True,timeout=10)
 # A resized viewing copy is separate from the original evidence.
 with Image.open(p) as im:
  im.thumbnail((1470,956));im.save(R/'logs/current-preview.png')
 manifest_path=R/'logs/screenshot-manifest.json'
 manifest=json.loads(manifest_path.read_text()) if manifest_path.exists() else []
 manifest.append({'path':str(p.relative_to(R)),'captured_at':datetime.fromtimestamp(p.stat().st_mtime).astimezone().isoformat(),'capture_command':['screencapture','-x',str(p)],'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'kind':'test' if str(p.relative_to(R)).startswith('screenshots/') else 'environment'})
 manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
 print('SCREENSHOT',p)
def run(ops):
 for op in ops:
  with (R/'logs/native-actions.jsonl').open('a') as f:f.write(json.dumps({'time':datetime.now().astimezone().isoformat(),'requested_operation':op})+'\n')
  if op[0]=='click':click(*op[1:])
  elif op[0]=='key':key(*op[1:])
  elif op[0]=='text':text(op[1])
  elif op[0]=='tab':tab(op[1])
  elif op[0]=='close':close_device()
  elif op[0]=='command':command(op[1])
  elif op[0]=='read':read_console(op[1])
  elif op[0]=='paste':paste_button(*op[1:])
  elif op[0]=='wait':time.sleep(min(op[1],10))
  elif op[0]=='snap':snap(op[1])
  else:raise ValueError(op)
if __name__=='__main__':run(json.loads(sys.argv[1]))
def scroll(pixels,x=1200,y=700):
 guard()
 emit(Q.CGEventCreateMouseEvent(None,5,Point(x,y),0))
 Q.CGEventCreateScrollWheelEvent.argtypes=[ctypes.c_void_p,ctypes.c_uint32,ctypes.c_uint32,ctypes.c_int32]
 Q.CGEventCreateScrollWheelEvent.restype=ctypes.c_void_p
 emit(Q.CGEventCreateScrollWheelEvent(None,0,1,int(pixels)));time.sleep(.5)
