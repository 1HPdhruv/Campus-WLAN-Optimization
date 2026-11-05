# Campus Scenario and Network Requirements Specification

**Project:** Campus WLAN Optimization Using Access Point Placement and Network Segmentation  
**Academic context:** Five-member Computer Networks capstone, SRM Institute of Science and Technology  
**Prepared:** 3 November 2026  
**Document status:** Proposed requirements specification for team review. Confirmed decisions below come from the Task 2 brief; proposed requirements and unresolved decisions have not been approved by producing this document.  
**Implementation status:** Requirements only; no topology, device configuration or performance result is established here.

## How to interpret this specification

| Label | Meaning |
| --- | --- |
| **C — Confirmed** | Explicit decision or requirement supplied in the Task 2 brief. |
| **P — Proposed** | Recommended assumption, policy, verification criterion or requirement requiring team approval before adoption. |
| **T — To be decided** | Parameter or design choice intentionally left open. |
| **V — Verified repository fact** | Observed artifact state; not evidence that the network has been implemented. |

Requirement IDs support later traceability to architecture, implementation, tests and academic chapters. The word **shall** describes the intended acceptance obligation once a proposed requirement is approved; it does not make a P item a confirmed decision. Proposed criteria are a reviewable starting point, not measured outcomes.

### Evidence and reference availability

The existing README, all six documentation Markdown files and all three results CSVs were read for this specification. The following source limitations apply:

| Source | Observed state and use |
| --- | --- |
| Task 2 project brief | Source of confirmed scope, floors, zones, user categories, VLAN proposal and initial three-tier architecture requirement. |
| [Architecture](architecture.md) | V: Names Core, Distribution and Access layers; no completed topology is provided. Redundancy and firewalls are mentioned but are not finalized scope. |
| [VLAN plan](vlan-plan.md) and [IP addressing](ip-addressing.md) | V: Contain an older VLAN mapping and incomplete implementation details. See Section 4 for the explicit discrepancy. |
| [Wireless plan](wireless-plan.md) | V: Zero-byte placeholder. |
| [Testing](testing.md) and [results narrative](results.md) | V: Draft outlines. The results narrative includes unsupported statements of successful improvement. |
| [Baseline CSV](../results/baseline.csv), [optimized CSV](../results/optimized.csv), [comparison CSV](../results/comparison.csv) | V: Populated numerical summaries without raw test provenance. They do not establish measured performance or acceptance targets. |
| `Campus WLAN Optimization.pptx` | Not found in the repository, surrounding `Desktop/CN` tree or available attachment tree during this review. Actual slide content and order could not be inspected. |
| `presentation/Campus_WLAN_Optimization.pptx` | V: Zero bytes; not a readable PowerPoint presentation. |
| `Computer Networks Course Case study project report.docx` | Not found in the same searched locations. Exact report formatting and preliminary-page requirements remain unverified. |
| Both existing `.pkt` files | V: Zero-byte placeholders, not working simulations. |

The six-chapter report structure and 12-slide reference description were supplied in Task 1. They remain planning context rather than independently inspected document requirements. No unavailable academic content has been reconstructed. Existing artifacts are preserved; this specification does not silently reconcile them.

## 1. Project scope

### 1.1 Confirmed scope

| ID | Status | Requirement |
| --- | --- | --- |
| SCP-01 | C | Model a hypothetical compact university campus with two floors and the five functional zones in Section 3. Do not represent it as a surveyed SRM campus. |
| SCP-02 | C | Use Cisco Packet Tracer for an entirely simulation-based project. Physical deployment and equipment purchasing are not required. |
| SCP-03 | C | Develop separate baseline and optimized Packet Tracer topologies. |
| SCP-04 | C | Investigate AP distribution, demand/capacity assumptions, channel allocation, network organization and segmentation. |
| SCP-05 | C | Include wired and wireless clients, the approved planning VLAN categories, DHCP, inter-VLAN routing and ACL-based restrictions. |
| SCP-06 | C | Use Core, Distribution and Access as the initial architecture requirement. Consider an Internet edge, router and the switching categories in Section 7. |
| SCP-07 | C | Compare the two networks using comparable representative populations and testing conditions. Do not assume or invent improvements. |

### 1.2 Scope boundaries

This task defines requirements only. Switch models, AP quantities, interface assignments, IP subnets, AP coordinates and commands are deferred. Any illustrative floor plan or population introduced later must be explicitly approved as a simulation assumption.

