# Implemented standalone WLAN

Both scenarios use two AP-PT devices, two Laptop-PT/WPC300N clients, STUDENT_WIFI and GUEST_WIFI, and WPA2-PSK/AES. The disposable lab key is CampusLab2026. Each AP bridges one untagged SSID onto one switch access VLAN; tagged multi-SSID operation is not claimed.

| AP | Ground switch port | Baseline | Optimized |
| --- | --- | --- | --- |
| AP0 / Student | Fa0/5 | VLAN 1, channel 1, clustered | VLAN 10, channel 1, Common-area side |
| AP1 / Guest | Fa0/6 | VLAN 1, channel 1, clustered | VLAN 40, channel 6, Library side |

Placement is illustrative on the logical canvas, without measured dimensions or RF gains. AP1 retains its Ground-switch uplink even though logically placed near the Library. Both Student-to-wired and Guest-to-external forwarding were actually tested. The historical controller VLAN 10 forwarding failure remains unresolved and unchanged; no WLC success is claimed. Faculty, Administration, IoT proxy and Management are wired representatives.
