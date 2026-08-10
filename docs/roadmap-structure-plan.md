# Roadmap Structure Update Plan

## Goal

Complete the first three roadmap TODOs while keeping the project a static,
synchronized documentation and diagram repository. The interactive web app is
explicitly out of scope for this work.

The result will be an unnumbered 11-track radial atlas that distinguishes
Safety from Real-World Deployment and Whole-Body Control from Contact-Rich
Control. The existing Draw.io diagram remains the canonical source.

## Agreed Scope

In scope:

- Remove reader-visible legacy section numbering.
- Split the Safety and Real-World Deployment track into two peer tracks.
- Split the Contact-Rich Robot and Whole-Body Control track into two peer
  tracks.
- Preserve existing topic material and references; redistribute topics rather
  than add new ones.
- Update the synchronization code and all generated artifacts.
- Remove the three completed TODOs from `README.md`, leaving the interactive
  web-app TODO.

Out of scope:

- Curating new learning references.
- Adding, removing, or substantively rewriting topic content.
- Building an interactive viewer, zooming UI, or reference popups.

## Target Reader-Facing Track Order

The visible atlas, generated Mermaid graph, README, repository-understanding
document, and reference index will use this exact unnumbered order:

1. Mathematical and Computational Foundations
2. Robot Modeling
3. Feedback and Control Theory
4. State Estimation
5. Motion Planning
6. Optimal Control
7. Whole-Body Control
8. Contact-Rich Control
9. Learning and Learning-Based Control
10. Safety
11. Real-World Deployment

The order is a layout and documentation convention, not a prescribed linear
curriculum.

## Canonical Ordering Metadata

Visible titles must no longer encode ordering. Add a `roadmapOrder` custom
property to every Draw.io section hub, with values `1` through `11` matching
the target order above. Update the synchronizer to:

- read and validate this property as a unique positive integer for each hub;
- sort groups by it instead of parsing a number from the hub label; and
- fail clearly if a hub is missing an order or two hubs share one.

This makes ordering explicit in the canonical diagram and leaves labels free
of hidden legacy numbering. Existing stable semantic IDs remain machine-facing
only and do not appear in reader-facing labels.

## Track Restructuring

### Safety and Real-World Deployment

Keep the existing `D` semantic group for the **Safety** track. It retains the
following stable topic IDs and reference bodies:

| ID | Topic |
| --- | --- |
| `D1` | Constraints, saturation, and anti-windup |
| `D2` | Uncertainty, robustness, and risk |
| `D3` | CLFs, CBFs, reachability, and safety filters |
| `D6` | Verification, hardware-in-the-loop, and experiments |

Create a new `H` semantic group for **Real-World Deployment**. Move the three
existing topics below, changing IDs only because the current synchronizer
derives membership from the ID prefix:

| Current ID | New ID | Topic |
| --- | --- | --- |
| `D4` | `H1` | Real-time optimization, latency, and embedded control |
| `D5` | `H2` | Sim-to-real, domain randomization, and adaptation |
| `D7` | `H3` | Deployment-ready robot autonomy |

Migrate the corresponding `roadmap-topic` markers in
`topics-and-references.md` so their existing reference bodies move with the
renamed topics.

Use these prerequisites:

```text
D1, D2 -> D3 -> D6
H1, H2 -> D6
H1, H2 -> H3
D6 -> H3
```

The first chain is internal to Safety; `H1`/`H2` to `D6` and `D6` to `H3` are
cross-track detailed edges. This preserves the current dependency meaning:
deployment capabilities inform verification, and verified systems precede
deployment-ready autonomy.

### Whole-Body and Contact-Rich Control

Keep the existing `R` semantic group for **Whole-Body Control**. It retains
these stable topics and reference bodies:

| ID | Topic |
| --- | --- |
| `R1` | Joint-space tracking and actuator control |
| `R2` | Computed torque and inverse-dynamics control |
| `R3` | Task-space and operational-space control |
| `R4` | Redundancy resolution and null-space control |
| `R6` | Whole-body control and hierarchical QPs |