Detailed RF prediction, production security certification, actual ISP performance, real SRM population statistics and physical deployment claims are outside the confirmed scope. QoS, controller automation, redundancy and traffic distribution techniques remain optional proposals pending feasibility and academic need; their mention in older documents does not establish implementation.

## 2. Campus description

The campus is one hypothetical two-floor university environment. The ground floor contains classrooms, a computer laboratory and a common area/lobby. The first floor contains a library and a combined faculty/administration office zone. A zone is a functional planning area, not necessarily one room, one AP or one subnet.

**C:** The environment contains exactly these five named functional zones. The classroom zone may contain multiple classrooms, but the number is unspecified. The office zone includes two user roles without creating an additional functional zone.

**P:** Organize demand by zone, role, wired/wireless access, application and activity level. Assign VLAN membership by device purpose or approved role, not simply by floor. A role may appear in multiple zones; a zone may contain multiple roles.

**T:** Floor dimensions, room shapes, adjacency, vertical relationships, wall/floor construction, cable paths, equipment locations and spatial scale. No location in this document is an actual SRM AP location.

## 3. Floor-wise functional zones

Zone IDs below are proposed documentation identifiers. The floor and zone names are confirmed; demand interpretations are proposed and require review.

| Zone ID | Floor | Confirmed functional zone | Proposed demand interpretation, not population data | Parameters still required |
| --- | --- | --- | --- | --- |
| Z-G-CL | Ground | Classrooms | Student wireless learning traffic with faculty access where required; demand may vary by teaching activity. | Classroom count, representative clients, activity mix and test points. |
| Z-G-LAB | Ground | Computer laboratory | Predominantly wired learning clients, with wireless use only where included in the approved scenario. | Wired/wireless mix, service endpoints and client distribution. |
| Z-G-COM | Ground | Common area / lobby | Student and guest wireless use; candidate area for testing uneven demand. | Guest participation, workload and representative positions. |
| Z-F-LIB | First | Library | Student and faculty study access; candidate mixed application demand. | Client mix, service requirements and representative positions. |
| Z-F-OFF | First | Faculty and administration offices | Faculty and administration access with separate logical policies despite sharing a zone. | Role distribution, protected services and wired/wireless mix. |

IoT endpoint placement and management attachment are **T**. They must be assigned a documented purpose before locations or quantities are chosen. No zone is assumed to have a specific number of APs, users or devices.

## 4. User categories and VLAN planning proposal

### 4.1 Current planning basis

The following mapping is **C: the current approved planning proposal** from Task 2. It is the basis for subsequent requirements work, not a claim that VLANs have been configured.

| VLAN | Category | Intended meaning | Unresolved details |
| --- | --- | --- | --- |
| 10 | Students | Representative student endpoints. | Population, access method, services and subnet. |
| 20 | Faculty | Representative teaching/staff endpoints. | Population and permitted shared services. |
| 30 | Administration | Administrative endpoints and approved administrative services. | Protected destinations and access rules. |
| 40 | Guests | Visitor endpoints using restricted access. | Authentication, access duration and external-service policy. |
| 50 | IoT | Approved simulated non-user endpoints. | Device purpose, controller/service flows and locations. |
| 99 | Network Management | Infrastructure management addresses and authorized management access. | Management hosts, interfaces, protocols and reachability. |

Management devices are an infrastructure category, not a campus user population statistic. A switch may carry multiple VLANs while its management interface belongs to VLAN 99. This does not imply every VLAN requires a wireless SSID or that every AP can carry multiple SSIDs.

### 4.2 Recorded legacy inconsistency

| VLAN | Existing `vlan-plan.md` / `ip-addressing.md` | Current Task 2 proposal | Required future action |
| --- | --- | --- | --- |
| 1 | Default | No user category specified | Decide default/native VLAN handling; do not assign a new purpose implicitly. |
| 10 | Faculty | Students | Reconcile role labels and dependent artifacts. |
| 20 | Students | Faculty | Reconcile role labels and dependent artifacts. |
| 30 | Guest | Administration | Reconcile role labels and dependent artifacts. |
| 40 | Administration | Guests | Reconcile role labels and dependent artifacts. |
| 50 | Absent | IoT | Add to future design artifacts after approval of implementation details. |
| 99 | Absent | Network Management | Add to future design artifacts after approval of implementation details. |

