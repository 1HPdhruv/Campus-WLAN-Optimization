"""Reusable native GUI steps for independent disposable Packet Tracer labs."""
from pathlib import Path
import time,json
import gui_native as g
R=Path(__file__).resolve().parents[1]
def menu(item):return g.ax('click menu item '+json.dumps(item)+' of menu 1 of menu bar item "File" of menu bar 1')
def new():
 menu('New');time.sleep(.7)
 contents=g.ax('get entire contents of window 1')
 if 'Any unsaved changes will be lost' in contents:
  g.ax('click button "Yes" of group 1 of window 1');time.sleep(1)
 title=g.ax('get name of window 1').strip()
 assert title.startswith('Cisco Packet Tracer') and '.pkt' not in title, 'New workspace not established: '+title
def save_as(filename):
 assert not (R/'tests'/filename).exists(), 'Preserve existing working file before replacement'
 menu('Save As ...');time.sleep(1)
 g.key(0,1048576);g.text(filename)
 actual=g.ax('get value of text field "Save As:" of splitter group 1 of window 1').strip()
 assert actual in {filename,Path(filename).stem},(actual,filename)
 # Native Save As resets to the application's saves folder: explicitly choose tests.
 g.ax('click pop up button "Where:" of splitter group 1 of window 1')
 g.ax('click menu item "tests" of menu 1 of pop up button "Where:" of splitter group 1 of window 1');time.sleep(.4)
 g.ax('click button "Save" of splitter group 1 of window 1');time.sleep(1)
 p=R/'tests'/filename
 assert p.is_file() and p.stat().st_size>0, 'Save not found in designated folder'
 return p

def network_switches():
 g.ax('click checkbox "Network Devices" of splitter group 1 of window 1');g.ax('click checkbox "Switches" of splitter group 1 of window 1')
def place(palette_x,x,y):g.click(palette_x,816);g.click(x,y);g.key(53)
def place_model(model,x,y):
 g.ax('click checkbox '+json.dumps(model)+' of splitter group 1 of window 1');g.click(x,y);g.key(53)
def pcs(positions):
 g.ax('click checkbox "End Devices" of splitter group 1 of window 1')
 for x,y in positions:place_model('PC-PT',x,y)
def cable_pc(pc,sw):
 # Caller verifies the first available switch FastEthernet port is the intended one.
 px,py=pc;sx,sy=sw
 g.ax('click checkbox "Connections" of splitter group 1 of window 1');g.ax('click checkbox "Copper Straight-Through" of splitter group 1 of window 1');g.click(px,py);g.click(px+74,py+69);g.click(sx,sy);g.click(sx+75,sy+28);g.key(53)
def open_device(x,y,name=None):
 g.CONTEXT='main';g.click(x,y);time.sleep(.8);g.CONTEXT='device'
 if name:assert g.ax('get name of window 1').strip()==name

def pc_ip(x,y,name,ip,gateway=None,evidence=None):
 open_device(x,y,name);g.tab('Desktop');g.click(165,156);time.sleep(.3)
 g.click(750,237);g.key(0,1048576);g.text(ip);g.key(48)
 g.click(750,269);g.key(0,1048576);g.text('255.255.255.0');g.key(48)
 if gateway:
  g.click(750,300);g.key(0,1048576);g.text(gateway);g.key(48)
 if evidence:g.snap(evidence)
 g.close_device()
def pc_terminal(x,y,name=None):open_device(x,y,name);g.tab('Desktop');g.click(1008,156)
def ios(x,y,config=None):
 import re
 open_device(x,y);g.tab('CLI')
 assert g.ax('exists static text "IOS Command Line Interface" of group 1 of window 1').strip()=='true','CLI unavailable; check simulated device power/module'
 deadline=time.monotonic()+50
 while time.monotonic()<deadline:
  value=g.console_value()
  if 'initial configuration dialog' in value.lower() and not re.search(r'(?m)^[A-Za-z][A-Za-z0-9_.()/-]*[>#](?:\s|$)',value):
   g.click(700,700);g.command('no');time.sleep(.3);break
  if 'Press RETURN' in value or re.search(r'(?m)^[A-Za-z][A-Za-z0-9_.()/-]*[>#](?:\s|$)',value):break
  time.sleep(1.5)
 else:raise RuntimeError('Device CLI boot readiness not observed')
 g.click(600,500);g.key(36)
 if config:g.paste_button(config)
def startup_save():g.paste_button('copy running-config startup-config\n');g.command('')

def reopen(filename):
 import subprocess
 new()
 subprocess.run(['open','-a','/Applications/Cisco Packet Tracer 9.0.1/Cisco Packet Tracer 9.0.1.app',str(R/'tests'/filename)],check=True)
 time.sleep(2)
 title=g.ax('get name of window 1').strip()
 assert title.endswith('/tests/'+filename),title
 return title
def ping_stats(value):
 import re
 found=re.findall(r'Packets: Sent = (\d+), Received = (\d+), Lost = (\d+)',value)
 assert found,'Missing completed ping statistics'
 return tuple(map(int,found[-1]))
def positive(target,stem):
 value=g.ping(target,stem+'_first.txt')
 if ping_stats(value)!=(4,4,0):
  time.sleep(3)
  value=g.ping(target,stem+'_repeat.txt')
 assert ping_stats(value)==(4,4,0), 'Persistent positive-control failure: '+target
 return value

def negative(target,stem):
 value=g.ping(target,stem+'.txt')
 assert ping_stats(value)==(4,0,4), 'Negative test did not produce expected isolation: '+target
 return value
