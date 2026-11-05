# Implemented three-tier campus architecture

The saved baseline and optimized files contain distinct core, distribution and access devices, with a separate edge router. The optimized architecture is:

```text
External PC — 2911 edge/DHCP — 3650-24PS routed core — 3560-24PS distribution
                                                            |             |
                                                        2960 Ground    2960 First
                                                        PCs and APs    PCs
```

The 3560 owns six SVI gateways, relay agents and inbound role ACLs. The 3650 carries routed /30 links and static routes. Access uplinks are 802.1Q trunks carrying all six VLANs, native 99. Two standalone AP-PT devices attach to Ground access ports; logical AP placement near a zone does not change that wiring. The external PC represents a simulated routed destination, not live Internet.

This is a single-path academic implementation, with no redundancy. Device counts and locations are simulation assumptions. The existing architecture-decision and capability-audit documents record prior decisions; the implemented port map, addressing and measured scope are authoritative in [report-content.md](../report/report-content.md). Original narrative files were archived before reconciliation.