**T — D-01:** Schedule a separate reconciliation of existing documentation and all future addressing, SSID, configuration and test references. The older files remain unchanged in this task. Where a conflict occurs during planning, explicitly reference the Task 2 mapping and log the discrepancy.

Client totals, active concurrency and allocation by role/zone remain **T**. Their future values must be labelled simulation assumptions, not actual university counts. The baseline shall retain role identities in its client inventory even if it deliberately uses less segmentation.

## 5. Functional requirements

| ID | Status | Requirement | Intended verification |
| --- | --- | --- | --- |
| FR-01 | C | Represent all five functional zones and both floors. | Compare the documented scenario with the logical and physical representations. |
| FR-02 | C | Include representative wired and wireless clients and all six network categories. | Review client inventory and role assignments. |
| FR-03 | C | Represent Core, Distribution and Access roles as the initial architecture. | Review labelled topology and device-role matrix; exact hardware count remains T. |
| FR-04 | C | Include an Internet-connectivity use case and router/edge function. | Review the selected upstream model and demonstrate the agreed service path. |
| FR-05 | C | Provide DHCP for applicable clients. | Verify leases, correct subnet, gateway and any approved service options. |
| FR-06 | C | Apply the Section 4 VLAN proposal in the optimized network. | Verify membership, transport and end-to-end role mapping. |
| FR-07 | C | Provide inter-VLAN routing for permitted communication. | Test approved source/destination pairs. |
| FR-08 | C | Restrict traffic using ACLs according to an approved policy. | Run positive and negative tests, not ping-only evidence. |
| FR-09 | C | Provide wireless association and a demand-based placement/channel plan in the optimized network. | Verify association and review the placement/channel rationale. |
| FR-10 | C | Maintain two separate topologies with comparable test populations and conditions. | Compare scenario manifests and test definitions. |
| FR-11 | P | Define one non-overlapping IP subnet per optimized VLAN, with documented gateway, infrastructure reservations and client allocation. | Review address calculations and verify representative clients. |
| FR-12 | P | Specify DHCP location and relay requirements consistently with routing and ACLs. | Test each applicable VLAN and required service exception. |
| FR-13 | P | Document SSID-to-role/VLAN mapping, wired port roles and management reachability. | Trace a representative flow from endpoint to destination. |
| FR-14 | P | Represent external access using a simulated upstream network/service, without depending on a live Internet connection. | Reach the agreed simulated destination; distinguish this from actual Internet access. |
| FR-15 | P | Save and reopen both `.pkt` artifacts, retaining reproducible device state. | Reopen in the agreed Packet Tracer version and rerun key checks. |
| FR-16 | P | Retain configuration evidence, test records and artifact/version identifiers for reported findings. | Trace a result to its originating run and saved topology. |

Router placement, routing protocol or static routing choice, gateway location, DHCP placement, DNS and NAT requirements are **T**. A simulated upstream service is a proposed implementation of the Internet use case; live ISP connectivity is not assumed.

## 6. Non-functional requirements

These are **P** unless explicitly marked otherwise. They express desired project quality without inventing service-level targets.

| ID | Requirement | Acceptance basis |
| --- | --- | --- |
| NFR-01 | Reproducibility: document version, device types, scenario parameters, initialization, workload and test procedure. | Another member can repeat the agreed tests using the saved artifacts. |
| NFR-02 | Fair comparison (**C**): use comparable representative populations and testing conditions. | Explain every difference between paired scenarios and its purpose. |
| NFR-03 | Evidence integrity: distinguish simulation observations, analytical estimates, targets and unsupported legacy entries. | Every reported number has a method and provenance, or an explicit non-measured label. |
| NFR-04 | Maintainability: use consistent role, zone, device, VLAN and test identifiers. | Architecture, addressing, tests and presentation can be cross-checked. |
| NFR-05 | Compatibility: use an agreed Packet Tracer version and verified feature/device combinations. | All members can open the artifacts and reproduce required behavior. |
| NFR-06 | Simulation practicality: size the demonstrator to available computers and simulator behavior. | Agreed scenarios complete without treating host slowdown as campus performance. |
| NFR-07 | Explainability: justify placement, segmentation and policy choices using requirements. | Each change has a rationale and a defined verification method. |
| NFR-08 | Scalability analysis: discuss logical growth separately from represented client count. | Estimates disclose assumptions and are not claimed as validated production capacity. |
| NFR-09 | Reliability and recovery: include only the recovery behavior the team agrees to test. | No availability percentage or redundancy claim without implemented evidence. |

