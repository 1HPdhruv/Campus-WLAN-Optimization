"""Build submission data from completed native Packet Tracer transcripts only."""
from pathlib import Path
import json,re,csv
R=Path(__file__).resolve().parents[1];P=R.parent
labels={'within_vlan':'Wired within VLAN','student_admin':'Student to Administration','faculty_admin':'Faculty to Administration','guest_admin':'Guest to Administration','guest_external':'Guest to external host','iot_admin':'IoT proxy to Administration','wireless_student':'Wireless Student to wired Student','student_management':'Student to management switch','iot_external':'IoT proxy to external host','student_faculty':'Student to Faculty','management_access':'Management to access switch','management_core':'Management to core','external_management':'External host to management switch'}
def transcript(variant,flow):
 for suffix in ['repeat','first']:
  p=R/'logs'/f'{variant}_{flow}_{suffix}.txt'
  if p.exists():
   a=re.findall(r'Packets: Sent = (\d+), Received = (\d+), Lost = (\d+)',p.read_text())
   if a:return p,tuple(map(int,a[-1]))
 raise RuntimeError('No completed trial: '+variant+' '+flow)
b=json.loads((R/'logs/baseline_results.json').read_text());b.update(json.loads((R/'logs/baseline_extra_results.json').read_text()));b.pop('reopened_wireless',None)
o=json.loads((R/'logs/optimized_results.json').read_text())
assert len(o)==13,'Essential probe sequence has not completed'
for variant,flows in [('baseline',b),('optimized',o)]:
 rows=[]
 for flow in flows:
  p,st=transcript(variant,flow)
  expected='allow' if variant=='baseline' else flows[flow]['expected']
  status='PASS' if st==(4,4,0) and expected=='allow' or st==(4,0,4) and expected=='deny' else 'FAIL'
  rows.append({'test_id':flow,'flow':labels[flow],'expected':expected,'packets_sent':st[0],'echo_replies':st[1],'status':status,'evidence':str(p.relative_to(P))})
 with (P/'results'/f'{variant}.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
 (R/'logs'/f'{variant}_verified_rows.json').write_text(json.dumps(rows,indent=2))
 assert all(r['status']=='PASS' for r in rows),rows
comp=[]
for flow in b:
 if flow not in o:continue
 bp,bs=transcript('baseline',flow);op,os=transcript('optimized',flow)
 comp.append({'flow':flow,'label':labels[flow],'short_label':{'student_admin':'Student/Admin','faculty_admin':'Faculty/Admin','guest_admin':'Guest/Admin','guest_external':'Guest/External'}.get(flow,labels[flow]),'baseline_received':bs[1],'optimized_received':os[1],'packets_sent':4,'optimized_expected':o[flow]['expected'],'baseline_evidence':str(bp.relative_to(P)),'optimized_evidence':str(op.relative_to(P))})
with (P/'results/comparison.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=comp[0].keys());w.writeheader();w.writerows(comp)
(R/'logs/comparison.json').write_text(json.dumps(comp,indent=2))
# Descriptive scientific plot. Intended ACL denials are not network packet-loss measurements.
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
chosen=[next(r for r in comp if r['flow']==k) for k in ['student_admin','faculty_admin','guest_admin','guest_external']]
fig,ax=plt.subplots(figsize=(9.2,4.8),layout='constrained');x=list(range(len(chosen)))
ax.bar([i-.18 for i in x],[r['baseline_received'] for r in chosen],.36,label='Baseline',color='#142e49')
ax.bar([i+.18 for i in x],[r['optimized_received'] for r in chosen],.36,label='Optimized',color='#087f8c')
ax.set_xticks(x,[r['label'].replace(' to ','\nto ') for r in chosen]);ax.set_yticks(range(5));ax.set_ylim(0,4.7);ax.set_ylabel('ICMP echo replies received out of 4');ax.set_title('Observed functional connectivity and access policy');ax.legend();ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
fig.savefig(P/'results/functional-comparison.png',dpi=180);fig.savefig(P/'results/functional-comparison.svg');plt.close(fig)
(P/'results/historical/README.md').write_text('''# Unverified historical data\n\nThese three CSVs are byte-for-byte copies of the original repository values. No supporting measurements were found. They are historical placeholders and are excluded from the submitted measured results. In particular, 50→180 Mbps and 78%→95% coverage are not project measurements.\n\nThe parent results directory now contains only newly verified functional test records and a descriptive graph of completed ICMP probes. ACL denials are intended policy outcomes, not network packet-loss rates.\n''')
print('Derived verified results:',len(b),'baseline probes,',len(o),'optimized probes,',len(comp),'comparable flows')
