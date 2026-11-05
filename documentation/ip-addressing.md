# Implemented simulation addressing

All values are simulation allocations, not real SRM addresses.

| VLAN | Role | Simulation subnet | Distribution gateway |
| --- | --- | --- | --- |
| 10 | Students | 10.10.10.0/24 | 10.10.10.1 |
| 20 | Faculty | 10.10.20.0/24 | 10.10.20.1 |
| 30 | Administration | 10.10.30.0/24 | 10.10.30.1 |
| 40 | Guests | 10.10.40.0/24 | 10.10.40.1 |
| 50 | IoT | 10.10.50.0/24 | 10.10.50.1 |
| 99 | Network Management | 10.10.99.0/24 | 10.10.99.1 |

| Endpoint | Role / logical zone | Baseline IP | Optimized IP | Addressing |
| --- | --- | --- | --- | --- |
| PC0 | Students, Classrooms | 10.10.1.101 | 10.10.10.10 | Static |
| PC1 | Students, Computer laboratory | 10.10.1.21 | 10.10.10.21 | DHCP, observed |
| PC2 | IoT policy proxy, Computer laboratory | 10.10.1.150 | 10.10.50.10 | Static; PC-PT |
| PC3 | Faculty, Library | 10.10.1.22 | 10.10.20.21 | DHCP, observed |
| PC4 | Administration, Faculty/admin | 10.10.1.130 | 10.10.30.10 | Static |
| PC5 | Management, Faculty/admin | 10.10.1.199 | 10.10.99.10 | Static |
| Laptop0 | Students, Common area | 10.10.1.110 | 10.10.10.20 | Static; wireless |
| Laptop1 | Guests, Library | 10.10.1.140 | 10.10.40.20 | Static; wireless |
| PC6 | External test host | 203.0.113.10 | 203.0.113.10 | Static; simulated external network |

| Local interface | Remote device / interface | Optimized use |
| --- | --- | --- |
| 2911 Gi0/0 | 3650 Gi1/0/1 | 10.255.0.1 / .2, /30 |
| 3650 Gi1/0/2 | 3560 Fa0/1 | 10.255.0.5 / .6, /30 |
| 3560 Fa0/2 | Ground 2960 Fa0/1 | 802.1Q: 10,20,30,40,50,99; native 99 |
| 3560 Fa0/3 | First 2960 Fa0/1 | 802.1Q: 10,20,30,40,50,99; native 99 |
| 2911 Gi0/1 | PC6 FastEthernet0 | 203.0.113.1 / .10, /24 |
| Ground Fa0/2 | PC0 | Access VLAN 10 |
| Ground Fa0/3 | PC1 | Access VLAN 10 |
| Ground Fa0/4 | PC2 | Access VLAN 50 |
| Ground Fa0/5 | AP0 Port0 | Access VLAN 10 |
| Ground Fa0/6 | AP1 Port0 | Access VLAN 40 |
| First Fa0/2 | PC3 | Access VLAN 20 |
| First Fa0/3 | PC4 | Access VLAN 30 |
| First Fa0/4 | PC5 | Access VLAN 99 |

Campus endpoint masks are /24 and gateways are distribution .1. Access management addresses are 10.10.99.11 and .12. PC6 gateway is 203.0.113.1. See report/report-content.md for static routes and verified DHCP scope.