Throughput, latency, coverage, availability and concurrent-user thresholds remain **T**. Success includes a valid experiment and correct policy behavior even if a numerical improvement is absent or not measurable in Packet Tracer.

## 7. Network equipment categories

Equipment categories are requirements considerations, not a bill of materials. Models, quantities and port counts remain **T**.

| Category | Required consideration | Design boundary |
| --- | --- | --- |
| Internet/upstream representation | A defined external service or upstream path for the Internet use case. | Simulated model proposed; real Internet dependency not established. |
| Router / edge function | Campus-to-upstream connectivity and any required edge routing. | Exact placement, routing and NAT decision deferred. |
| Core switching | Backbone role in the initial three-tier architecture. | Device capability, quantity and routed/switched interfaces deferred. |
| Distribution switching | Aggregate access connectivity and provide the selected distribution functions. | Policy and gateway placement must be decided explicitly. |
| Access switching | Attach wired clients and APs; carry the approved VLANs. | Port assignments, trunks, uplinks and PoE modelling deferred. |
| Wireless APs | Provide representative WLAN access with documented placement and channel rationale. | Quantity, model, radio settings and positions deferred. |
| Wireless controller, if needed | Possible means of implementing the chosen WLAN/VLAN capabilities. | Optional; no controller architecture has been selected. |
| Wired clients | Represent applicable roles, including laboratory/office use as approved. | Population and role distribution deferred. |
| Wireless clients | Represent applicable mobile/user roles and zone demand. | Population, radio capability and association method deferred. |
| IoT endpoints | Represent an approved non-user device purpose. | No specific sensor, actuator or device count selected. |
| Network/service endpoints | Support DHCP and any approved DNS, application or upstream test services. | A separate server device for each service is not assumed. |
| Management endpoint/interfaces | Enable authorized infrastructure administration. | Management station count, address assignments and protocols deferred. |

A role need not correspond to exactly one device. Combining Core and Distribution into a collapsed-core topology would change the confirmed initial architecture and requires explicit team approval; it must not be introduced silently. A dedicated firewall appliance is not mandatory under the present scope; ACL-based restrictions are required.

## 8. Baseline network requirements

The baseline is a deliberately inefficient **hypothetical simulation**, not a reconstruction of an observed SRM network.

| ID | Status | Requirement |
| --- | --- | --- |
| BL-01 | C | Model poorly distributed AP locations relative to the approved demand/test-point plan. |
| BL-02 | C | Model inadequate traffic segmentation, less effective organization and congestion-prone design assumptions. |
| BL-03 | C | Use the same campus scenario and comparable representative population/testing conditions as the optimized network. |
| BL-04 | P | Preserve role and zone identifiers even when roles share a baseline broadcast domain. A flat or partially segmented baseline is a choice requiring approval. |
| BL-05 | P | Provide intentional, documented limitations while keeping the network operational for its agreed permitted services. Avoid accidental cabling, addressing or DHCP faults masquerading as WLAN problems. |
| BL-06 | P | Retain the initial three-tier role structure in both networks for the primary comparison. Any topology simplification requires an explicit experimental exception. |
| BL-07 | P | Record AP positions, channels, segmentation, workload and uplink assumptions before measurements. Do not tune them after observing results to force a desired outcome. |
| BL-08 | P | Test baseline reachability, association, service access and policy exposure before optimization; record findings without preassigned failure rates. |

**T:** Exact AP placement deficiencies, baseline VLAN usage, channel arrangement, shared-link assumptions and access restrictions. Congestion-prone means an explicitly justified workload/resource relationship; congestion itself is not a measured fact until observed by a valid method.

## 9. Optimized network requirements

