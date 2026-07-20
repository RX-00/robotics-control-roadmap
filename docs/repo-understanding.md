# Repository Understanding

This repository is a work-in-progress learning atlas for robot control. It is primarily a documentation and diagram project, with a small standard-library synchronizer used to derive rendered and textual artifacts from the editable Draw.io source.

## Project Goal

The roadmap is intended to help students, researchers, and practitioners answer three questions:

1. Which subjects are part of modern robot control?
2. Which topics are prerequisites for other topics?
3. Which learning resources should be used for each topic?

The organizing principle is conceptual prerequisite order, not historical chronology. The map supports multiple learning tracks rather than prescribing one strictly linear curriculum.

## Canonical Content

<!-- roadmap-canonical:start -->
The canonical Draw.io source contains 59 topic nodes across 9 content areas:

- 1. Mathematical and Computational Foundations
- 2. Robot Modeling
- 3A. Feedback and Control Theory
- 3B. State Estimation
- 3C. Motion Planning
- 3D. Optimal Control
- 4. Contact-Rich Robot and Whole-Body Control
- 5. Learning and Learning-Based Control
- 6. Safety and Real-World Deployment

The synchronized semantic graph contains 60 nodes when the central roadmap node is included, and 99 directed prerequisite edges:

- 53 within-track edges; and
- 46 cross-track or entry edges.

The graph is acyclic.
<!-- roadmap-canonical:end -->

## Visual Presentation

The default roadmap is a radial atlas:

- foundational material is placed near the center;
- coherent subject tracks radiate outward;
- solid colored arrows show within-track learning order;
- thick borders identify major checkpoints.

Cross-track connectors are omitted from the public atlas because they create excessive crossings. The exact cross-track edges are authored on a hidden **Detailed cross-domain prerequisites** layer in the Draw.io file and reproduced in the generated Mermaid graph.

## Artifact Inventory

- `README.md`: public-facing project explanation and embedded roadmap.
- `robotics-control-roadmap.drawio`: canonical editable source with visible and detailed prerequisite layers.
- `roadmap-prerequisites.mmd`: generated exact edge-level Mermaid prerequisite graph.
- `images/robotics-control-roadmap.svg`: generated scalable public rendering.
- `topics-and-references.md`: partially synchronized reference index; topic bodies remain human-authored.
- `scripts/sync_from_drawio.py`: standard-library parser, validator, and synchronizer.
- `tests/test_sync_from_drawio.py`: synchronization and preservation regression tests.
- `images/Control_Map_ver5.png`: external visual inspiration; it is not an export of this roadmap.
- `LICENSE`: GPL-3.0 license text.

## Synchronization and Validation

After editing the Draw.io source, synchronize downstream artifacts with:

```bash
python scripts/sync_from_drawio.py
```

Check that committed artifacts are current without writing files:

```bash
python scripts/sync_from_drawio.py --check
```

The synchronizer validates stable node IDs, layer roles, edge endpoints, section roots, duplicate edges, graph acyclicity, canvas bounds, node overlap, and SVG XML. It supports both compressed and uncompressed Draw.io pages, but never rewrites the Draw.io source. Contributors should additionally inspect the SVG after meaningful layout changes.

There is no package build or automated CI workflow at present.

## Contribution Guidance

When changing roadmap content:

1. Edit `robotics-control-roadmap.drawio` in diagrams.net.
2. Keep existing semantic IDs stable. New topics should use a custom `roadmapId` such as `F7`; new section hubs should use `hub-X`.
3. Put within-track arrows on the visible **Radial atlas** layer and entry or cross-track arrows on the hidden detail layer.
4. Run `python scripts/sync_from_drawio.py`.
5. Inspect the radial SVG for overlap, clipping, and confusing edge crossings.
6. Run the unit tests and synchronization check before committing.

When adding references, prefer stable, authoritative, and pedagogically strong sources. Do not add a reference merely to fill a section; topic-level curation is part of the roadmap's intended value.
