from pathlib import Path
import json,csv,shutil,hashlib
P=Path(__file__).resolve().parents[2];E=P/'submission-evidence';R=P/'report';R.mkdir(exist_ok=True);(R/'figures').mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s)
# Preserve original narrative before reconciling the authoritative implementation notes.
for name in ['README.md','documentation/architecture.md','documentation/vlan-plan.md','documentation/ip-addressing.md','documentation/wireless-plan.md','documentation/testing.md','documentation/results.md']:
 dst=E/'references/original-project-documents'/name
 if not dst.exists():dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(P/name,dst)
figs=[
('01-baseline.png',E/'screenshots/baseline_final_topology.png','Functioning baseline: shared client VLAN 1, clustered APs, same three network tiers.'),
('02-optimized.png',E/'screenshots/optimized_submission_ready.png','Saved optimized campus reopened in Packet Tracer; logical labels represent five functional zones.'),
('03-trunks.png',E/'screenshots/optimized_distribution_trunks.png','Distribution uplinks trunk all six VLANs, native VLAN 99; all six are forwarding.'),
('04-student-dhcp.png',E/'screenshots/optimized_reopened_PC1_lease.png','Student PC1 obtains 10.10.10.21/24 and gateway 10.10.10.1 after reopening.'),
('05-dhcp-bindings.png',E/'screenshots/optimized_reopened_DHCP_bindings.png','Edge router DHCP bindings corroborate the Student and Faculty leases.'),
('06-acl-counters.png',E/'screenshots/optimized_ACL_counters.png','Distribution ACL readback and counters support observed policy outcomes.'),
('07-guest-denial.png',E/'screenshots/optimized_reopened_guest_admin.png','Guest wireless client receives zero echo replies from Administration; rejection is intended.'),
('08-faculty-allowed.png',E/'screenshots/optimized_reopened_faculty_admin.png','Faculty reaches Administration with four of four replies after initial ARP handling.'),
('09-wireless-forwarding.png',E/'screenshots/optimized_reopened_wireless_student.png','Standalone Student WLAN forwards to the wired Student endpoint after reopening.'),
('10-functional-comparison.png',P/'results/functional-comparison.png','Observed four-packet probe reply counts. Zero on denied flows represents policy enforcement.'),
('11-historical-wlc.png',P.parent/'PT-Capability-Lab/task-7/screenshots/77_H02_WLC_to_switch_packet_OSI.png','Preserved historical WLC diagnostic: VLAN 10 forwarding failure remains unresolved.'),
('12-ap-channel.png',E/'screenshots/optimized_guests_AP.png','Guest standalone AP configuration: channel 6, WPA2-PSK/AES.'),
('13-fresh-mac.png',E/'screenshots/optimized_reopened_fresh_wireless_MAC.png','Fresh MAC learning after reopening: Student WLAN on Fa0/5 VLAN 10; Guest WLAN on Fa0/6 VLAN 40.')]
manifest=[]
for n,src,caption in figs:
 dst=R/'figures'/n;shutil.copy2(src,dst);assert sha(src)==sha(dst)
 manifest.append({'figure':n,'caption':caption,'source':str(src),'sha256':sha(src)})