| ID | Status | Requirement |
| --- | --- | --- |
| OP-01 | C | Plan AP placement using approved zone demand and the agreed spatial model. |
| OP-02 | C | Provide an explicit channel plan rather than arbitrary channel assignments. |
| OP-03 | C | Segment the optimized network using VLANs 10, 20, 30, 40, 50 and 99 with the Section 4 role mapping. |
| OP-04 | C | Provide appropriate routing and ACL-based access policies. |
| OP-05 | C | Improve network organization while retaining comparable representative populations and test conditions. |
| OP-06 | P | Document access ports, uplinks, gateway locations, DHCP ownership and SSID/VLAN relationships before implementation. |
| OP-07 | P | Use equal AP quantities and comparable AP capabilities for the primary placement/channel experiment. If additional APs are approved, report that as a distinct resource change. |
| OP-08 | P | Hold shared upstream/service capacity constant in the primary comparison unless a separately justified experiment changes it. |
| OP-09 | P | Use intermediate variants where practical to distinguish placement/channel changes from segmentation/policy effects. Otherwise state that the combined experiment cannot isolate individual causes. |
| OP-10 | P | Consider QoS or traffic distribution only after verifying a concrete supported mechanism and an appropriate test. Do not equate EtherChannel with wireless client load balancing. |

No optimized throughput, latency, loss, coverage or user-capacity improvement is prescribed. Improved organization and correct segmentation can be demonstrated independently of quantitative WLAN speed claims. VLANs alone do not prove improved radio coverage or reduced RF interference.

## 10. Network security requirements

**C:** The optimized network requires segmentation, inter-VLAN routing and ACL-based access restrictions. The following detailed policy is **P**, pending approval of destinations, protocols, direction and service exceptions.

| ID | Source category | Proposed access intent | Required evidence after approval |
| --- | --- | --- | --- |
| SEC-01 | Students | Permit approved learning/shared services and simulated external access; deny direct access to administration endpoints and infrastructure management. | Approved application succeeds; protected destination is denied. |
| SEC-02 | Faculty | Permit approved teaching/shared services and simulated external access; deny administration and management access unless specifically authorized. | Role-specific allow and deny tests. |
| SEC-03 | Administration | Permit approved administrative/shared services; no automatic authority to manage infrastructure. | Administrative service succeeds; unauthorized management is denied. |
| SEC-04 | Guests | Permit approved bootstrap services and simulated external access; deny other internal destinations except explicit service exceptions. | External service succeeds; internal roles/management remain inaccessible. |
| SEC-05 | IoT | Permit only approved controller/service and necessary bootstrap traffic; deny general user and management access. | Required device flow succeeds; unrelated destination is denied. |
| SEC-06 | Network Management | Permit infrastructure administration only from explicitly authorized management sources. | Authorized management succeeds; unauthorized sources fail. |
| SEC-07 | All applicable roles | Preserve necessary DHCP, DNS and return traffic according to the final service placement. | Lease/name-resolution and application tests work with ACLs enabled. |
| SEC-08 | Infrastructure | Restrict trunks to required VLANs; document native/default VLAN use and unused-port handling. | Configuration review and representative segmentation tests. |
| SEC-09 | Wireless access | Use an approved supported authentication/encryption method and documented role mapping. | Authorized association succeeds and an invalid-credential test fails where supported. |
| SEC-10 | Management | Prefer supported encrypted management protocols and use laboratory-only credentials. | Demonstrate the approved protocol without publishing reusable secrets. |

The final policy matrix must identify source, destination, protocol/port, direction, action, enforcement point and test ID. An ICMP denial alone does not establish that a protected application is inaccessible. Same-VLAN client isolation, guest-to-guest blocking, stateful inspection and enterprise authentication are **T**, not implied by inter-VLAN ACLs.

Baseline security limitations must be explicit and contained within the simulated environment. Baseline and optimized networks can have deliberately different policy outcomes; performance comparisons must use flows allowed in both, while security improvements are evaluated separately.

## 11. Performance measurement requirements

### 11.1 Evidence classification

**C:** Do not invent improvements. **P:** Every reported item shall carry one of these labels:

- **Observed simulation result:** Recorded in a named run using a documented simulator method.
- **Analytical estimate:** Calculated from explicit assumptions and a stated formula/model.
- **Proposed target:** A desired outcome requiring approval, not an observation.
- **Unverified legacy entry:** Existing data without adequate provenance.
- **Not measurable / not assessed:** No defensible method was available; never substitute zero.

Existing CSV entries remain unverified legacy entries. They shall not determine test parameters or acceptance thresholds and shall not be relabelled measured without supporting evidence. Claims in the existing results narrative do not establish an experiment.

### 11.2 Candidate measurements and operational definitions

All methods below are **P**; numerical workloads, thresholds and sample sizes are **T**.

