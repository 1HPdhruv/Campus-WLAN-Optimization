# Packet Tracer Capability Test Plan

**Project:** Campus WLAN Optimization Using Access Point Placement and Network Segmentation  
**Target simulator:** Cisco Packet Tracer 9.0.1  
**Prepared:** 3 November 2026  
**Status:** Plan only. Every exercise and model pairing is **NOT RUN**. Expected outcomes below are acceptance criteria, not observations.  
**Approved campus architecture:** Distinct Core, Distribution and Access switching layers, with a separate edge router. Disposable capability fixtures intentionally omit unrelated layers; they are not the final campus topology.

## 1. Verified palette inventory

The following visibility evidence was supplied by the project team in Task 5 after visual inspection. The inventory preserves the reported labels, including abbreviated GUI names. Codex has not independently repeated that GUI inspection. Palette visibility establishes availability for evaluation, not correct operation or compatibility.

| Category | Team-confirmed visible labels |
| --- | --- |
| Routers | 4331; 4321; 1941; 2901; 2911; 829; IR1101; 1841; 2811; 2620XM; 2621XM; PT-Router |
| Switches | 2960; PT-Switch; 3560-24PS; 3650-24PS; IE-2000; IE-3400; IE-9320; 2950-24; 2950T |
| Wireless | LAP-PT; 3702i; WLC; WLC 3504; WLC 2504; AP-PT; AP-PT-A; AP-PT-AC; AP-PT-N; WRT300N; Meraki |
| End devices | PC; Laptop; Server; Network Controller; Printer; Tablet; Smartphone; Generic Wireless; Generic Wired; Sniffer |

IoT smart-device models were not individually identified in the supplied inventory. Exercise I must discover and record them. A Network Controller is not automatically a WLAN controller, and a generic wireless endpoint is not automatically an IoT sensor. Do not expand “Meraki” into an unverified exact model name.

Earlier [capability audit](packet-tracer-capability-audit.md) and [architecture decision](architecture-decision.md) are historical records. Task 5 supplies newer palette evidence, while Tasks 4–5 establish the mandatory full three-tier architecture. Existing documents remain unchanged.

## 2. Provisional device shortlist

| Candidate | Intended campus role | Required capability evidence before a final recommendation |
| --- | --- | --- |
| 2911 | Edge router | C2 routed transit/static return path; D1 DHCP where desired; later edge/NAT/security tests if required by the approved upstream design. |
| 3650-24PS | Core | A/B VLAN and transport checks as applicable, C1 repeated on this model, C2 routed ports/static routing. Port/media budgets remain unapproved. |
| 3560-24PS | Distribution | C1 SVI routing, D2/D3 DHCP or relay as selected, E ACL attachment/enforcement and B trunk compatibility. |
| 2960 | Access | A VLAN membership and B tagged transport, with exact interface labels recorded. It is not selected as an inter-VLAN router. |
| 3702i / LAP-PT | Controller-managed AP | H registration, compatible client association, security and actual client forwarding; test each candidate separately. |
| WLC 2504 / WLC 3504 | WLAN controller | H per-pair registration and data-plane tests. A result for one controller cannot certify the other. |
| AP-PT | Standalone control fixture | F/G isolate basic SSID/security/bridging behavior. This is not automatic approval of AP-PT for multi-SSID campus service. |

All selections remain provisional. These tests do not determine final counts, AP locations, real campus capacity, gateway placement or the campus IP plan. QoS, production-like throughput, automatic balancing and roaming guarantees are outside A–J and remain open if later required.

## 3. Test objectives

| Exercise | Objective | Smallest useful fixture described here |
| --- | --- | --- |
| A | Create the six VLAN IDs and demonstrate membership/isolation. | One 2960 and two PCs: 3 devices. |
| B | Demonstrate 802.1Q transport and allowed-VLAN enforcement. | Two switches and two PCs: 4 devices; substitute one candidate per repeat. |
| C1 | Demonstrate multilayer SVI routing. | One multilayer switch and two PCs: 3 devices. Repeat on 3560 and 3650 separately. |
| C2 | Verify core/edge routed ports and static routes. | One 3650, one 2911 and two PCs: 4 devices. |
| D1 | Verify 2911 DHCP server behavior. | One 2911 and one PC: 2 devices, direct cable. |
| D2 | Verify DHCP pools on a multilayer switch. | One multilayer switch and one PC: 2 devices; second PC optional. |
| D3 | Verify server-based DHCP relay fallback. | One multilayer switch, one Server and one PC: 3 devices. |
| E | Prove an ACL selectively allows HTTP and blocks another routed flow. | One multilayer switch, one PC and one Server: 3 devices. |
| F | Inspect/configure standalone SSID, channel and security controls. | One AP-PT: 1 device. |
| G | Verify association and wireless-to-wired bridging. | F's AP plus one Laptop and one wired PC: 3 devices total. |
| H | Verify controller/AP registration, then WLAN-to-VLAN forwarding. | One 3560, one WLC, one AP, one admin PC, one Laptop: 5 devices, contingent on D2. Add one DHCP Server only if D3 fallback is needed. |
| I | Distinguish IP smart devices from components and test registration/connectivity. | Palette inspection first; then one switch, one IP-capable Thing, one Server and one PC: 4 devices. Add an AP only for a wireless-only Thing. |
| J | Inspect ARP/ICMP and Simulation Mode without unrelated routing. | Two PCs: 2 devices, direct cable. Can also reuse a known-good fixture. |

### 3.1 Execution boundaries and preflight

These instructions are for later manual execution. Preparing this document does not execute or save any lab. Use fresh disposable workspaces, never the baseline/optimized files. Do not copy test addressing, test passwords or test VLAN names into the eventual campus plan. No software installation, preferences changes or repository changes are needed to run these exercises.

Before each exercise:

1. Record the About version/build, exact palette/device label, operator and test ID. Preserve any other open work.
2. Use a fresh device instance or a separately maintained disposable fixture with known state. Avoid carrying ACLs, DHCP pools or cached wireless profiles between unrelated tests.
3. On IOS devices, decline the initial configuration dialog if it appears, then inspect `show ip interface brief` and, where supported, `show interfaces status`. Discover interface names rather than assuming numbering.
4. Use Copper Straight-Through for client-to-switch and AP/controller-to-switch links. Use the automatic connection tool for switch-to-switch, switch-to-router or direct PC/router and PC/PC fixtures when cable polarity is uncertain. Record actual ports/media chosen.
5. Wait for device startup and forwarding state; allow ARP/DHCP convergence before evaluating steady-state traffic. A first failed ping is not a final failure verdict.
6. Paste one command block at a time. Capture rejected commands and parser help. Do not paste both alternative model-specific interface variants into one device.

