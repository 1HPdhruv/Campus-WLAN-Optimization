# Implemented VLAN plan

The current implementation uses the approved mapping below. Earlier conflicting mappings in the original repository (including swapped Students/Faculty roles) are superseded here; their byte-identical originals are retained in submission-evidence/references/original-project-documents. Earlier requirements and audit documents remain historical planning records.

| VLAN | Role | Simulation subnet | Distribution gateway |
| --- | --- | --- | --- |
| 10 | Students | 10.10.10.0/24 | 10.10.10.1 |
| 20 | Faculty | 10.10.20.0/24 | 10.10.20.1 |
| 30 | Administration | 10.10.30.0/24 | 10.10.30.1 |
| 40 | Guests | 10.10.40.0/24 | 10.10.40.1 |
| 50 | IoT | 10.10.50.0/24 | 10.10.50.1 |
| 99 | Network Management | 10.10.99.0/24 | 10.10.99.1 |

Baseline campus clients share VLAN 1; optimized clients use the role VLANs. Management VLAN 99 is also native on the two access trunks. It is not an unused black-hole native VLAN and must not be described as that security pattern.