| ID | Measure | Proposed operational definition | Reporting boundary |
| --- | --- | --- | --- |
| MEAS-01 | Functional reachability | Success/failure of named endpoint/service tests under the approved policy. | Separate intended ACL denials from operational failures. |
| MEAS-02 | DHCP correctness | Correct subnet, gateway and agreed options for eligible clients. | A lease proves configuration behavior, not WLAN capacity. |
| MEAS-03 | Packet delivery/loss | Application/test PDUs not delivered divided by PDUs sent, over a defined window with an explicit delivery deadline. | State protocol and warm-up; avoid treating every intermediate event as a new application packet. Report policy drops separately. |
| MEAS-04 | Latency | Defined RTT or one-way delay for named flows using supported simulator observations. | Never mix RTT and one-way delay or use animation playback/wall-clock duration as link latency. |
| MEAS-05 | Throughput/goodput | Delivered bits or application payload bits divided by the stated simulation interval, only if reliably observable. | Define direction, aggregate/per-client scope and payload accounting. A configured link rate is not measured throughput. |
| MEAS-06 | Sampled coverage proxy | Successful qualifying wireless test points divided by all predefined test points in the same approved spatial model. | Report a sampled model result, not real RF area coverage. Coordinates, service criterion and sample distribution must be fixed. |
| MEAS-07 | Area coverage estimate, if used | Estimated union of modelled qualifying coverage within the defined floor boundary divided by that floor area. | Requires approved dimensions, scale and assumptions. Do not sum overlapping circles or substitute sampled-point percentage for area percentage. |
| MEAS-08 | Association / connection time | Interval between a specified trigger and a specified endpoint state, separating association from DHCP/application readiness. | Use only if those events and timestamps can be observed reliably. |
| MEAS-09 | Represented concurrency | Number of represented clients simultaneously generating the defined workload and satisfying the approved criterion. | Separate configured, associated, active and successful clients. Do not extrapolate to real campus capacity. |
| MEAS-10 | Link utilization | Observed or analytically estimated traffic relative to a named link capacity and time window. | Label estimates; state direction and workload. Lower utilization alone does not prove better service. |

Jitter, roaming and QoS effects are optional **T** measures. They require definitions and simulator feasibility checks before inclusion.

### 11.3 Paired-test controls and records

**P:** Each baseline/optimized test pair shall record:

1. Run/test ID, date, operator, Packet Tracer version, saved topology identifier and scenario variant.
2. Client identities, categories, zones and positions, including selected AP associations when relevant.
3. Source/destination, protocol, packet/payload size, offered rate, duration, direction and activity schedule.
4. Initialization, ARP/DHCP/convergence warm-up and whether the test is cold-start or steady-state.
5. AP/channel/resource changes under test, alongside all unchanged controls.
6. Expected policy outcome, observed outcome, raw observations, calculation method and evidence path.
7. Independent trial count and variability where measurable; replaying one captured animation is not a new trial.

Keep client population, workload, service endpoints, spatial model and test points comparable. If capacity is tested at multiple population levels, compare baseline and optimized networks at each common level rather than comparing a low-load baseline with a high-load optimized run. Trial counts, sampling windows and acceptance criteria require approval before collection.

Use `(optimized - baseline) / baseline × 100` for signed relative change where the denominator is nonzero. Clearly identify lower-is-better metrics. For percentage-valued metrics, distinguish percentage-point change from relative percent change. Report undefined comparisons explicitly.

## 12. Simulation limitations