Create a new `I` semantic group for **Contact-Rich Control** (`I` denotes
interaction/contact control). Move these topics and migrate their preserved
reference bodies in the reference index:

| Current ID | New ID | Topic |
| --- | --- | --- |
| `R5` | `I1` | Force, impedance, and admittance control |
| `R7` | `I2` | Contact scheduling, grasping, and locomotion control |

Use these prerequisites:

```text
R1 -> R2 -> R3 -> R4 -> R6
I1 -> I2
R3 -> I1
I1 -> R6
R6 -> I2
```

`R3 -> I1`, `I1 -> R6`, and `R6 -> I2` are detailed cross-track edges. Keep
the existing modeling and optimal-control prerequisites, remapped to `I1` and
`I2` where they formerly targeted `R5` and `R7`.

## Diagram and Visual Design

Edit `robotics-control-roadmap.drawio` as the only source of semantic and
layout changes.

- Rename all nine existing hub labels to remove their numeric prefixes.
- Rename `hub-D` visibly to **Safety** and `hub-R` visibly to
  **Whole-Body Control**.
- Add visible hubs `hub-H` and `hub-I`, their topic nodes, and `roadmapOrder`
  properties.
- Move the renamed topic nodes into their new semantic groups and update their
  IDs / `roadmapId` properties as specified above.
- Rebalance the radial layout for 11 spokes. Keep Whole-Body Control adjacent
  to Contact-Rich Control, and Safety adjacent to Real-World Deployment.
- Give each split pair related but distinguishable colors; do not rely on color
  alone to communicate the distinction.
- Keep only within-track arrows on the visible **Radial atlas** layer. Put new
  or remapped cross-track prerequisites on the hidden **Detailed cross-domain
  prerequisites** layer.

## Synchronizer and Generated Content

Update `scripts/sync_from_drawio.py` for `roadmapOrder` and its validation.
The synchronization flow should continue to generate:

- `images/robotics-control-roadmap.svg`;
- `roadmap-prerequisites.mmd`;
- the Roadmap Contents block in `README.md`;
- the Canonical Content block in `docs/repo-understanding.md`; and
- synchronized group and topic headings in `topics-and-references.md`.

Adjust or extend unit tests to cover unnumbered, explicitly ordered hubs and
ensure reference-body preservation still works for the deliberate marker
migrations. The existing tests that verify synchronization and Draw.io edits
must continue to pass.

## Implementation Sequence

1. Add `roadmapOrder` support and validation in the synchronizer, with tests.
2. Update the Draw.io hubs, topic IDs, layers, and prerequisites according to
   this plan; preserve all remaining semantic IDs.
3. Migrate the five reference markers and their bodies: `D4 -> H1`,
   `D5 -> H2`, `D7 -> H3`, `R5 -> I1`, and `R7 -> I2`.
4. Run the synchronizer to regenerate the SVG, Mermaid graph, README,
   repository-understanding doc, and reference headings.
5. Remove the three completed structure TODOs from the README, retaining only
   the web-app TODO.
6. Run automated checks and inspect the rendered SVG before committing.

## Acceptance Criteria

- All 11 public hub titles are unnumbered and appear in the agreed order.
- The diagram contains distinct peer spokes for Safety / Real-World Deployment
  and Whole-Body / Contact-Rich Control, with each pair adjacent.
- Existing references remain attached to their intended topics, including the
  five migrated markers.
- The visible atlas contains no cross-track arrows; the Mermaid graph and
  hidden Draw.io layer contain the agreed detailed dependencies.
- `python scripts/sync_from_drawio.py --check` succeeds after synchronization.
- `python -m unittest discover -s tests` succeeds.
- Manual SVG inspection confirms readable labels, no clipping or overlaps, and
  no confusing visible-edge crossings.
- The README’s remaining TODO is only the future interactive web app.
