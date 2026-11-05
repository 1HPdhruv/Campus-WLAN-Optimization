# Campus WLAN Optimization Using Access Point Placement and Network Segmentation

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