def connect(a,port_a,b,port_b,cable='Copper Straight-Through'):
 g.ax('click checkbox "Connections" of splitter group 1 of window 1')
 g.ax('click checkbox '+json.dumps(cable)+' of splitter group 1 of window 1')
 g.click(*a);g.ax('click menu item '+json.dumps(port_a)+' of window 1')
 g.click(*b);g.ax('click menu item '+json.dumps(port_b)+' of window 1');g.key(53)
def pc_info(rel):
 g.command('ipconfig /all');time.sleep(.4)
 for _ in range(5):
  v=g.console_value()
  if v.rstrip().endswith('C:\\>'):
   (R/rel).write_text(v);print(v[-2000:]);return v
  if '--More--' in v[-100:]:g.click(700,700);g.key(49)
  else:time.sleep(.3)
 raise RuntimeError('PC ipconfig output still paginated/incomplete')
def dhcp_pc(x,y,name,prefix,stem):
 import re
 open_device(x,y,name);g.tab('Desktop');g.click(165,156)
 valid=False
 for attempt in range(2):
  # Real mouse click is required: AX radio selection changed state without requesting DHCP.
  g.click(513,203);g.click(44,203)
  for _ in range(8):
   time.sleep(2)
   fields=g.ax('get value of every text field of group "IP Configuration" of group 1 of window 1')
   ips=re.findall(r'\d+\.\d+\.\d+\.\d+',fields)
   clients=[a for a in ips if a.startswith(prefix) and 20<int(a.rsplit('.',1)[1])<255]
   if clients and '255.255.255.0' in ips and prefix+'1' in ips:valid=True;break
  if valid:break
 assert valid,'No observed valid DHCP lease: '+fields
 print(name,'observed DHCP',fields.strip());g.snap(stem+'_ip.png');g.close_device()
 pc_terminal(x,y,name);pc_info(str(Path(stem).with_suffix(''))+'_lease.txt' if stem.startswith('logs/') else 'logs/'+Path(stem).name+'_lease.txt')
 positive(prefix+'1','logs/'+Path(stem).name+'_gateway');g.snap(stem+'_gateway.png');g.close_device()
def ssh_trial(allowed,rel,screenshot):
 command='ssh -l labadmin 10.10.99.1'
 g.command(command);time.sleep(.35);sent_password=False;authenticated=False
 deadline=time.monotonic()+30
 while time.monotonic()<deadline:
  v=g.console_value();latest=v.rsplit('C:\\>'+command,1)[-1]
  if latest.rstrip().endswith('Password:') and not sent_password:
   g.command('LabOnly99Test');sent_password=True
  elif v.rstrip().endswith('E-MLS>') or v.rstrip().endswith('E-MLS#'):
   authenticated=True;break
  elif latest.rstrip().endswith('C:\\>') and ('closed' in latest.lower() or 'timed out' in latest.lower() or 'refused' in latest.lower()):break
  time.sleep(.3)
 (R/rel).write_text(v);print(v[-1300:]);g.snap(screenshot)
 assert authenticated==allowed,'SSH source policy mismatch or unresolved session'
 if not allowed:assert 'closed' in latest.lower() or 'timed out' in latest.lower() or 'refused' in latest.lower(),'No completed denial observed'
 if authenticated:g.command('exit');time.sleep(.3)
 return authenticated
def ap_config(x,y,evidence):
 open_device(x,y);g.tab('Config');g.click(70,208)
 g.click(1100,190);g.key(0,1048576);g.text('STUDENT_WIFI');g.key(48)
 g.click(539,307);g.click(1350,307);g.key(0,1048576);g.text('CampusLab2026');g.key(48)
 g.click(1100,215);g.key(115);g.key(36);g.click(1000,500)
 assert g.ax('get value of text field "SSID" of group 1 of window 1').strip()=='STUDENT_WIFI'
 assert g.ax('get value of radio button "WPA2-PSK" of group 1 of window 1').strip()=='1'
 assert g.ax('get name of every menu button of group 1 of window 1').strip()=='1, AES'
 g.snap(evidence);g.close_device()
def field(name,value,container='group 1 of window 1'):
 ref='text field '+json.dumps(name)+' of '+container
 x,y=map(int,g.ax('get position of '+ref).strip().split(','));g.click(x+25,y+8);g.key(0,1048576);g.text(value);g.key(48)
def auto_cable(a,b):
 g.ax('click checkbox "Connections" of splitter group 1 of window 1');g.ax('click checkbox "Automatically Choose Connection Type" of splitter group 1 of window 1');g.click(*a);g.click(*b);g.key(53)
def wireless_laptop(x,y,ip,evidence):
 open_device(x,y);g.tab('Physical');g.click(256,434);g.drag(412,440,100,550);g.click(100,132);g.drag(1395,833,412,440);g.click(256,434);g.tab('Config');g.click(87,209)
 for px,py,val in [(1120,231,'STUDENT_WIFI'),(1350,305,'CampusLab2026')]:
  if py==305:g.click(560,305)
  g.click(px,py);g.key(0,1048576);g.text(val);g.key(48)
 g.click(197,516)
 for py,val in [(531,ip),(553,'255.255.255.0')]:g.click(1120,py);g.key(0,1048576);g.text(val);g.key(48)
 g.snap(evidence);g.close_device()
def wlc_browser():
 open_device(400,600,'PC0');g.tab('Desktop');g.click(1290,156);field('URL','https://10.10.99.2');g.click(1366,147);time.sleep(3);g.click(724,680);time.sleep(.5);g.click(750,291);g.text('labadmin');g.key(48);g.text('CampusLab2026!');g.click(696,365);time.sleep(3)
def native_control(ref):
 x,y=map(int,g.ax('get position of '+ref).strip().split(','));w,h=map(int,g.ax('get size of '+ref).strip().split(','));g.click(x+w/2,y+h/2,absolute=True)
