from pathlib import Path
import json,csv,hashlib,re,zipfile,subprocess,datetime
P=Path(__file__).resolve().parents[2];E=P/'submission-evidence';L=P.parent/'PT-Capability-Lab'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
before=json.loads((E/'logs/preservation-before.json').read_text());audit={'date':datetime.datetime.now().astimezone().isoformat(),'scope':'Final functional minimum viable submission audit'}
lab_bad=[n for n,h in before['lab'].items()if not(L/n).is_file()or sha(L/n)!=h]
assert lab_bad == ['task-7/tests/H02_wireless_forwarding_diagnostic.pkt'],lab_bad
audit['historical_lab']={'original_files_checked':len(before['lab']),'all_unchanged':False,'unchanged_count':len(before['lab'])-len(lab_bad),'mismatches':[{'path':n,'original_sha256':before['lab'][n],'current_sha256':sha(L/n),'modified_time':datetime.datetime.fromtimestamp((L/n).stat().st_mtime).astimezone().isoformat()}for n in lab_bad],'exception':'H02 file changed during the initial GUI session. No original byte copy recovered; exact state delta is unverified. Original diagnostic reports/screenshots and H01 wired control remain unchanged. No historical outcome was revised.'}
for name in ['baseline','optimized','comparison']:
 assert sha(P/f'results/historical/{name}.csv')==before['project'][f'results/{name}.csv']
assert sha(P/'presentation/Campus_WLAN_Optimization.pptx')==before['project']['presentation/Campus_WLAN_Optimization.pptx']
audit['preservation']={'legacy_csv_byte_copies':True,'original_presentation_unchanged':True,'commits_created':False,'software_installed':False}
arch=E/'references/original-project-documents'
originals=[]
for p in arch.rglob('*'):
 if p.is_file():
  n=str(p.relative_to(arch));assert sha(p)==before['project'][n],n;originals.append(n)
audit['preservation']['original_narrative_copies']=originals
shots=json.loads((E/'logs/screenshot-manifest.json').read_text())
for r in shots:assert sha(E/r['path'])==r['sha256'],r['path']
for r in json.loads((P/'report/figure-manifest.json').read_text()):
 assert sha(Path(r['source']))==r['sha256'];assert sha(P/'report/figures'/r['figure'])==r['sha256']
audit['screenshots']={'execution_capture_records':len(shots),'all_hashes_valid':True,'curated_figure_copies':13,'genuine_capture_provenance':'Native screencapture command and time in screenshot-manifest.json; figure 10 is explicitly a derived graph; figure 11 is preserved historical evidence.'}
for variant,expected_count in [('baseline',9),('optimized',13)]:
 rows=list(csv.DictReader((P/f'results/{variant}.csv').open()));assert len(rows)==expected_count
 for r in rows:
  t=(P/r['evidence']).read_text();st=re.findall(r'Packets: Sent = (\d+), Received = (\d+), Lost = (\d+)',t)[-1];st=tuple(map(int,st));assert st[0]==int(r['packets_sent'])==4 and st[1]==int(r['echo_replies']);assert r['status']=='PASS';assert st==((4,4,0)if r['expected']=='allow'else(4,0,4))
 audit[variant+'_results']={'probes':len(rows),'all_match_actual_transcripts':True,'all_match_expected':True,'allow_count':sum(r['expected']=='allow'for r in rows),'deny_count':sum(r['expected']=='deny'for r in rows)}
comp=list(csv.DictReader((P/'results/comparison.csv').open()));assert len(comp)==9
for r in comp:
 for v in ['baseline','optimized']:
  t=(P/r[v+'_evidence']).read_text();st=re.findall(r'Packets: Sent = (\d+), Received = (\d+), Lost = (\d+)',t)[-1];assert int(st[1])==int(r[v+'_received'])
audit['comparison']={'flows':9,'each_value_matches_completed_raw_probe':True,'claim_boundary':'Functional echo-reply counts only. Intended ACL denial is not measured network packet loss. No throughput or RF coverage metric.'}
persist=json.loads((E/'logs/persistence_results.json').read_text());assert len(persist['probes'])==5
for k,r in persist['probes'].items():assert tuple(r['stats'])==((4,4,0)if r['expected']=='allow'else(4,0,4))
audit['native_topologies']={}
for variant in ['baseline','optimized']:
 p=P/f'packet-tracer/{variant}/campus_{variant}.pkt';assert p.stat().st_size>60000
 audit['native_topologies'][variant]={'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p),'native_open_verified':True,'evidence':persist[variant+'_opened']}
audit['native_topologies']['optimized_reopened_probe_count']=5
for client,ip,gw in [('PC1','10.10.10.21','10.10.10.1'),('PC3','10.10.20.21','10.10.20.1')]:
 t=(E/f'logs/optimized_reopened_{client}_lease.txt').read_text();assert ip in t and gw in t and '255.255.255.0'in t and '10.255.0.1'in t
audit['dhcp']={'configured_pools':6,'tested_role_pools':['Students','Faculty'],'actual_reopened_addresses':['10.10.10.21','10.10.20.21'],'server':'10.255.0.1'}
receipt=json.loads((E/'build/presentation-validation.json').read_text());ppt=P/'presentation/Campus_WLAN_Optimization_Final.pptx';assert receipt['finalSha256']==sha(ppt);assert receipt['packageIntegrity']['slide_count']==12 and receipt['firstPartyImport']['passed'] and receipt['presentationLayout']['finding_count']==0
pdf=E/'build/Campus_WLAN_Optimization_Final.pdf';info=subprocess.check_output(['pdfinfo',str(pdf)],text=True);assert re.search(r'Pages:\s+12',info)
audit['presentation']={'path':str(ppt),'sha256':sha(ppt),'slides':12,'structural_validation':'PASS','artifact_tool_reimport':'PASS','libreoffice_open_and_pdf_export':'PASS','pdf_pages':12,'powerpoint_native_open':'NOT VERIFIED; application unavailable','visual_review':'All 12 authoring renders individually inspected; external-render spot checks on slides 5 and 11','layout_warnings':receipt['presentationLayout'].get('warnings',[]),'validation_receipt':'submission-evidence/build/presentation-validation.json'}
paths=[P/'README.md',P/'report/report-content.md']+[P/f'documentation/{n}.md'for n in ['architecture','ip-addressing','results','testing','vlan-plan','wireless-plan']]
badlinks=[]
for p in paths:
 for link in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',p.read_text()):
  if re.match(r'https?://',link)or link.startswith('#'):continue
  target=(p.parent/link.split('#')[0]).resolve()
  if not target.exists():badlinks.append({'file':str(p.relative_to(P)),'link':link})
assert not badlinks,badlinks
audit['report']={'chapters':6,'figure_manifest_entries':13,'local_links_checked':True,'final_institutional_formatting':'Pending supplied template','team_identities':'Pending user input'}
audit['project_files_changed_from_start']=[n for n,h in before['project'].items()if not(P/n).is_file()or sha(P/n)!=h]
audit['status']='Functional deliverables PASS; historical byte-preservation exception disclosed'
(E/'logs/final-audit.json').write_text(json.dumps(audit,indent=2)+'\n');print(json.dumps({k:audit[k]for k in ['status','historical_lab','baseline_results','optimized_results','comparison']},indent=2))