write(R/'figure-manifest.json',json.dumps(manifest,indent=2)+'\n')
opt=json.loads((E/'logs/optimized_verified_rows.json').read_text());comp=json.loads((E/'logs/comparison.json').read_text())
def mdtable(headers,rows):return '| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+''.join('| '+' | '.join(map(str,r))+' |\n' for r in rows)
vlans=[('10','Students','10.10.10.0/24','10.10.10.1'),('20','Faculty','10.10.20.0/24','10.10.20.1'),('30','Administration','10.10.30.0/24','10.10.30.1'),('40','Guests','10.10.40.0/24','10.10.40.1'),('50','IoT','10.10.50.0/24','10.10.50.1'),('99','Network Management','10.10.99.0/24','10.10.99.1')]
vtab=mdtable(['VLAN','Role','Simulation subnet','Distribution gateway'],vlans)
endpoints=[('PC0','Students, Classrooms','10.10.1.101','10.10.10.10','Static'),('PC1','Students, Computer laboratory','10.10.1.21','10.10.10.21','DHCP, observed'),('PC2','IoT policy proxy, Computer laboratory','10.10.1.150','10.10.50.10','Static; PC-PT'),('PC3','Faculty, Library','10.10.1.22','10.10.20.21','DHCP, observed'),('PC4','Administration, Faculty/admin','10.10.1.130','10.10.30.10','Static'),('PC5','Management, Faculty/admin','10.10.1.199','10.10.99.10','Static'),('Laptop0','Students, Common area','10.10.1.110','10.10.10.20','Static; wireless'),('Laptop1','Guests, Library','10.10.1.140','10.10.40.20','Static; wireless'),('PC6','External test host','203.0.113.10','203.0.113.10','Static; simulated external network')]
etab=mdtable(['Endpoint','Role / logical zone','Baseline IP','Optimized IP','Addressing'],endpoints)
ports=[('2911 Gi0/0','3650 Gi1/0/1','10.255.0.1 / .2, /30'),('3650 Gi1/0/2','3560 Fa0/1','10.255.0.5 / .6, /30'),('3560 Fa0/2','Ground 2960 Fa0/1','802.1Q: 10,20,30,40,50,99; native 99'),('3560 Fa0/3','First 2960 Fa0/1','802.1Q: 10,20,30,40,50,99; native 99'),('2911 Gi0/1','PC6 FastEthernet0','203.0.113.1 / .10, /24'),('Ground Fa0/2','PC0','Access VLAN 10'),('Ground Fa0/3','PC1','Access VLAN 10'),('Ground Fa0/4','PC2','Access VLAN 50'),('Ground Fa0/5','AP0 Port0','Access VLAN 10'),('Ground Fa0/6','AP1 Port0','Access VLAN 40'),('First Fa0/2','PC3','Access VLAN 20'),('First Fa0/3','PC4','Access VLAN 30'),('First Fa0/4','PC5','Access VLAN 99')]
ptab=mdtable(['Local interface','Remote device / interface','Optimized use'],ports)
limits='''The campus is hypothetical. No SRM floor dimensions, population counts, physical AP locations or surveyed coverage are asserted. The 16 devices, two APs and eight campus endpoints are simulation assumptions, not capacity recommendations. Canvas positions and floor labels are illustrative and do not establish floor attenuation, interference, signal strength or client density.

PC2 is a PC-PT proxy for IoT network policy; appliance registration and telemetry are untested. Six DHCP pools are configured, but actual lease allocation was verified only for Students and Faculty. Other representatives use static addresses. The external PC at 203.0.113.10 is a routed simulation endpoint, not live Internet access. DNS, NAT, HTTP application services, enterprise authentication, SSH administration, redundancy, roaming, WPA3 and QoS were not implemented or verified. Management tests establish IP reachability, not an authenticated management service.

The WLC-based historical fixture still fails wireless VLAN 10 forwarding and has an unresolved root cause. Current WLAN success concerns the two standalone AP-PT devices only. There is one SSID per AP and an untagged access uplink; multi-SSID-to-VLAN tagging is not demonstrated. No throughput, RF coverage percentage, latency improvement or congestion reduction has been established. Four-packet functional probes do not support statistical performance claims.'''
report='''# Campus WLAN Optimization Using Access Point Placement and Network Segmentation

**Report content and evidence package — 5 November 2026**  
**Institution:** SRM Institute of Science and Technology.  
**Team:** five members; names and register numbers await the team.  
**Environment:** Cisco Packet Tracer 9.0.1.0858 on macOS.  
**Status:** functioning baseline and optimized simulation files with recorded functional evidence. Final institutional formatting awaits the user-supplied report template.

This document supplies the six requested chapters. Figures are actual evidence captures or an explicitly identified results graph. Original capability-test findings remain separate and unchanged. The title expresses the project aim; measured findings establish segmentation and connectivity behavior, not RF optimization performance.

## Chapter 1 — Introduction

### 1.1 Context and problem statement

Campus networks serve different trust groups and should distinguish shared access from restricted departmental and management resources. A flat client network allows communication that may violate those intended boundaries. Wireless planning also needs deliberate placement and channel choices, but a logical simulator does not replace a physical RF survey.

The project models a compact two-floor hypothetical university campus. The ground floor contains Classrooms, Computer laboratory and Common area; the first floor contains Library and Faculty/administration. Students, Faculty, Administration, Guests, IoT and Network Management are distinct roles. A full core–distribution–access hierarchy with a separate edge router is an approved academic requirement. It is retained in both networks to make the baseline comparison clear; no assertion is made that a real campus of this assumed size requires three tiers.

### 1.2 Aim and objectives

The aim is to produce a working simulation comparison that combines role segmentation with a more deliberate AP/channel arrangement. Objectives are to implement the approved six VLANs, verify trunking and routed connectivity, allocate addresses through DHCP, enforce ACL restrictions, demonstrate basic standalone wireless forwarding, and document exactly what the simulator evidence supports.

### 1.3 Scope and representative campus

Eight campus endpoints and one external test host represent traffic roles. Infrastructure comprises one edge router, one core switch, one distribution switch, two access switches and two APs. Together these make 16 devices in each topology. This is a manageable functional sample, not a real population estimate or saturation-load study. Ground and first-floor labels group zones on a logical canvas; they do not encode actual building dimensions.

## Chapter 2 — Literature Survey

### 2.1 Hierarchical campus architecture

Cisco's campus design guide [1] describes layered campus roles that separate endpoint attachment, aggregation/policy and backbone transport. The project applies these concepts through distinct access switches, a distribution switch owning gateways and ACLs, and a routed core. Production guidance provides architectural context; actual Packet Tracer command support and behavior require independent verification.

### 2.2 WLAN placement and channel planning

Cisco's site-survey guidance [2] supports validating a WLAN against its real environment and application needs. Accordingly, this simulation does not turn AP icons into measured coverage claims. Cisco RF-channel guidance [3] informs the use of distinct channel choices. The implemented channel 1/6 plan is a qualitative improvement in organization over 1/1; no measured interference reduction is claimed.

### 2.3 Addressing and access boundaries

RFC 2131 [4] supplies the DHCP protocol context, including obtaining client addressing through servers and relay agents. RFC 1918 [5] defines private address ranges used in guest restrictions. The project tests actual lease output and forwarding policies rather than inferring success from configuration syntax.

### 2.4 Engineering gap and contribution

These sources do not prove that a particular simulated AP, switch or controller behaves like production hardware. The project's contribution is a reproducible, evidence-linked functional implementation in the installed simulator. The historical WLC forwarding failure illustrates why association and configured VLAN names are insufficient evidence. This is a focused technical-source survey, not a claim of exhaustive peer-reviewed research or a novel RF algorithm.

## Chapter 3 — Methodology

### 3.1 Evidence-first audit and preservation

The starting project contained zero-byte campus .pkt files and an unusable zero-byte original presentation. Historical CSV values lacked supporting measurement evidence. Before implementation, project and capability-lab files were hashed; legacy CSVs were copied unchanged into results/historical. The historical reports, screenshots and uploaded references were retained. Final hashing identified one exception: task-7/tests/H02_wireless_forwarding_diagnostic.pkt changed at 19:26:37 during the initial GUI session; an original byte copy was not recovered. The other 851 of 852 historical files match their initial hashes. The difference is disclosed in the final audit and must not be described as complete byte preservation. Previously verified wired VLAN 10 control remains PASS at 4/4 in both directions including reopen. Historical controller wireless remains FAIL with repeated 0/4; traffic observed in VLAN 99 did not establish the intended VLAN 10 path.

### 3.2 Controlled baseline and optimized pair

Both topologies use the same device models, eight campus endpoint identities, two APs, external host and routed tier structure. Baseline clients share VLAN 1 and 10.10.1.0/24, with no departmental ACLs. Its two APs are centrally clustered on channel 1. The optimized copy assigns role VLANs, applies routing policies and separates AP logical positions, with channels 1 and 6. No baseline link or endpoint was deliberately broken. The experiment changes several design aspects together; it cannot isolate an AP-placement effect from segmentation.

### 3.3 Implementation sequence

1. Place the minimal topology and validate native device interfaces.
2. Configure the functioning shared baseline, DHCP and standalone WLANs.
3. Run baseline probes and save/reopen the native file.
4. Configure optimized access VLANs, 802.1Q trunks, distribution SVIs, routed core, DHCP relay and ACLs.
5. Read back VLAN membership, trunk forwarding state, routes, leases and ACL counters.
6. Run allowed and denied probes with positive controls; preserve initial and repeated outputs.
7. Save/reopen the optimized .pkt, renew the two DHCP clients and retest five critical paths.
8. Derive CSVs and figures from completed transcripts, then assemble the presentation and this report package.

### 3.4 Test interpretation

A permitted test passes when a completed steady-state four-echo probe receives four replies. An initial ARP/convergence trial may receive fewer; original output is retained and a bounded repeat is recorded. A restricted flow passes its policy check when no echo reply is received, the source has a working permitted control and ACL readback/counters support the restriction. Denied probes may report Destination host unreachable from the gateway. These are intentional policy outcomes, not a measured packet-loss rate. Every CSV row links to its actual raw transcript.

## Chapter 4 — Implementation

### 4.1 Device selection and actual roles

The 2911 provides the external-facing routed link and IOS DHCP server. The 3650-24PS supplies routed core transport; its simulated power supply was installed to make the device operational. The 3560-24PS owns all VLAN gateways, helper addresses and inter-role ACLs. Two 2960 switches provide Layer 2 access and trunks. Two standalone AP-PT units bridge one SSID each onto their respective switch access VLAN. Six campus PC-PT devices, two Laptop-PT clients with WPC300N wireless adapters and an external PC complete the topology. The candidate WLC path was not adopted because its prior forwarding failure remained unresolved.

### 4.2 Three-tier forwarding path

```text
External PC6 — 2911 edge / DHCP — 3650 core — 3560 distribution
                                                    |          |
                                               2960 Ground  2960 First
                                               PCs / APs    PCs
```

The distribution–access connections are 802.1Q trunks. Core–distribution and edge–core are routed /30 links. Inter-VLAN packets therefore route at the distribution layer; packets to the external host traverse distribution, core and edge. This is a single-path academic topology without hardware or gateway redundancy.

'''+ptab+'''
Both APs retain wired attachment to the Ground access switch, including AP1 placed logically near the Library. This represents centralized wireless cabling rather than a second-floor local AP uplink. A proposed AP rewire was cancelled when the application offered a delete-device action; the saved topology and port map above record the retained attachment.

### 4.3 VLANs and endpoint addressing

All addresses below are simulation allocations. The baseline campus gateway is 10.10.1.1/24 at distribution VLAN 1; the optimized VLAN gateways are:

'''+vtab+'\n'+etab+'''
Campus endpoint masks are /24; their optimized gateway is the .1 address of their role subnet. The external PC uses /24 and gateway 203.0.113.1. Ground and First access-switch management SVIs are 10.10.99.11 and 10.10.99.12. Baseline Ground management is 10.10.1.11. The core holds a campus summary route toward distribution and a default toward edge. Distribution defaults to core; edge routes the campus 10.10.0.0/16 summary toward core. These broad summaries are sufficient for this isolated exercise and are not an enterprise route-filtering design.

### 4.4 Representative applied CLI

The following excerpts reflect commands applied and accepted on the actual models. Full per-device command sequences are in [submission-evidence/configurations](../submission-evidence/configurations/); the configuration readback and command transcripts are in [logs](../submission-evidence/logs/). These sequences are supporting source files, not exported full running configurations.

```ios
! Access switch, one Student endpoint
vlan 10
 name STUDENTS
interface fastEthernet0/2
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
!
! Distribution uplink to Ground
interface fastEthernet0/2
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 10,20,30,40,50,99
!
! Distribution gateway and relay
ip routing
interface vlan 10
 ip address 10.10.10.1 255.255.255.0
 ip helper-address 10.255.0.1
 ip access-group STUDENTS_IN in
 no shutdown
!
ip access-list extended STUDENTS_IN
 permit udp any eq bootpc any eq bootps
 deny ip any 10.10.30.0 0.0.0.255
 deny ip any 10.10.99.0 0.0.0.255
 deny ip any 10.255.0.0 0.0.255.255
 permit ip any any
```

DHCP is hosted at edge address 10.255.0.1 and reached through the core. Six pools use their corresponding /24 and distribution .1 default gateway; addresses .1 through .20 are excluded. Actual reopened leases were PC1 10.10.10.21 and PC3 10.10.20.21. Router bindings confirm MAC addresses 0030.A3C2.9DB0 and 000B.BE26.9266 respectively. DNS service was not deployed; there is no claimed DNS success.

### 4.5 Access-control policy

Student ingress denies Administration, Management and infrastructure-transit destinations, then permits other IP. Faculty and Administration ingress deny Management and transit destinations but permit other IP. Guest ingress permits DHCP and ICMP to its own gateway, denies RFC 1918 destinations, then permits public destinations. IoT ingress permits DHCP, ICMP to its own gateway and traffic to the designated external test host, then denies other IP. ACL DHCP exceptions precede restrictions. An edge ingress ACL blocks external access to Management and infrastructure transit addresses. Management has no distribution ingress ACL.

These ACLs are stateless. For example, a management-originated external probe's return traffic to VLAN 99 would also meet the edge restriction; unrestricted management Internet access is neither provided nor claimed. The design is not a stateful firewall and does not prevent Layer 2 attacks, address spoofing or traffic between peers within one role VLAN. Faculty-to-Administration reachability represents a permitted resource endpoint, not a tested application service.

### 4.6 Standalone WLAN configuration

AP0 advertises STUDENT_WIFI with WPA2-PSK/AES and uplinks Ground Fa0/5. AP1 advertises GUEST_WIFI and uplinks Ground Fa0/6. The test key CampusLab2026 is a disposable demonstration credential. Both APs use channel 1 in baseline; optimized AP0 uses 1 and AP1 uses 6. The optimized Student and Guest bridge VLANs are 10 and 40 respectively. The wireless clients use matching SSID/security and static role addresses. Actual forwarding is demonstrated by Laptop0 reaching PC0 and Laptop1 reaching the external host; association alone was not treated as success.

### 4.7 Genuine implementation figures

'''
for i,(n,src,caption) in enumerate(figs,1):report+=f'![Figure {i}. {caption}](figures/{n})\n\n**Figure {i}.** {caption}\n\n'
report+='''## Chapter 5 — Results and Discussion

### 5.1 Essential verification outcomes

'''+mdtable(['Requirement','Recorded observation','Outcome'],[
('Within-VLAN switching','PC0 → DHCP Student PC1, 4/4','PASS'),('802.1Q propagation','Two distribution trunks; all six VLANs active and forwarding','PASS'),('Inter-VLAN routing','Student → Faculty and Faculty → Administration, 4/4','PASS'),('DHCP allocation','PC1 and PC3 actual leases plus router bindings, retained after reopen','PASS for tested pools'),('Permitted / denied policies','Eight allowed and five denied optimized probes match their expectations','PASS for sampled flows'),('Standalone wireless data','Student WLAN → wired Student and Guest WLAN → external host, 4/4','PASS'),('Management separation','Authorized PC5 → access/core succeeds; Student/external → management denied','PASS for sampled ICMP paths'),('Native-file persistence','Both .pkt files opened; five optimized follow-up probes match expected outcomes','PASS'),('Controller-based WLAN','Historical VLAN 10 repeated 0/4, VLAN 99 observation; unresolved','FAIL, preserved')])+'''
### 5.2 Complete optimized probe record

Each result is a four-packet completed trial. Eight permitted flows have 4/4 echo replies; five intended denied flows have 0/4. All thirteen therefore pass the specified functional/policy expectation. This is not a performance score.

'''+mdtable(['Test','Expectation','Echo replies','Result','Raw evidence'],[(r['flow'],r['expected'],f"{r['echo_replies']}/4",r['status'],f"[transcript](../{r['evidence']})")for r in opt])+'''
### 5.3 Comparable baseline and optimized flows

Nine identical role-to-role purposes were probed in both designs. Destination addresses change with the VLAN design, while endpoint identities and four-echo method remain comparable. Every baseline flow had 4/4 steady-state replies. The optimized design preserves legitimate connectivity and blocks the four sampled unauthorized campus paths below. The additional external-to-management denial is recorded only in the optimized set.

'''+mdtable(['Comparable flow','Baseline replies','Optimized replies','Optimized expectation'],[(r['label'],f"{r['baseline_received']}/4",f"{r['optimized_received']}/4",r['optimized_expected'])for r in comp])+'''
The [comparison CSV](../results/comparison.csv) records transcript provenance for both sides of every row. Figure 10 and presentation slide 11 chart four representative flows from these records. A zero-height optimized bar means the policy intentionally denied that probe.

### 5.4 Persistence and corroboration

After native reopen, Student and Faculty DHCP leases were renewed and read back. Five further optimized probes cover within-VLAN connectivity, Faculty-to-Administration permission, Guest-to-external permission, Guest-to-Administration denial and Student wireless forwarding. All matched their expected outcomes. Fresh Ground MAC learning shows VLAN 10 wireless traffic on Fa0/5 and VLAN 40 on Fa0/6. Distribution ACL counters record hits on tested permit and deny entries. The baseline was independently reopened and its wireless Student control again received 4/4. The machine-readable [persistence record](../submission-evidence/logs/persistence_results.json) and raw transcripts retain this evidence.

### 5.5 Interpretation and threats to validity

The defensible improvement is the introduction of enforceable role boundaries while sampled permitted paths continue to work. The baseline openly reaches Administration and management because it has no departmental isolation, not because it is malfunctioning. AP distribution and channel configuration are more deliberate in the optimized design, but the experiment did not measure radio contention, useful throughput or signal strength. The same small representative population cannot support claims about hundreds of users or congestion under load. Warm-up differences, ARP, simulation timing and repeated probes are documented rather than hidden.

Historical CSV files remain byte-for-byte archived and excluded from current conclusions. Values such as 50 to 180 Mbps and 78% to 95% coverage lack evidence and are not measured project outcomes. Current canonical CSV files contain verified functional records only.

## Chapter 6 — Conclusion and Future Scope

### 6.1 Conclusion

A functioning baseline and a six-VLAN optimized campus were created and saved in the actual Packet Tracer application. The implementation retains distinct core, distribution and access devices, DHCP relay across a routed core, access trunks, distribution-layer gateways and sampled role-policy enforcement. Basic standalone wireless forwarding works. The saved optimized file retains its behavior after reopening. The evidence supports a functional network segmentation demonstration and an explicit AP/channel planning strategy.

### 6.2 Limitations

'''+limits+'''

### 6.3 Future engineering work

Apply the final institutional report template when supplied, add the five team members' identities and rehearse a demonstration from the saved .pkt files. Further engineering can diagnose the separate WLC VLAN mismatch without rewriting its original outcome, validate all DHCP role pools, add management authentication and service-specific ACLs, and address return traffic with an explicit security model. A real deployment study would require floor plans, RF surveys, client-density/load assumptions and a suitable emulator or measured testbed for throughput, interference, roaming and resilience.

## Verified IEEE-style reference candidates

The following primary sources were checked for relevance. Access date: 5 November 2026. Exact institutional bibliography styling can be applied after the report template arrives. These are vendor/standards references, not invented journal papers.

'''
refs=json.loads((E/'references/verified-reference-candidates.json').read_text())
for i,r in enumerate(refs,1):report+=f"[{i}] {r['author']}, “{r['title']},” "+(r.get('identifier','')+', ' if r.get('identifier') else '')+(r.get('date','')+'. ' if r.get('date') else '')+f"[Online]. Available: {r['url']}. [Accessed: Nov. 5, 2026].\n\n"
report+='''## Evidence package index

- [Baseline native topology](../packet-tracer/baseline/campus_baseline.pkt) and [optimized native topology](../packet-tracer/optimized/campus_optimized.pkt).
- [Presentation](../presentation/Campus_WLAN_Optimization_Final.pptx).
- [Baseline outcomes](../results/baseline.csv), [optimized outcomes](../results/optimized.csv), [comparison data](../results/comparison.csv), [graph](../results/functional-comparison.png).
- [Applied command sequences](../submission-evidence/configurations/), [raw readback and ping transcripts](../submission-evidence/logs/), [genuine captures](../submission-evidence/screenshots/).
- [Figure source/hash manifest](figure-manifest.json) and [execution capture manifest](../submission-evidence/logs/screenshot-manifest.json).
- [Preserved historical data](../results/historical/README.md), [original narrative documents](../submission-evidence/references/original-project-documents/).
- Original capability workspace remains outside this repository at ../PT-Capability-Lab. Its Task 7 reports document the historical wired PASS and WLC wireless FAIL.
'''
write(R/'report-content.md',report)
write(P/'documentation/vlan-plan.md','# Implemented VLAN plan\n\nThe current implementation uses the approved mapping below. Earlier conflicting mappings in the original repository (including swapped Students/Faculty roles) are superseded here; their byte-identical originals are retained in submission-evidence/references/original-project-documents. Earlier requirements and audit documents remain historical planning records.\n\n'+vtab+'\nBaseline campus clients share VLAN 1; optimized clients use the role VLANs. Management VLAN 99 is also native on the two access trunks. It is not an unused black-hole native VLAN and must not be described as that security pattern.\n')
write(P/'documentation/ip-addressing.md','# Implemented simulation addressing\n\nAll values are simulation allocations, not real SRM addresses.\n\n'+vtab+'\n'+etab+'\n'+ptab+'\nCampus endpoint masks are /24 and gateways are distribution .1. Access management addresses are 10.10.99.11 and .12. PC6 gateway is 203.0.113.1. See report/report-content.md for static routes and verified DHCP scope.\n')
write(P/'documentation/architecture.md','''# Implemented three-tier campus architecture

The saved baseline and optimized files contain distinct core, distribution and access devices, with a separate edge router. The optimized architecture is:

```text
External PC — 2911 edge/DHCP — 3650-24PS routed core — 3560-24PS distribution
                                                            |             |
                                                        2960 Ground    2960 First
                                                        PCs and APs    PCs
```

The 3560 owns six SVI gateways, relay agents and inbound role ACLs. The 3650 carries routed /30 links and static routes. Access uplinks are 802.1Q trunks carrying all six VLANs, native 99. Two standalone AP-PT devices attach to Ground access ports; logical AP placement near a zone does not change that wiring. The external PC represents a simulated routed destination, not live Internet.

This is a single-path academic implementation, with no redundancy. Device counts and locations are simulation assumptions. The existing architecture-decision and capability-audit documents record prior decisions; the implemented port map, addressing and measured scope are authoritative in [report-content.md](../report/report-content.md). Original narrative files were archived before reconciliation.
''')
write(P/'documentation/wireless-plan.md','''# Implemented standalone WLAN

Both scenarios use two AP-PT devices, two Laptop-PT/WPC300N clients, STUDENT_WIFI and GUEST_WIFI, and WPA2-PSK/AES. The disposable lab key is CampusLab2026. Each AP bridges one untagged SSID onto one switch access VLAN; tagged multi-SSID operation is not claimed.

| AP | Ground switch port | Baseline | Optimized |
| --- | --- | --- | --- |
| AP0 / Student | Fa0/5 | VLAN 1, channel 1, clustered | VLAN 10, channel 1, Common-area side |
| AP1 / Guest | Fa0/6 | VLAN 1, channel 1, clustered | VLAN 40, channel 6, Library side |

Placement is illustrative on the logical canvas, without measured dimensions or RF gains. AP1 retains its Ground-switch uplink even though logically placed near the Library. Both Student-to-wired and Guest-to-external forwarding were actually tested. The historical controller VLAN 10 forwarding failure remains unresolved and unchanged; no WLC success is claimed. Faculty, Administration, IoT proxy and Management are wired representatives.
''')
write(P/'documentation/testing.md','''# Executed essential tests

Execution date: 5 November 2026. Installed simulator: Packet Tracer 9.0.1.0858. Both native files were created, saved and reopened through the application.

The canonical [baseline](../results/baseline.csv) and [optimized](../results/optimized.csv) records link every four-packet outcome to an actual transcript. Nine baseline probes and thirteen optimized probes matched their expectations. Optimized has eight allowed 4/4 flows and five intended denied 0/4 flows. VLAN membership, all-six-VLAN trunk forwarding, SVI/routing readback, two actual DHCP leases and ACL counters corroborate the probes. Five optimized paths and two DHCP clients were checked again after reopening; baseline wireless was also rechecked after reopening.

Preserve first ARP/convergence trials and bounded repeats. An intended ACL denial is a policy PASS, not a network packet-loss measurement. An associated wireless client is insufficient evidence without data forwarding. Historical Task 7 wired VLAN 10 PASS and WLC wireless FAIL remain unchanged outside the repository.

See [the report](../report/report-content.md) for complete procedures, addresses and limits, and [persistence outcomes](../submission-evidence/logs/persistence_results.json) for saved-file checks.
''')
write(P/'documentation/results.md','''# Verified functional results

Current CSVs are derived from actual completed Packet Tracer transcripts. Legacy unsupported throughput and coverage values were preserved unchanged in [results/historical](../results/historical/README.md) and excluded from conclusions.

'''+mdtable(['Flow','Baseline replies / 4','Optimized replies / 4','Optimized policy'],[(r['label'],r['baseline_received'],r['optimized_received'],r['optimized_expected'])for r in comp])+'''
All nine baseline probes functioned. All thirteen optimized probes matched expected permission or denial. Two DHCP role pools were actually exercised; six pools are configured. Both standalone wireless clients have verified permitted data forwarding. The historical WLC failure remains unresolved.

![Observed functional comparison](../results/functional-comparison.png)

The graph shows functional probe reply counts, not throughput, coverage, latency or generic packet-loss improvement. Full evidence and limitations: [report-content.md](../report/report-content.md).
''')
write(P/'README.md','''# Campus WLAN Optimization Using Access Point Placement and Network Segmentation

SRM Institute of Science and Technology · five-member academic capstone · hypothetical two-floor campus · Cisco Packet Tracer 9.0.1.0858.

## Current status

The baseline and optimized native topologies are implemented, saved and reopened in the installed simulator. Both contain distinct core, distribution and access layers plus a separate edge router. Nine baseline connectivity probes and thirteen optimized permission/denial probes matched their expected outcomes. Six role VLANs, 802.1Q trunks, distribution routing, DHCP relay, ACL policies and basic standalone wireless forwarding have recorded evidence. Two DHCP role pools were actually exercised; six are configured.

## Submission artifacts

- [Baseline topology](packet-tracer/baseline/campus_baseline.pkt).
- [Optimized topology](packet-tracer/optimized/campus_optimized.pkt).
- [12-slide final presentation](presentation/Campus_WLAN_Optimization_Final.pptx).
- [Six-chapter report content and evidence package](report/report-content.md), awaiting the final report-format template.
- [Baseline outcomes](results/baseline.csv), [optimized outcomes](results/optimized.csv), [comparison CSV](results/comparison.csv), [functional graph](results/functional-comparison.png).
- [Actual configuration transcripts and probe logs](submission-evidence/logs/), [applied command sequences](submission-evidence/configurations/), [genuine screenshots](submission-evidence/screenshots/).
- [Implemented VLAN mapping](documentation/vlan-plan.md), [IP/port map](documentation/ip-addressing.md), [wireless design](documentation/wireless-plan.md).

## Scenario and interpretation

Ground floor: Classrooms, Computer laboratory, Common area. First floor: Library and Faculty/administration. The 16-device simulation includes eight campus endpoints, two APs and an external test PC. These are simulation assumptions, not real SRM counts or an equipment procurement design. PC2 is an IoT network-policy proxy, not a validated IoT appliance.

The baseline uses a functioning shared client VLAN. The optimized design uses VLAN 10 Students, 20 Faculty, 30 Administration, 40 Guests, 50 IoT and 99 Management. Distribution owns the six .1 gateways; core links are routed. Student/Guest/IoT restrictions and management separation are demonstrated by actual allowed and denied ICMP probes. Eight optimized allowed flows receive 4/4; five denied flows receive 0/4 as intended. These are sampled policy outcomes, not a measured performance percentage.

## Reproduce a short demonstration

1. Open either .pkt from Packet Tracer File → Open. Use the exact file path if multiple application instances are running.
2. In optimized, open PC1 and PC3 → Desktop → IP Configuration. Confirm DHCP addresses 10.10.10.21 and 10.10.20.21, /24, gateways .1. Saved leases may need renewal/time to converge.
3. From PC0 Desktop → Command Prompt, ping 10.10.10.21 (permit) and 10.10.30.10 (deny). From PC3 ping 10.10.30.10 (permit).
4. From Laptop0 ping 10.10.10.10. From Laptop1 ping 203.0.113.10 (permit) and 10.10.30.10 (deny).
5. Distribution CLI: `show interfaces trunk`, `show ip interface brief`, `show ip route`, `show access-lists`. Edge CLI: `show ip dhcp binding`. Access CLI: `show vlan brief`.
6. Allow initial ARP/STP convergence; retain first output and a completed repeated positive probe. Expected ACL rejection is not a connectivity fault.

## Limits and preserved findings

Standalone AP-PT forwarding is verified. The separate historical WLC VLAN 10 forwarding test still FAILS and its root cause is unresolved. Its original wired VLAN 10 control remains PASS. Historical reports and screenshots are unchanged. Final hashing found 851 of 852 historical files unchanged; task-7/tests/H02_wireless_forwarding_diagnostic.pkt was saved during the initial GUI session and no original byte copy was recovered. Its original/new hashes and the preservation exception are recorded in submission-evidence/logs/final-audit.json. Do not describe the entire capability workspace as byte-identical. Original uploaded references and the original zero-byte presentation are retained.

There are no measured throughput, latency, RF coverage, congestion or roaming improvements. Logical AP positions and channels 1/6 express a planning strategy. No physical floor RF model is claimed. The external PC is a simulated routed host, not real Internet; DNS/NAT/SSH and production authentication are not implemented. Management evidence is ICMP reachability and filtering only. Stateless ACL return-traffic limitations are discussed in the report.

Unsupported legacy metric CSVs are archived byte-for-byte in [results/historical](results/historical/README.md). Earlier conflicting repository VLAN mappings were reconciled in the current implementation notes; original narrative files are retained in submission-evidence/references/original-project-documents. Older requirements/audit documents remain historical planning records rather than claims that all proposed features were implemented.

## Remaining submission work

Provide the institutional report template and five team members' names/register numbers, apply final formatting, and rehearse the saved-file demonstration. WLC repair and real RF/capacity validation are future engineering work. No Git commits or software installations were made during implementation.
''')
print('Report words',len(report.split()),'curated figures',len(figs))