**Port conventions used in examples:** 2960/3560 access ports `FastEthernet0/1`, `FastEthernet0/2`; their example uplink `GigabitEthernet0/1`; 3650 equivalents `GigabitEthernet1/0/1`, `GigabitEthernet1/0/2`, with routed uplink `GigabitEthernet1/0/24`; 2911 `GigabitEthernet0/0` and `GigabitEthernet0/1`. These are conventional lab labels to verify against the actual instance. Substitute the discovered interface consistently if it differs. On a 3650, inspect that any required simulated power module is present before diagnosing a dark device as a protocol failure.

### 3.2 Temporary addressing ledger

All addresses are **disposable lab assumptions**, not campus allocations. The RFC 1918 private addresses below must remain inside the isolated Packet Tracer exercises. `/24` is used for readability, not as a final subnet-sizing decision.

| Test network | Temporary use | Key addresses |
| --- | --- | --- |
| 172.31.10.0/24 | Student-role test VLAN 10 or a flat test link | Gateway .1 when present; WLC dynamic interface .2 in H2; PCs .11/.12; wireless client .21 in static G; wired G target .22. |
| 172.31.20.0/24 | Faculty-role test VLAN 20 | Gateway .1; WLC dynamic interface .2 in H2; PC .11; E HTTP Server .10. |
| 172.31.30.0/24 | C2 edge-side test LAN | 2911 .1; remote PC .11. This lab is not an administration policy test. |
| 172.31.50.0/24 | I IoT test LAN | Registration Server .2; admin PC .10; Thing .21. No router/gateway needed for same-LAN minimum. |
| 172.31.99.0/24 | H management or D3 service fixture | Multilayer SVI .1; WLC .2 in H or Server .2 in D3, never both in one fixture; admin PC .10. |
| 172.31.254.0/30 | C2 point-to-point transit | 3650 .1; 2911 .2; mask 255.255.255.252. |

