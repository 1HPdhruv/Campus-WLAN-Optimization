from pathlib import Path
import sys,time,subprocess,json
sys.path.insert(0,str(Path(__file__).parent))
import gui_native as g,lab_gui as l
subprocess.run(['osascript','-e','tell application "System Events" to set frontmost of (first application process whose unix id is 42895) to true'],check=True)
g.guard();g.snap('screenshots/00_execution_preflight.png');l.new();g.snap('screenshots/01_blank_campus_workspace.png')
# Exact palette identifiers verified in previous execution; actual placements are inspected next.
g.ax('click checkbox "Network Devices" of splitter group 1 of window 1');g.ax('click checkbox "Routers" of splitter group 1 of window 1');l.place_model('2911',650,180)
l.network_switches();l.place_model('3650-24PS',650,260);l.place_model('3560-24PS',650,345)
for x in (350,950):l.place_model('2960',x,450)
l.pcs([(120,570),(300,570),(500,570),(850,570),(1050,570),(1240,570),(940,180)])
g.ax('click checkbox "Network Devices" of splitter group 1 of window 1');g.ax('click checkbox "Wireless Devices" of splitter group 1 of window 1')
l.place_model('AccessPoint-PT',460,460)
l.place_model('AccessPoint-PT',720,460)
g.ax('click checkbox "End Devices" of splitter group 1 of window 1');l.place_model('Laptop-PT',450,670);l.place_model('Laptop-PT',720,670)
g.snap('screenshots/02_campus_device_inventory.png')