| Limitation | Required interpretation |
| --- | --- |
| Simplified wireless geometry | Packet Tracer documents distance/range-based association in Physical Workspace. It does not establish a calibrated model of the hypothetical building's walls, floors, multipath or real RF coverage. Spatial assumptions must be disclosed. [Cisco distance model](https://tutorials.ptnetacad.net/help/default/workspace_physical_distanceMeasurements.htm) |
| Event-driven timing | Simulation Mode records events on simulator time. Playback speed and host execution duration are not network latency measurements. [Cisco Simulation Mode](https://tutorials.ptnetacad.net/help/default/mode_simulation.htm) |
| Device/version dependence | WLAN-to-VLAN and controller behavior depend on the selected supported arrangement. Documentation of WLC capabilities does not prove a particular AP/controller combination works in the team's version. Verify before selecting it. [Cisco WLC configuration](https://tutorials.ptnetacad.net/help/default/config_WLCs.htm) |
| QoS and scaling limits | Cisco's FAQ identifies inaccurate QoS drop-rate numbers and wireless association/scaling limitations. Verify behavior in the chosen version; do not treat simulator limits as real AP limits. [Cisco FAQ](https://tutorials.ptnetacad.net/help/default/faqTroubleShoot.htm) |
| Channel and interference modelling | Configuring channels and observing associations can demonstrate a plan. Any claimed interference reduction needs a defined supported observation or an explicitly analytical model. |
| Represented population | A practical demonstrator represents roles and workloads; it does not validate production-scale simultaneous users merely by adding icons. |
| External services | A simulated upstream destination demonstrates a designed path, not actual Internet performance or an ISP service-level agreement. |
| Security depth | VLAN/ACL tests demonstrate the selected policy behavior, not comprehensive security assurance or stateful firewall operation. |
| Artifact creation | Text configuration drafts are not valid Packet Tracer files. Building, saving and reopening valid `.pkt` artifacts requires a verified Packet Tracer workflow. |

Sources were consulted on 3 November 2026. They are feasibility references, not substitutes for the missing academic PPT/report. Physical validation is not required; if a claim cannot be supported in the simulator, narrow the claim or present a labelled analytical estimate.

## 13. Assumptions

### 13.1 Confirmed scenario premises

The campus is hypothetical and compact, has two floors and five specified zones, uses the six-category VLAN planning proposal, begins with a three-tier architecture requirement and is evaluated through two Packet Tracer networks. These are **C**, not new assumptions needing reapproval.

### 13.2 Proposed assumptions requiring approval

| ID | Proposed assumption | Why approval is needed | Related decision |
| --- | --- | --- | --- |
| A-01 | Use a manageable representative client set with every role covered by the test inventory. | Actual simulated totals and zone/activity allocation affect addressing and workload. | D-03 |
| A-02 | Use the qualitative zone-demand interpretations in Section 3. | Wired/wireless mix and role placement were not supplied. | D-03 |
| A-03 | Use a simulated upstream service for the Internet use case. | Defines the edge test boundary. | D-08 |
| A-04 | Use a flat or partially segmented baseline while preserving endpoint role identities. | Determines the intended baseline deficiency and addressing. | D-09 |
| A-05 | Hold AP quantities/capabilities and shared service capacity constant for the primary comparison. | Separates placement/organization effects from added resources. | D-10 |
| A-06 | Adopt the Section 10 access-policy intents, subject to explicit service exceptions. | The brief requires restrictions but does not define permissions. | D-06 |
| A-07 | Use an approved illustrative spatial model and fixed test points for coverage demonstrations. | Dimensions and positions have not been provided. | D-04 |
| A-08 | Use one non-overlapping subnet per optimized VLAN, with DHCP for applicable clients and reserved infrastructure addresses. | Address families, sizing and service placement remain open. | D-07 |
| A-09 | Use repeated independent trials and intermediate optimization variants where feasible. | Test effort and valid observable metrics depend on simulator capability. | D-11 |

No client count, AP count, floor dimension, location coordinate, PHY rate or performance threshold is assumed numerically in this specification.

## 14. Constraints

| ID | Constraint | Status/source |
| --- | --- | --- |
| CON-01 | Simulation-based academic work; no mandatory purchase or physical deployment. | C — Task 2 scope. |
| CON-02 | Five-member project team. | C — Project brief. |
| CON-03 | Consider Core, Distribution and Access initially; do not silently collapse layers. | C — Task 2 architecture requirement. |
| CON-04 | Use the current VLAN proposal in planning while recording the conflicting legacy mapping. | C — Task 2 instructions. |
| CON-05 | No invented real SRM dimensions, populations, AP locations or measured performance. Label future hypothetical quantities as simulation assumptions. | C — Task 2 restrictions. |
| CON-06 | This task creates exactly `documentation/scenario-requirements.md`; it does not alter existing files, implement networks, generate configurations or create commits. | C — Task 2 deliverable boundary. |
| CON-07 | Primary academic references are presently unavailable or empty. | V — Repository/reference inspection. |
| CON-08 | Existing simulations and presentation are empty; existing CSVs lack raw measurement provenance. | V — Repository inspection. |
| CON-09 | Selected features must work in the team's agreed Packet Tracer environment and available computing resources. | P — Engineering feasibility constraint. |
| CON-10 | Delivery date, detailed rubric, report formatting and team availability are unspecified. | T — Must be obtained before schedule and submission acceptance are finalized. |

## 15. Unresolved decisions and next engineering task

### 15.1 Decision register

Suggested owners identify accountability, not named assignments. M1: lead/architecture; M2: baseline; M3: optimized/VLAN; M4: wireless/testing; M5: documentation/results. All decisions below remain open.

| ID | Decision required | Suggested owner | Resolve before |
| --- | --- | --- | --- |
| D-01 | Reconcile legacy VLAN labels and define default/native VLAN handling. Current Task 2 role mapping itself is already the planning basis. | M1 + M3 + M5 | Updating dependent documentation or configuration. |
| D-02 | Agree Packet Tracer version and verify required AP/controller, VLAN, DHCP, routing, ACL and optional QoS capabilities. | M1 + M3 + M4 | Selecting device models and WLAN architecture. |
| D-03 | Approve represented client totals, roles by zone, wired/wireless mix, activity and concurrency. | M1 + M2 + M4 | Subnet sizing and traffic plan. |
| D-04 | Approve illustrative dimensions/scale, adjacency, obstacles, test points and treatment of inter-floor coverage. | M1 + M4 | AP placement and coverage calculations. |
| D-05 | Define Core/Distribution/Access responsibilities, gateway placement, edge attachment, routed/switched boundaries and any redundancy. | M1 + M3 | Final architecture and interface design. |
| D-06 | Approve service destinations, protocols, ACL policy, authentication and management access. | M1 + M3 | Security design and acceptance tests. |
| D-07 | Select addressing family/scope, subnet sizes, DHCP location, reservations, DNS and relay requirements. | M1 + M3 | Addressing plan and implementation. |
| D-08 | Approve simulated upstream/service model and determine whether NAT or DNS is needed. | M1 + M2 + M3 | Edge design and external-service tests. |
| D-09 | Define the baseline's intended AP, segmentation, channel and organization deficiencies. | M1 + M2 + M4 | Baseline implementation and predeclared tests. |
| D-10 | Select AP count/capabilities, SSIDs, controller need, channels/bands and resource-change controls. | M1 + M3 + M4 | Final equipment and wireless plans. |
| D-11 | Approve measurable metrics, workload levels, trial counts, thresholds, warm-up and analysis methods. | M4 + M2 + M5 | Measurement collection. |
| D-12 | Decide whether QoS, traffic distribution, roaming, redundancy or further security features are required or deferred. | M1 + M3 + M4 | Committing to additional scope. |
| D-13 | Obtain actual PPT/report template, rubric and deadline; verify chapter/slide and formatting requirements. | M5 + M1 | Academic structure and submission schedule. |
| D-14 | Establish origins of legacy CSV figures and authorize their later treatment as targets, historical entries or replaceable draft data. | M5 + M4 | Updating results or making numerical claims. |
| D-15 | Assign named owners/reviewers, binary-file editing ownership and a GitHub review/evidence workflow. | M1 + all members | Parallel implementation. |

### 15.2 Recommended next engineering task

**Prepare an architecture decision and simulation-feasibility package after team review of this specification.** Start with D-02 through D-08: confirm the simulator environment, approve client/spatial assumptions, settle three-tier responsibilities and access requirements, and define the upstream/service and addressing approach.

The next package should contain a labelled logical architecture, role/interface requirements, capability matrix, proposed addressing/service ownership and an approved experiment outline. Device models and AP quantities should be selected only after the relevant assumptions and capabilities are established. Any later hands-on capability test is a separate implementation activity; none is performed by this specification.

Use the following review gate before full topology implementation:

1. Confirm which P requirements and A assumptions are accepted, amended or deferred; identify reviewers and a decision date. Do not mark unresolved items approved by default.
2. Obtain or explicitly record the continued absence of the academic reference documents.
3. Resolve decisions necessary for the initial architecture; retain optional features as explicit deferred items.
4. Freeze an initial version of the role/zone inventory, baseline deficiencies and paired-test controls.
5. Authorize subsequent reconciliation of older documentation as a separate task, preserving the conflict history.

The later implementation sequence is baseline construction and validation, controlled optimized variants, paired evidence collection, analysis, then report and presentation completion. No performance improvement is promised by this requirements foundation.
