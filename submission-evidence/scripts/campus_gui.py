from pathlib import Path
import sys,time,re,json,subprocess
import gui_native as g,lab_gui as l
R=Path(__file__).resolve().parents[1]
def close():
 g.click(650 if g.ax('get name of window 1').strip().startswith(('Switch','Router')) else 592,77);g.key(53);time.sleep(.7)
def ios_at(x,y,name=None):
 l.open_device(x,y,name);g.tab('CLI');g.click(600,700);g.key(36);time.sleep(.5)
 for _ in range(25):
  try:v=g.console_value()
  except Exception:time.sleep(.6);continue
  if '[yes/no]:' in v[-600:] and not re.search(r'(?:^|\n)[A-Za-z][A-Za-z0-9_.-]*[>#]\s*$',v.rstrip()):g.command('no');time.sleep(1);g.key(36);continue
  if re.search(r'(?:^|\n)[A-Za-z][A-Za-z0-9_.-]*[>#]\s*$',v.rstrip()):
   g.command('enable');time.sleep(.2);return g.console_value()
  time.sleep(.7);g.key(36)
 raise RuntimeError('No actual CLI prompt')
def show(cmd,stem):
 g.command(cmd);time.sleep(.5)
 for _ in range(10):
  v=g.console_value()
  if '--More--' in v[-110:]:g.key(49);time.sleep(.2)
  else:break
 v=g.console_value();(R/'logs'/f'{stem}.txt').write_text(v);print(v[-1600:],flush=True);return v

def apply(x,y,config,stem):
 ios_at(x,y);g.paste_button((R/'configurations'/config).read_text());time.sleep(.7)
 v=g.console_value();(R/'logs'/f'{stem}_applied.txt').write_text(v)
 if '% Invalid' in v or '% Incomplete' in v:print('INSPECT CLI ERRORS',stem,flush=True)
 show('show ip interface brief',stem+'_interfaces');g.snap('screenshots/'+stem+'_interfaces.png');l.startup_save();g.close_device()
def save_to(target):
 p=Path(target);assert not p.exists() or p.stat().st_size==0,'Preserve nonempty existing file'
 l.menu('Save As ...');time.sleep(.8)
 g.ax('set value of text field "Save As:" of splitter group 1 of window 1 to '+json.dumps(p.name));g.click(750,267,absolute=True);g.ax('key code 5 using {command down, shift down}');time.sleep(.7)
 g.ax('set value of text field 1 of sheet 1 of window 1 to '+json.dumps(str(p.parent)));g.ax('key code 36');time.sleep(.7);g.ax('click button "Save" of splitter group 1 of window 1');time.sleep(.8)
 content=g.ax('get entire contents of window 1')
 if 'Overwrite' in content:
  g.ax('click button "Yes" of group 1 of window 1');time.sleep(.8)
 if 'Replace' in content:
  # Native replace is authorized only for the original zero-byte placeholder.
  g.ax('click button "Replace" of sheet 1 of window 1');time.sleep(.8)
 assert p.exists() and p.stat().st_size>0,p
 assert str(p) in g.ax('get name of window 1')
 print('SAVED',p,p.stat().st_size,flush=True)
def reopen(p):
 l.new();subprocess.run(['open','-a','/Applications/Cisco Packet Tracer 9.0.1/Cisco Packet Tracer 9.0.1.app',str(p)],check=True);time.sleep(3)
 assert str(p) in g.ax('get name of window 1')
def pc_dhcp(x,y,name,stem):
 l.open_device(x,y,name);g.click(713,77);g.click(165,156);g.click(513,203);g.click(44,203);time.sleep(3)
 g.snap('screenshots/'+stem+'_lease.png');g.close_device()
def ping_at(x,y,name,target,stem,expected=None):
 l.pc_terminal(x,y,name);v=g.ping(target,'logs/'+stem+'_first.txt')
 if expected=='allow' and l.ping_stats(v)!=(4,4,0):time.sleep(2);v=g.ping(target,'logs/'+stem+'_repeat.txt')
 g.snap('screenshots/'+stem+'.png');g.close_device();return l.ping_stats(v)
def ap(x,y,ssid,channel,stem):
 l.open_device(x,y);g.tab('Config');g.click(70,208)
 g.click(1100,190);g.key(0,1048576);g.text(ssid);g.key(48)
 g.click(539,307);g.click(1350,307);g.key(0,1048576);g.text('CampusLab2026');g.key(48)
 g.click(1100,215);g.key(115)
 for _ in range(channel-1):g.key(125)
 g.key(36);g.click(1000,500);g.snap('screenshots/'+stem+'.png');g.close_device()
def desktop_grid(x,y,name):
 l.open_device(x,y,name);g.click(713,77);g.click(1433,114);time.sleep(.2)
def terminal(x,y,name):
 desktop_grid(x,y,name);g.click(1008,156);g.click(600,700)
def pc_ip(x,y,name,ip,gateway,stem):
 desktop_grid(x,y,name);g.click(165,156)
 for py,value in [(237,ip),(269,'255.255.255.0'),(300,gateway)]:g.click(750,py);g.key(0,1048576);g.text(value);g.key(48)
 g.snap('screenshots/'+stem+'_IP.png');g.close_device()
def pc_dhcp(x,y,name,stem):
 desktop_grid(x,y,name);g.click(165,156);g.click(513,203);g.click(44,203);time.sleep(3);g.snap('screenshots/'+stem+'_lease.png');g.close_device()
def ping_at(x,y,name,target,stem,expected=None):
 terminal(x,y,name);v=g.ping(target,'logs/'+stem+'_first.txt')
 if expected=='allow' and l.ping_stats(v)!=(4,4,0):time.sleep(2);v=g.ping(target,'logs/'+stem+'_repeat.txt')
 g.snap('screenshots/'+stem+'.png');g.close_device();return l.ping_stats(v)
