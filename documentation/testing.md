# Executed essential tests

Execution date: 5 November 2026. Installed simulator: Packet Tracer 9.0.1.0858. Both native files were created, saved and reopened through the application.

The canonical [baseline](../results/baseline.csv) and [optimized](../results/optimized.csv) records link every four-packet outcome to an actual transcript. Nine baseline probes and thirteen optimized probes matched their expectations. Optimized has eight allowed 4/4 flows and five intended denied 0/4 flows. VLAN membership, all-six-VLAN trunk forwarding, SVI/routing readback, two actual DHCP leases and ACL counters corroborate the probes. Five optimized paths and two DHCP clients were checked again after reopening; baseline wireless was also rechecked after reopening.

Preserve first ARP/convergence trials and bounded repeats. An intended ACL denial is a policy PASS, not a network packet-loss measurement. An associated wireless client is insufficient evidence without data forwarding. Historical Task 7 wired VLAN 10 PASS and WLC wireless FAIL remain unchanged outside the repository.

See [the report](../report/report-content.md) for complete procedures, addresses and limits, and [persistence outcomes](../submission-evidence/logs/persistence_results.json) for saved-file checks.