Unless overridden, use mask `255.255.255.0`. For flat tests without a router, leave the default gateway blank (or the simulator's unspecified value), not an invented reachable gateway. No duplicate .2 service/controller assignments may coexist. For H, reserve .1–.20 and use DHCP starting above .20; counts and lease sizes are lab parameters only. Do not set a DNS option pointing to an unconfigured server; use literal test URLs/addresses instead.

## 4. Detailed test procedures

### A. VLAN creation and port assignment

**Devices/connections:** one fresh 2960; PC-A NIC → Fa0/1; PC-B NIC → Fa0/2. No router. Set PC-A `172.31.10.11/24`, PC-B `172.31.10.12/24`, gateways blank via **Desktop → IP Configuration → Static**.

**GUI:** switch → **CLI**; alternative readback at **Config → VLAN Database** and **Config → interface**. Configure all six role IDs using test-prefixed names:

```text
enable
configure terminal
vlan 10
 name TEST_STUDENTS
exit
vlan 20
 name TEST_FACULTY
exit
vlan 30
 name TEST_ADMIN
exit
vlan 40
 name TEST_GUESTS
exit
vlan 50
 name TEST_IOT
exit
vlan 99
 name TEST_MANAGEMENT
exit
interface FastEthernet0/1
 switchport mode access
 switchport access vlan 10
 no shutdown
exit
interface FastEthernet0/2
 switchport mode access
 switchport access vlan 10
 no shutdown
end
show vlan brief
```

1. PC-A → **Desktop → Command Prompt**: `ping 172.31.10.12`. Expect eventual successful replies with both ports in VLAN 10.
2. Move only PC-B's port:

```text
configure terminal
interface FastEthernet0/2
 switchport access vlan 20
end
show vlan brief
```

3. Repeat ping. Expect failure because the same-subnet PCs are now in distinct Layer 2 domains and no router is present. Keeping their IPs unchanged is deliberate for this isolation control, not a production subnet design.
4. Restore Fa0/2 to VLAN 10 and confirm recovery.

**Pass:** all six IDs exist, port membership follows each change, same-VLAN connectivity works and separated-VLAN connectivity fails, then recovers. **Fail/inconclusive:** baseline connectivity never works, wrong port is changed, or an unintended path/gateway allows traffic. Fix fixture faults before concluding feature absence.

**Limits:** creation validates six IDs, not six complete security policies. Default VLAN entries may remain. Repeat on the candidate multilayer switches when VLAN-command compatibility is required; model interface names differ.

### B. 802.1Q trunking

**Devices/connections:** two 2960s S1/S2; one PC on Fa0/1 of each; S1 Gi0/1 ↔ S2 Gi0/1. PCs `172.31.10.11/24` and `.12/24`, gateways blank. Reuse A's six-VLAN creation commands on **both** switches and assign each PC access port to VLAN 10.

**GUI:** **CLI**; readback **Config → uplink interface → VLAN Switch Mode**. On each switch:

```text
enable
configure terminal
interface GigabitEthernet0/1
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30,40,50,99
 no shutdown
end
show interfaces trunk
show interfaces GigabitEthernet0/1 switchport
```

1. Confirm both ends show operational trunking with VLAN 10 active/forwarding and consistent native VLAN. Keep the default native VLAN in this fixture; user test traffic uses tagged VLAN 10.
2. Ping between PCs; expect replies. Optional Simulation inspection can look for model-exposed 802.1Q fields, but lack of a displayed tag alone is not an operational verdict.
3. On S1 only, temporarily remove VLAN 10 from the allowed list:

```text
configure terminal
interface GigabitEthernet0/1
 switchport trunk allowed vlan 20,30,40,50,99
end
show interfaces trunk
```

4. Expect PC-to-PC connectivity to fail. Restore the complete list and confirm recovery.

**Pass:** operational trunk, allowed/active VLAN evidence, successful VLAN 10 traffic, expected pruning failure and recovery. **Fail:** a valid unpruned fixture cannot carry VLAN traffic after link/STP/VLAN checks, or pruning has no intended effect after ruling out another path.

**Model repeats:** replace S2 with 3560, then 3650, one at a time. If a multilayer device rejects `switchport mode trunk` because encapsulation is negotiable, inspect interface `?` and use `switchport trunk encapsulation dot1q` first **only where accepted**. A fixed-802.1Q 2960 may reject that encapsulation-selection command while supporting trunking correctly. Configure a 3650 uplink using its discovered Gi1/0/x name.

### C. Inter-VLAN routing and routed candidate checks

#### C1. Multilayer SVI routing

**Devices/connections:** one 3560-24PS, PC-A on Fa0/1, PC-B on Fa0/2. No router/access switch is needed to isolate SVI routing. Repeat later on a fresh 3650 with Gi1/0/1 and Gi1/0/2.

**GUI:** device **CLI**; PCs **Desktop → IP Configuration**. PC-A `172.31.10.11/24`, gateway `172.31.10.1`; PC-B `172.31.20.11/24`, gateway `172.31.20.1`.

```text
enable
configure terminal
vlan 10
 name TEST_STUDENTS
exit
vlan 20
 name TEST_FACULTY
exit
interface FastEthernet0/1
 switchport mode access
 switchport access vlan 10
 no shutdown
exit
interface FastEthernet0/2
 switchport mode access
 switchport access vlan 20
 no shutdown
exit
interface Vlan10
 ip address 172.31.10.1 255.255.255.0
 no shutdown
exit
interface Vlan20
 ip address 172.31.20.1 255.255.255.0
 no shutdown
exit
no ip routing
end
show ip interface brief
```

Confirm each PC can reach its own gateway; routed PC-to-PC traffic should fail while forwarding is disabled. Then:

```text
configure terminal
ip routing
end
show ip route
show ip interface brief
```

Ping PC-A → `172.31.20.11` and PC-B → `172.31.10.11`.

**Expected/pass:** both SVIs up/up, connected routes for both /24s when routing is enabled, correct client gateways, bidirectional reachability only with routing enabled. Some IOS variants also display local /32 routes; exact formatting is not the criterion. **Fail:** no forwarding after confirming addressing, SVI state and active member ports. An SVI down because its VLAN has no live forwarding port is a fixture issue.

**Limits:** a 2960 management SVI is not equivalent to multilayer forwarding. A passing 3560 result does not certify 3650; run the same test with the correct ports. Gateway placement here is a lab device function, not a final campus core/distribution decision.

#### C2. 3650 routed uplink and 2911 static routes

**Minimum:** 3650 + 2911 + PC-A + PC-R. On the 3650, establish C1's VLAN 10 PC port and SVI with routing enabled; VLAN 20 and PC-B are unnecessary. Connect 3650 Gi1/0/24 ↔ 2911 Gi0/0; PC-R ↔ 2911 Gi0/1. PC-A is `.10.11/24`, gateway `.10.1`; PC-R `172.31.30.11/24`, gateway `172.31.30.1`.

On 3650:

```text
enable
configure terminal
interface GigabitEthernet1/0/24
 no switchport
 ip address 172.31.254.1 255.255.255.252
 no shutdown
exit
ip routing
ip route 172.31.30.0 255.255.255.0 172.31.254.2
end
show ip route
show ip interface brief
```

On 2911:

```text
enable
configure terminal
interface GigabitEthernet0/0
 ip address 172.31.254.2 255.255.255.252
 no shutdown
exit
interface GigabitEthernet0/1
 ip address 172.31.30.1 255.255.255.0
 no shutdown
exit
ip route 172.31.10.0 255.255.255.0 172.31.254.1
end
show ip route
```

**GUI/test:** use both PCs' Command Prompt; ping each remote PC. Verify transit neighbors first if forwarding fails. Temporarily remove the 2911 return route with `no ip route 172.31.10.0 255.255.255.0 172.31.254.1`, observe failure, then restore it and retest.

**Pass:** routed port operates, both static routes appear with the intended next hops, bidirectional client traffic works, removal/restoration of the return route has the expected effect. **Fail/blocked:** rejected model functions or unresolved route/interface problems must be recorded separately. **Limit:** no NAT, real Internet, redundancy or full three-tier integration is established by this small fixture.

### D. DHCP configuration

Run D1 to evaluate the 2911. Run D2 to evaluate local multilayer DHCP; it is an independent capability, not inferred from C. D3 is the server/relay alternative. Do not leave multiple unintended DHCP servers active in the same fixture.

#### D1. 2911 DHCP server

**Minimum:** one 2911 directly connected to one PC using automatic cable selection. **GUI:** router **CLI**; PC **Desktop → IP Configuration → DHCP** after configuring:

```text
enable
configure terminal
interface GigabitEthernet0/0
 ip address 172.31.10.1 255.255.255.0
 no shutdown
exit
ip dhcp excluded-address 172.31.10.1 172.31.10.20
ip dhcp pool TEST10
 network 172.31.10.0 255.255.255.0
 default-router 172.31.10.1
exit
end
show ip dhcp pool
show ip dhcp binding
```

Inspect PC `ipconfig`; ping `172.31.10.1`. **Expected/pass:** a lease within the correct /24, outside reserved .1–.20, mask/gateway correct, binding correlated with the PC where output is supported, and gateway reachable. No exact first lease address or lifetime is guaranteed. **Fail:** persistent lack of a lease/wrong scope after link/server checks. A self-assigned 169.254.x.x address is not a valid lease.

**Limits:** no DNS service is configured, so DNS is deliberately omitted. Modelled lease timers/counters may be incomplete. This result says nothing yet about distribution-switch DHCP or relay.

#### D2. Multilayer DHCP pools

**Minimum:** one 3560 with C1 VLAN 10/SVI and one attached PC. Do not include D1's router. Repeat on a fresh 3650 using the C1 port substitutions if local core DHCP is being considered.

Apply D1's `ip dhcp excluded-address` and `ip dhcp pool TEST10` commands on the multilayer switch; use C1's SVI instead of the router interface. For a second client in VLAN 20, optionally add:

```text
configure terminal
ip dhcp excluded-address 172.31.20.1 172.31.20.20
ip dhcp pool TEST20
 network 172.31.20.0 255.255.255.0
 default-router 172.31.20.1
exit
end
show ip dhcp binding
```

**GUI/test:** select DHCP on the applicable PC interface, inspect its lease, ping its gateway; if both clients are present, also verify C1 forwarding. **Pass:** model accepts the service commands and supplies the correct scope/gateway. **Fail/unsupported subset:** preserve parser errors or service failure after fixture checks. **Limit:** successful routing does not imply a DHCP server implementation; use D3 if necessary rather than declaring the whole switch unsuitable.

#### D3. Server DHCP and relay

**Minimum:** fresh 3560 + PC in VLAN 10 + Server in VLAN 99. Establish C1's VLAN 10 access/SVI/routing; connect Server to Fa0/3. Server address `172.31.99.2/24`, gateway `172.31.99.1`. This is an isolated service fixture, not approval to host campus shared services in management VLAN 99.

```text
enable
configure terminal
vlan 99
 name TEST_MANAGEMENT
exit
interface FastEthernet0/3
 switchport mode access
 switchport access vlan 99
 no shutdown
exit
interface Vlan99
 ip address 172.31.99.1 255.255.255.0
 no shutdown
exit
interface Vlan10
 ip helper-address 172.31.99.2
end
show ip interface Vlan10
```

**GUI:** Server → **Desktop → IP Configuration** for static addressing; **Services → DHCP → On**. Add pool `TEST10_RELAY`: gateway `172.31.10.1`, start `172.31.10.21`, mask `255.255.255.0`, maximum users `5`; leave DNS unspecified/0.0.0.0 if required by the UI. Add/Save according to the visible controls. Ensure no default or other active scope competes with this test. The PC selects DHCP.

**Expected/pass:** correct VLAN 10 lease and gateway, PC can reach gateway and Server; Simulation Mode can show relayed DHCP with the relevant gateway context where exposed. For the negative control, enter `interface Vlan10` in configuration mode and remove the helper with `no ip helper-address 172.31.99.2`; start a fresh discover. Cross-subnet acquisition should fail until `ip helper-address 172.31.99.2` is restored. Use `ipconfig /release` and `/renew` only if accepted, or switch Static → DHCP to restart. Verify a new DHCP Discover in Simulation Mode: a cached lease or unicast renewal is not evidence for this negative control. If fresh acquisition cannot be established, mark that control inconclusive.

**Fail:** wrong pool/no new lease after verifying both VLANs, server gateway, routing, service state and helper. **Limits:** exact server fields differ by build; document any UI substitution. A second VLAN/PC is optional after the minimum passes. A same-VLAN DHCP success does not prove relay.

### E. ACL enforcement

**Minimum:** one 3560 + one student-test PC + one HTTP Server. Use C1's VLANs/SVIs/access ports and routing, with Server replacing PC-B. PC `172.31.10.11/24`, gateway `.10.1`; Server `172.31.20.10/24`, gateway `.20.1`.

**GUI:** Server → **Services → HTTP → On**. From PC **Command Prompt**, ping the Server; from **Web Browser**, open `http://172.31.20.10`. Confirm both work before filtering. On the switch:

```text
enable
configure terminal
ip access-list extended TEST_STUDENT_IN
 permit tcp 172.31.10.0 0.0.0.255 host 172.31.20.10 eq 80
 deny ip 172.31.10.0 0.0.0.255 172.31.20.0 0.0.0.255
 permit ip any any
exit
interface Vlan10
 ip access-group TEST_STUDENT_IN in
end
show access-lists
show ip interface Vlan10
```

Retry ping and reload the literal HTTP URL, generating a new request rather than relying on a previously displayed page. Expect HTTP to work, Server ping to fail, and PC's own gateway ping to remain permitted. Remove only the attachment:

```text
configure terminal
interface Vlan10
 no ip access-group TEST_STUDENT_IN in
end
```

Confirm Server ping recovers. **Pass:** unfiltered controls worked, policy is attached in the intended direction, HTTP remains usable, ICMP is blocked and removal restores it. **Fail/inconclusive:** HTTP was already broken, cached content is mistaken for a new transaction, or both protocols are affected contrary to the defined policy. Counters are supporting evidence; missing/inaccurate counters do not outweigh observed forwarding.

**Limits:** this intentionally permissive test ACL is not the final campus policy. It does not implement stateful inspection or same-VLAN isolation. Return HTTP traffic enters VLAN 20 without this source-VLAN filter. Repeat on 3650 only if ACL enforcement is needed there; record each model separately.

### F. Basic wireless SSID configuration

**Minimum:** one standalone **AP-PT**, no client yet. This control fixture deliberately does not use a controller-managed 3702i/LAP-PT as an autonomous AP.

**GUI:** AP → **Config → wireless port** (record its actual name). Enable the port, set SSID `CAPABILITY-LAB`, choose channel `1` if offered, choose **WPA2-PSK / AES** if exposed and enter temporary passphrase `LabOnly-WiFi-2026`. Read back the fields after navigating away/back; use Apply only if present. No IOS commands are required for this GUI AP.

**Expected/pass:** requested values persist and the interface is enabled. Record all exposed channel/security options without claiming that a saved SSID proves association. **Partial/blocked:** record missing AES/WPA2/channel controls or a model with only controller-managed settings. Do not substitute WEP and call the WPA2 criterion passed.

**Limits:** channel 1 is a lab choice, not campus channel planning or a measured interference improvement. This validates one SSID's controls, not multiple SSIDs or tagging. Repeat on AP-PT-A/AC/N only when that model is relevant; do not assume equal controls.

### G. Wireless client association and bridging

**Minimum:** F's AP-PT + Laptop + wired PC. Connect the AP Ethernet port directly to the PC NIC using automatic cable selection. Keep Laptop within the modelled range. No router, DHCP server or switch is needed.

1. Laptop → **Physical**: inspect its module. If no suitable radio is present, in this disposable device only, power off, replace the Ethernet module with the compatible laptop wireless module (such as WPC300N if available), then power on. Record exact module/band; do not change software or reuse a module incompatible with the AP.
2. Laptop → **Desktop → PC Wireless → Connect**: refresh, select `CAPABILITY-LAB`, choose matching WPA2/AES settings and enter F's lab key. Some client models expose **Config → Wireless0** instead; use the observed path and record it.
3. Give the active wireless interface `172.31.10.21/24`, wired PC `172.31.10.22/24`, gateways blank. Confirm which interface `ipconfig` describes.
4. Inspect client Link Information/association details and ping the wired PC; ping the Laptop from the wired PC. Trace one exchange through the AP in Simulation Mode if needed.
5. Disconnect/remove the test association/profile, reconnect with an incorrect key and confirm no fresh usable association/data flow. Then reconnect with the correct key and confirm recovery. If cached association cannot be cleared reliably, mark the negative credential test inconclusive rather than passed.

**Pass:** correct association and bidirectional wireless-to-wired traffic; credential rejection and recovery recorded separately. **Fail:** association/data remains broken after checking radio, port, range, addressing and credentials. **Limits:** the AP's GUI Ethernet port may not have an IP setting; a bridging AP needs no test gateway address. A link graphic alone is not a pass. This exercise does not prove controller compatibility, VLAN tagging, roaming or realistic throughput.

### H. Controller and lightweight AP compatibility

#### H0. Fixture and per-pair scope

**Minimum:** one 3560 (D2 must already pass), one WLC 2504, one 3702i, one admin PC, one wireless Laptop: five devices. No edge/core layer is needed in this capability fixture. Test these four pairings independently using fresh candidate instances: WLC 2504 + 3702i; WLC 2504 + LAP-PT; WLC 3504 + 3702i; WLC 3504 + LAP-PT. The generic WLC is not a silent replacement for a failing candidate.

Connections: admin PC → Fa0/1, AP wired uplink → Fa0/2, WLC data port `1` → Gi0/1. Confirm the controller's exact data-port label; do not confuse its logical management interface with a cable port. AP power and the Laptop's radio compatibility must be verified.

**Temporary management:** SVI 99 `172.31.99.1/24`; WLC management `.99.2`; admin PC `.99.10`, gateway `.99.1`; AP uses DHCP. Configure the switch:

```text
enable
configure terminal
vlan 10
 name TEST_STUDENTS
exit
vlan 20
 name TEST_FACULTY
exit
vlan 99
 name TEST_MANAGEMENT
exit
interface FastEthernet0/1
 switchport mode access
 switchport access vlan 99
 no shutdown
exit
interface FastEthernet0/2
 switchport mode access
 switchport access vlan 99
 no shutdown
exit
interface GigabitEthernet0/1
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 10,20,99
 no shutdown
exit
interface Vlan99
 ip address 172.31.99.1 255.255.255.0
 no shutdown
exit
interface Vlan10
 ip address 172.31.10.1 255.255.255.0
 no shutdown
exit
interface Vlan20
 ip address 172.31.20.1 255.255.255.0
 no shutdown
exit
ip routing
ip dhcp excluded-address 172.31.99.1 172.31.99.20
ip dhcp excluded-address 172.31.10.1 172.31.10.20
ip dhcp excluded-address 172.31.20.1 172.31.20.20
ip dhcp pool TEST99
 network 172.31.99.0 255.255.255.0
 default-router 172.31.99.1
exit
ip dhcp pool TEST10
 network 172.31.10.0 255.255.255.0
 default-router 172.31.10.1
exit
ip dhcp pool TEST20
 network 172.31.20.0 255.255.255.0
 default-router 172.31.20.1
exit
end
show interfaces trunk
show ip dhcp binding
```

The encapsulation-selection command is conditional as explained in B: skip it only if the instance is fixed to dot1q and inspection confirms that fact. Native VLAN 99 is a disposable bootstrap convention here, not a campus native-VLAN decision.

If D2 fails, use a separately verified D3 Server fallback, adding one Server. In this H fixture use Server `172.31.99.3/24`, gateway `.99.1`, with distinct pools for 99/10/20 and the correct gateways; relay 10/20 to `.99.3`. Management DHCP is directly attached. Remove competing switch pools first; set WLC DHCP-server fields to `.99.3` instead of the per-VLAN SVI addresses below. Record this six-device variant.

#### H1. Management access, discovery and one management WLAN

**WLC GUI:** **Config → Management** (or **INTERFACE → management**) sets `172.31.99.2/24`, gateway `172.31.99.1`. Admin PC uses **Desktop → Web Browser** to reach `http://172.31.99.2` for an initial setup screen if presented; use `https://172.31.99.2` when the model requires it after setup. Follow the actual device's setup/login behavior. Create disposable credentials when prompted; do not assume a guessed factory password or alter host/browser security settings to bypass a failure.

For the displayed setup fields use a lab system name, the same management addressing, **management VLAN identifier 0/untagged if that mode is exposed**, and physical port 1. Here the switch maps untagged management frames to native VLAN 99; the controller's untagged indicator is not a new campus user VLAN. If the controller instead requires tagged management VLAN 99, explicitly record that alternative: set the WLC-facing switch port's native VLAN to 1 using `switchport trunk native vlan 1`, retain allowed VLANs `10,20,99`, and keep the controller management interface tagged 99. Admin/AP access ports remain in VLAN 99. Do not mix tagged management 99 with native management 99. An absent control is a recorded model difference, not permission to assume its value.

Create a temporary WLAN `CAP-MGMT` bound to the management interface, WPA2 Personal/PSK with AES and F's lab key; enable/broadcast it. Depending on the model this is a setup wizard or browser **WLANs → Create New** workflow. Read back after Apply. Keep internal controller DHCP disabled/unconfigured when using the switch/Server DHCP path.

AP: inspect **Config → GigabitEthernet** for its DHCP address. On 3702i, use **Config → WLC → Primary Controller** address `172.31.99.2` if the control exists. Otherwise, first test discovery on this same management subnet. No routed discovery option is assumed. Wait for startup/convergence and inspect controller AP summary/list and AP state; confirm radio enabled and association to this controller.

Laptop: join `CAP-MGMT`, request DHCP and verify a management-subnet lease, association details, then ping admin PC `.99.10`.

**H1 pass:** AP management lease, registered AP state, enabled WLAN, client association and usable data path all demonstrated. **Blocked:** no access to controller UI, no lease or unresolved discovery must be distinguished from an incompatible pairing. Record failed stage and exact errors. **Limit:** H1 does not prove distinct client VLAN mapping, because management and client traffic share one test subnet.

#### H2. WLAN-to-VLAN forwarding and two-SSID separation

Retain the same five-device fixture; no extra wireless client is required because the Laptop can test SSIDs sequentially.

**Controller browser workflow, where modelled:** **Controller → Interfaces → New** creates `cap-v10`, VLAN 10. Open it and set port 1, IP `172.31.10.2`, mask `255.255.255.0`, gateway `172.31.10.1`, primary DHCP server `172.31.10.1` for the switch-pool variant; Apply. Create `cap-v20` similarly with VLAN 20, IP `172.31.20.2`, gateway/DHCP `172.31.20.1`. In the Server fallback use `.99.3` for both DHCP-server fields. These are controller interface addresses, not replacements for the client default gateways.

**WLANs → Create New**: create profile/SSID `CAP-10`, bind it to `cap-v10`, enable it and set WPA2 Personal/PSK, AES and F's lab key. Repeat for `CAP-20` bound to `cap-v20`. Set **General → Interface/Interface Group** and **Security → Layer 2** where those fields exist; exact simulated labels must be recorded. If an AP group is required, assign both WLANs and the AP to a supported group. Verify both are advertised by this same AP; merely having two profile records is insufficient.

1. Join `CAP-10`, clear/restart the client's DHCP acquisition and verify `172.31.10.0/24`, gateway `.10.1`, then ping `.10.1` and admin PC `.99.10` through the routed switch.
2. While CAP-10 is active, on the WLC-facing switch port temporarily allow only `20,99`. Verify CAP-10 data traffic fails while AP management/registration in 99 remains available. Restore `10,20,99` and verify recovery. A retained lease does not prove a new DHCP transaction or forwarding.
3. Join `CAP-20` and force a fresh DHCP transaction. Verify `172.31.20.0/24`, gateway `.20.1`, and usable traffic. Repeat targeted pruning by allowing only `10,99`, then restore.
4. Corroborate the path with DHCP bindings, operational trunk VLANs and Simulation PDU details where exposed. Do not count management addressing alone as VLAN mapping.

**H2 pass:** both role SSIDs on the chosen AP, correct respective client scopes/gateways, working traffic, selective client-VLAN pruning and recovery without losing management. **Fail/partial:** association works but mapping/forwarding fails, all traffic behaves as management VLAN, or the same AP cannot expose the required WLANs. Report H1 separately from H2; do not work around a tagging failure by flattening the lab and claiming mapping passed.

**Known limits:** WLC 2504/3504 UI, supported fields, discovery and DHCP proxy behavior can differ. Browser fields are proposed navigation based on documented controller concepts, not a guarantee that every pane is implemented. Model names do not prove CAPWAP, roaming or enterprise feature completeness. If a field or forwarding mode is absent, record PARTIAL/BLOCKED with evidence; do not invent a CLI command to compensate.

### I. IoT availability and connectivity

#### I1. Discover an IP-capable device

**GUI-only inventory first:** **End Devices → Home / Smart City / Industrial / Power Grid**, as available. Record exact visible labels. Open **Specifications**, **Physical**, and **Config** on a disposable candidate. Distinguish a networked Smart Thing with Ethernet/wireless from a sensor/actuator component with only analog/digital slots. The latter requires an MCU/SBC and is not directly an IP host. Do not assume a specific sensor is available merely because an old template exists.

**I1 pass:** record at least one actual IP-capable candidate and its interface/security/registration options. **Blocked/partial:** only non-IP components are found or the chosen device has no required networking controls; revise the IoT demonstration scope rather than assigning it a fictitious IP.

#### I2. Minimum wired registration fixture

**Devices/connections:** one 2960, one selected Ethernet-capable Thing, one Server, one admin PC. Connect them to switch Fa0/1, Fa0/2, Fa0/3 respectively and configure all three as access VLAN 50 using A's pattern. No router is needed. Static IPs: Thing `172.31.50.21/24`, Server `.50.2/24`, PC `.50.10/24`; gateways blank/unspecified for this same-LAN fixture.

**GUI:** Server **Services → IoT → On**. PC **Desktop → Web Browser → http://172.31.50.2**; use the registration page's **Sign up now** workflow to create a disposable account. Thing **Config → Settings → IoT Server / Remote Server**: enter `.50.2` and the lab account, then Connect/Register if shown. Do not program or install an application on the Thing.

Confirm the Server web page lists the correct Thing and exposes a supported status or control. Where a safe test state exists, exercise it and observe a corresponding update. Some Things do not expose ping; registration and actual state/service traffic can establish connectivity without inventing an ICMP response.

If only a wireless IP Thing is suitable, add one AP, attach its Ethernet to a VLAN 50 access port and set a temporary IoT SSID/security combination verified for that device. Use the same test subnet and Server. This five-device variant is preferable to adding a home gateway with hidden DHCP/NAT just to force connectivity. If static addressing is unavailable, use a clearly recorded DHCP extension with a valid service/gateway design instead of assuming the minimum static fixture is executable.

**Pass:** exact device/network type recorded, addressing/association valid, fresh registration succeeds and supported state traffic is observed. **Fail/inconclusive:** registration service/account/network failure not resolved; a static icon or a component's local sensor value alone is not IP connectivity evidence. **Limits:** modelled sensor behavior is not physical sensor accuracy, and IoT connectivity does not certify the final VLAN 50 ACL policy.

### J. Packet Simulation Mode and ICMP testing

**Minimum:** two PCs directly connected using automatic cable selection, `172.31.10.11/24` and `.12/24`, gateways blank. Alternatively reuse a known-good A/C fixture and record which one. No custom IOS configuration is needed for the two-PC fixture.

1. **Realtime → Command Prompt:** establish a baseline with `ping 172.31.10.12` and reverse direction. Record initial ARP behavior and subsequent replies; do not invent RTT values.
2. Select **Simulation** on the Realtime/Simulation bar. In event filters select **ARP** and **ICMP**. Filters affect display, not whether other protocols execute.
3. Use **Add Simple PDU** (envelope), click source then destination. Advance with **Capture/Forward** or **Auto Capture/Play**. Inspect event-list entries and the PDU's **OSI Model**, **Inbound PDU Details** and **Outbound PDU Details** where available.
4. Distinguish ARP resolution from ICMP echo request/reply. On C's routed fixture, additionally confirm the gateway path if desired; a same-LAN J result does not prove routing.
5. Negative control: ping unused `172.31.10.250` in this two-PC-only fixture. Expect no echo reply and ARP resolution failure/timeout as modelled; it is not a congestion-loss measurement.
6. Preserve observations before **Reset Simulation**. Do not treat replay of a captured event list as another independent trial.

**Pass:** controls operate, a generated ICMP request/reply and any required ARP exchanges can be inspected, and the unused destination does not return a false success. **Fail/blocked:** missing mode access or unexplained inability to observe/generate traffic after fixture checks. **Limits:** time is event-based; animation speed and host wall-clock duration are not network latency. Repeated pings are connectivity samples, not realistic WLAN throughput or production loss rates.

## 5. Cisco CLI commands and interpretation

All configuration blocks in Section 4 are **proposed disposable-lab commands**. None were executed to prepare this file. Do not apply the blocks to the final campus network or a different fixture without adapting ports/state.

| Check | Read-only command or GUI equivalent | What it can establish |
| --- | --- | --- |
| Model/interfaces | `show version`, `show ip interface brief`, `show interfaces status` where accepted | Actual simulated model/interface names and state; a simulated IOS version is not an imported real IOS image. |
| VLAN membership | `show vlan brief` | VLAN IDs and access membership, not all trunk-carried VLANs. |
| Trunk transport | `show interfaces trunk`, `show interfaces <port> switchport` | Operational trunk/encapsulation, native and allowed/forwarding VLANs; support and wording vary. |
| Routes/SVIs | `show ip route`, `show ip interface brief` | Connected/static route entries and SVI state, corroborated by traffic. |
| DHCP | `show ip dhcp pool`, `show ip dhcp binding`; client `ipconfig` | Pool/lease evidence when implemented; a displayed address without a new transaction may be cached. |
| ACL | `show access-lists`, `show ip interface Vlan10` | Rule ordering/attachment/direction, supplemented by positive and negative service tests. |
| Wireless/controller | Actual GUI AP/client/controller state and traced traffic | Association/registration and data path. Do not paste switch IOS into an AP/controller GUI model. |
| Packet path | Simulation event/PDU inspection | Modelled packet processing, not physical RF measurements. |

If a command is rejected, record the exact model, command, mode and error; inspect `?` at that level. A missing inspection command is not by itself proof that forwarding is unsupported. Configuration syntax acceptance alone is not a functional pass. No `write erase`, software update or security bypass is needed.

## 6. Expected test outcomes

The Actual/Status cells are deliberately unfilled except for NOT RUN. No example RTT, loss percentage, lease result or screenshot has been fabricated.

| Test | Expected behavior if the scoped capability works | Status |
| --- | --- | --- |
| A | Six IDs created; membership and same-VLAN/isolation/recovery controls behave as specified. | NOT RUN |
| B / per-model repeats | Operational tagged transport; VLAN pruning selectively breaks and restoration recovers traffic. | NOT RUN |
| C1 / 3560 and 3650 separately | Correct SVI/route state and bidirectional inter-VLAN forwarding after enabling routing. | NOT RUN |
| C2 / 3650 + 2911 | Routed transit and static return routing work; route removal/restoration changes end-to-end reachability. | NOT RUN |
| D1 / 2911 | Correct fresh client lease and reachable gateway. | NOT RUN |
| D2 / each multilayer model | Local DHCP behavior demonstrated independently from routing. | NOT RUN |
| D3 | Remote pool selected through relay; helper removal prevents fresh remote acquisition and restoration recovers it. | NOT RUN |
| E / selected model | HTTP allowed, Server ICMP denied, local gateway permitted, and ACL removal restores Server ICMP. | NOT RUN |
| F | AP controls persist with the specified SSID/security and a documented channel option. | NOT RUN |
| G | Genuine association and bridging; incorrect-key negative test recorded separately. | NOT RUN |
| H1 / each of four pairings | AP registers and management WLAN provides actual client connectivity. | NOT RUN |
| H2 / each relevant pairing | Separate role scopes/data paths and selective client-VLAN pruning demonstrated on the same AP. | NOT RUN |
| I1/I2 | Real IP Thing identified; network registration and supported service/state exchange succeed. | NOT RUN |
| J | ARP/ICMP events observable; valid target succeeds and known-unused target has no echo response. | NOT RUN |

## 7. GUI verification steps and evidence

These are navigation aids, not claims that every model exposes identical tabs. Use Section 4 for the full procedure and record differences from the suggested paths.

| Location | Use in this plan | Evidence to capture during later execution |
| --- | --- | --- |
| Help/About or macOS application About menu | Version preflight | Displayed simulator version/build, not installer filename. |
| Network Devices / End Devices palette and hover label | Inventory/model choice | Exact label and any suffix; preserve the distinction from role names. |
| Switch/Router → CLI | A–E/H | Input/parser errors, relevant show output, port labels and attachment state. |
| Switch → Config → VLAN Database / interface | A/B readback | VLAN IDs, role assignment and trunk mode; avoid mistaking access membership output for trunk state. |
| PC/Laptop/Server → Desktop → IP Configuration | A–J addressing | Active interface, static/DHCP mode, address, mask and gateway. |
| Server → Services → DHCP / HTTP / IoT | D/E/I | Actual enabled service and fields; distinguish a pool saved in UI from a successful transaction. |
| AP → Config → wireless interface | F/G | Actual channel/security choices and applied values. |
| Laptop → Physical; Desktop → PC Wireless | G/H | Installed radio, association/SSID details and credential-test outcome without exposing reusable credentials. |
| WLC → Config → Management; admin client → Web Browser | H | Management reachability, controller model, AP list, WLAN/dynamic-interface relationship and client state. |
| Thing → Specifications / Config → Settings | I | IP versus component classification, actual interface and registration method. |
| Simulation → filters / event list / PDU details | J and diagnostic traces | Protocol/packet direction, actual outcome and relevant drop reason, retaining initialization context. |

The tests may alter **simulated device** settings in future disposable labs. They do not require changing the installed Packet Tracer version, host security permissions or global application preferences. Screenshots/logs are to be collected during execution, not fabricated now. Do not save results over existing documentation or CSVs; agree evidence storage in the later execution task.

## 8. Pass/fail record template

Use a separate record per model/variant/pairing. This template is included in the requested document; no additional result file is created now.

| Field | Value to enter during execution |
| --- | --- |
| Test ID / variant / trial | |
| Date/time / operator / reviewer | |
| Packet Tracer version/build | |
| Exact device model(s) / port map / wireless module | |
| Fixture and temporary addressing actually used | |
| Prerequisites and initialization/warm-up | |
| Commands accepted / rejected / UI differences | |
| Positive test: method / actual outcome / evidence | |
| Negative control: method / actual outcome / evidence | |
| Recovery/reversal: actual outcome / evidence | |
| Expected criterion met? | |
| Status | NOT RUN |
| Root-cause checks / model limitations / unresolved issue | |
| Scope of capability demonstrated | |
| Implication for provisional device selection | |

Execution statuses:

- **PASS:** stated functional criteria and applicable controls met, with evidence.
- **FAIL:** the scoped requirement is not met in a correctly established fixture; retain diagnosis rather than asserting unsupported hardware from one failed attempt.
- **PARTIAL:** a clearly identified subset works, for example H1 passes but H2 does not. State exactly which subset.
- **BLOCKED / INCONCLUSIVE:** prerequisite, access, cabling, GUI, syntax, caching or discovery issue prevents a defensible verdict.
- **NOT RUN:** no execution evidence yet; the state of every exercise in this document.

A failed negative control matters: if both correct and incorrect credentials work, the security test is not passed merely because connectivity exists. A successful AP registration or a valid management lease cannot replace a failed data-VLAN test. Mark models as final only after required functional cases, compatibility and project-scale constraints have been reviewed.

## 9. Device compatibility risks

| Risk | Handling in this plan |
| --- | --- |
| GUI labels differ from catalog labels | Preserve the team inventory and record exact instantiated label/version; do not silently expand 2960 or WLC into an assumed variant. |
| Port numbering/media/power differs | Preflight discovers real interfaces; adapt blocks once and record the mapping. Check required simulated power/module state. |
| Fixed versus selectable dot1q | B treats encapsulation-selection rejection independently from trunk capability. |
| SVI autostate or stale fixture | C checks live VLAN members, state and clean configuration before concluding routing failure. |
| Local DHCP absent or modelled differently | Separate D1, D2 and D3; server/relay is an explicit tested alternative. |
| ACL syntax accepted but ineffective | E uses unfiltered, selective allow/deny and recovery controls; counters are not sufficient alone. |
| AP/adapter/security mismatch | F/G record real bands/modules/options; no assumption that every client supports every AP. |
| Controller discovery or VLAN transport limitations | H separates discovery, registration, association, DHCP and data-tagging stages, and tests all candidate pairs separately. |
| Untagged management convention leaks into final design | H's native 99/VLAN-0 indicator is labelled disposable and must be reconsidered in the final architecture. |
| UI field absent or model-specific | Record PARTIAL/BLOCKED; do not import real-device commands and claim the simulator implements them. |
| IoT component mistaken for network endpoint | I1 reads actual interfaces/specifications before assigning any IP. |
| Cached state masks failures | Explicitly restart DHCP/association and generate a fresh application request where necessary; retain initialization context. |
| Capabilities overgeneralized | A passing device/pairing does not certify another model, all six production policies, realistic RF, scale, QoS or redundant behavior. |
| Prior installation diagnostics | Retain earlier audit findings as history. If a repeatable startup/UI error blocks execution, record it; this plan authorizes no reinstall, re-signing or settings repair. |

The final campus gateway location remains a later architecture decision. Using a distribution candidate as a gateway in a disposable lab does not resolve the old core-routing wording or authorize documentation changes. AP counts, five-zone geometry and actual campus subnets remain outside this plan.

## 10. Recommended order of testing

1. **Preflight and A:** model/interface discovery, six VLAN IDs, access membership and Layer 2 controls.
2. **B:** 2960 pair first, then mixed 2960–3560 and 2960–3650 trunks.
3. **C1:** 3560, then 3650, with separate records; **C2** validates 3650/2911 routed/static functions.
4. **D1 and D2:** choose DHCP roles from evidence; **D3** verifies relay/server placement when required and provides a fallback for H.
5. **E:** prove selective routed policy before adding wireless complexity.
6. **J:** run the minimal ICMP fixture and learn event interpretation; reuse known-good wired tests for troubleshooting.
7. **F then G:** establish a standalone SSID/client baseline independently of controllers.
8. **H1 then H2:** start WLC 2504 + 3702i; repeat only after isolating failures, then evaluate the other controller/AP pairs independently.
9. **I1 then I2:** select a genuine IP Thing and prove registration/network service behavior.
10. **Review evidence:** resolve failed/partial cases, choose the verified models and service/gateway approach, then plan full three-tier integration. Do not infer the final campus is validated from these small labs.

The next authorized engineering action should be manual execution of these disposable exercises with evidence collection. No test was run and no topology was created to prepare this plan. The final baseline and optimized project files remain untouched.

### Technical sources and evidence boundary

Primary sources consulted for procedure design: the installed Packet Tracer help and its public counterparts for [switch controls](https://tutorials.ptnetacad.net/help/default/config_switches.htm), [AP/lightweight AP controls](https://tutorials.ptnetacad.net/help/default/config_others.htm), [WLC configuration](https://tutorials.ptnetacad.net/help/default/config_WLCs.htm), [server services](https://tutorials.ptnetacad.net/help/default/config_servers.htm), [PC utilities](https://tutorials.ptnetacad.net/help/default/config_PCs.htm), [IoT Things versus components and registration](https://tutorials.ptnetacad.net/help/default/iot_using_things.htm), and [Simulation Mode](https://tutorials.ptnetacad.net/help/default/mode_simulation.htm).

[Cisco controller interface documentation](https://www.cisco.com/c/en/us/td/docs/wireless/controller/8-5/olh/wlc-olh/contc.html) explains dynamic-interface fields and the untagged VLAN indicator; it describes real controller software and does not prove full Packet Tracer implementation. The original [Cal State LA Packet Tracer wireless lab](https://cs3.calstatela.edu/~egean/cs4471/lab-assignments/Cisco%20Packet%20Tracer%20Wireless%20Lab.pdf) provides primary educational precedent for 2504/3702i browser bootstrap and untagged management. Its older workflow is contextual evidence, not a guarantee for 9.0.1. Actual UI/model discrepancies are intentionally part of H's record.

Sources were reviewed on 3 November 2026. The detailed addresses, fixtures and commands here are proposed lab designs; neither references nor palette visibility are substituted for test results.
