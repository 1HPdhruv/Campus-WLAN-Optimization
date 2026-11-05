from pathlib import Path
r=Path(__file__).resolve().parents[1]/'configurations'
roles={10:'STUDENTS',20:'FACULTY',30:'ADMINISTRATION',40:'GUESTS',50:'IOT',99:'MANAGEMENT'}
def save(name,lines):
 (r/name).write_text('\n'.join(lines)+ '\n')
def header(host):return ['enable','configure terminal','hostname '+host,'no ip domain-lookup']
def routed(port,ip):return ['interface '+port,'no switchport','ip address '+ip+' 255.255.255.252','no shutdown','exit']
def trunk(port,vlans,native,encap=False):return ['interface '+port]+(['switchport trunk encapsulation dot1q'] if encap else [])+['switchport mode trunk','switchport trunk native vlan '+str(native),'switchport trunk allowed vlan '+vlans,'no shutdown','exit']
def access(port,v):return ['interface '+port,'switchport mode access','switchport access vlan '+str(v),'spanning-tree portfast','no shutdown','exit']
def vlans():
 a=[]
 for v,n in roles.items():a+=['vlan '+str(v),'name '+n,'exit']
 return a
for variant in ['baseline','optimized']:
 opt=variant=='optimized';prefix=variant.upper()
 edge=header('CAMPUS-EDGE')+['interface gigabitEthernet0/0','ip address 10.255.0.1 255.255.255.252','no shutdown','exit','interface gigabitEthernet0/1','ip address 203.0.113.1 255.255.255.0','no shutdown','exit','ip route 10.10.0.0 255.255.0.0 10.255.0.2']
 if opt:edge+=['no ip dhcp pool BASELINE','no ip dhcp excluded-address 10.10.1.1 10.10.1.20']
 for v,n in (roles.items() if opt else [(1,'BASELINE')]):
  edge+=['ip dhcp excluded-address 10.10.%s.1 10.10.%s.20'%(v,v),'ip dhcp pool '+n,'network 10.10.%s.0 255.255.255.0'%v,'default-router 10.10.%s.1'%v,'exit']
 edge+=['end'];save(variant+'_edge.txt',edge)
 core=header('CAMPUS-CORE')+['ip routing']+routed('gigabitEthernet1/0/1','10.255.0.2')+routed('gigabitEthernet1/0/2','10.255.0.5')+['ip route 10.10.0.0 255.255.0.0 10.255.0.6','ip route 0.0.0.0 0.0.0.0 10.255.0.1','end'];save(variant+'_core.txt',core)
 d=header('CAMPUS-DISTRIBUTION')+['ip routing']+routed('fastEthernet0/1','10.255.0.6')
 if opt:d+=vlans()+['interface vlan 1','no ip address','shutdown','exit']
 for p in ['fastEthernet0/2','fastEthernet0/3']:d+=trunk(p,'10,20,30,40,50,99' if opt else '1',99 if opt else 1,True)
 for v in (roles if opt else [1]):d+=['interface vlan '+str(v),'ip address 10.10.%s.1 255.255.255.0'%v,'ip helper-address 10.255.0.1','no shutdown','exit']
 d+=['ip route 0.0.0.0 0.0.0.0 10.255.0.5']
 if opt:
  for v,name in [(10,'STUDENTS_IN'),(20,'FACULTY_IN'),(30,'ADMIN_IN'),(40,'GUESTS_IN'),(50,'IOT_IN')]:
   d+=['ip access-list extended '+name,'permit udp any eq bootpc any eq bootps']
   if v in [10,20,30]:
    if v==10:d+=['deny ip any 10.10.30.0 0.0.0.255']
    d+=['deny ip any 10.10.99.0 0.0.0.255','deny ip any 10.255.0.0 0.0.255.255','permit ip any any']
   elif v==40:d+=['deny ip any 10.0.0.0 0.255.255.255','deny ip any 172.16.0.0 0.15.255.255','deny ip any 192.168.0.0 0.0.255.255','permit ip any any']
   else:d+=['permit ip any host 203.0.113.10','deny ip any any']
   d+=['exit','interface vlan '+str(v),'ip access-group '+name+' in','exit']
 d+=['end'];save(variant+'_distribution.txt',d)
 for floor,num,ports in [('ground',11,{2:10,3:10,4:50,5:10,6:40}),('first',12,{2:20,3:30,4:99})]:
  a=header('ACCESS-'+floor.upper())+(vlans() if opt else [])+trunk('fastEthernet0/1','10,20,30,40,50,99' if opt else '1',99 if opt else 1)
  for p,v in ports.items():a+=access('fastEthernet0/'+str(p),v if opt else 1)
  if opt:a+=['interface vlan 1','no ip address','shutdown','exit','interface vlan 99','ip address 10.10.99.%s 255.255.255.0'%num,'no shutdown','exit','ip default-gateway 10.10.99.1']
  else:a+=['interface vlan 1','ip address 10.10.1.%s 255.255.255.0'%num,'no shutdown','exit','ip default-gateway 10.10.1.1']
  a+=['end'];save(variant+'_access_'+floor+'.txt',a)
print('Prepared model-compatible configurations for actual GUI application; no test result inferred.')
