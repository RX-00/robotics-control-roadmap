# Repository Understanding

This repository is a work-in-progress learning atlas for robot control. It is primarily a documentation and diagram project, with a small standard-library generator used to keep the editable and rendered roadmap artifacts synchronized.

## Project Goal

The roadmap is intended to help students, researchers, and practitioners answer three questions:

1. Which subjects are part of modern robot control?
2. Which topics are prerequisites for other topics?
3. Which learning resources should be used for each topic?

The organizing principle is conceptual prerequisite order, not historical chronology. The map supports multiple learning tracks rather than prescribing one strictly linear curriculum.

## Canonical Content

The roadmap contains 59 topic nodes across nine content areas:

- mathematical and computational foundations;
- robot modeling;
- feedback and control theory;
- state estimation;
- motion planning;
- optimal control;
- contact-rich robot and whole-body control;
- learning and learning-based control;
- safety and real-world deployment.

The canonical semantic graph is [`roadmap-prerequisites.mmd`](../roadmap-prerequisites.mmd). It contains 60 semantic nodes when the central roadmap node is included, and 99 directed prerequisite edges:

- 53 within-track edges; and
- 46 cross-track or entry edges.

The graph is acyclic.

## Visual Presentation

The default roadmap is a radial atlas:

- foundational material is placed near the center;
- coherent subject tracks radiate outward;
- solid colored arrows show within-track learning order;
- thick borders identify major checkpoints; and
- faint dashed arcs summarize cross-track dependencies.

Rendering every edge-level cross-track prerequisite in the public atlas would create excessive crossings. The exact cross-track edges are therefore stored on a hidden **Detailed cross-domain prerequisites** layer in the Draw.io file. The public SVG uses a smaller set of domain-level bundled connectors.

## Artifact Inventory

- `README.md`: public-facing project explanation and embedded roadmap.
- `roadmap-prerequisites.mmd`: exact edge-level Mermaid prerequisite graph.
- `robotics-control-roadmap.drawio`: editable radial atlas with visible and detailed prerequisite layers.
- `images/robotics-control-roadmap.svg`: scalable public rendering generated from the same topic data.
- `topics-and-references.md`: reference skeleton containing a section for every topic node.
- `scripts/generate_roadmap.py`: standard-library generator for the Draw.io, SVG, and Mermaid artifacts.
- `images/Control_Map_ver5.png`: external visual inspiration; it is not an export of this roadmap.
- `LICENSE`: GPL-3.0 license text.

## Regeneration and Validation

Regenerate the synchronized artifacts with:

```bash
python scripts/generate_roadmap.py
```

The generator validates the node and edge inventory and verifies that the Draw.io and SVG outputs parse as XML. Contributors should additionally inspect the SVG visually and open the Draw.io file after meaningful layout changes.

There is no package build or automated CI workflow at present.

## Contribution Guidance

When changing roadmap content:

1. Update the topic or edge definitions in `scripts/generate_roadmap.py`.
2. Keep the corresponding headings in `topics-and-references.md` synchronized.
3. Run the generator.
4. Inspect the radial SVG for overlap, clipping, and confusing edge crossings.
5. Open the Draw.io file and verify both the default atlas and hidden detailed-prerequisite layer.
6. Update the README if the visual language or roadmap scope changed.

When adding references, prefer stable, authoritative, and pedagogically strong sources. Do not add a reference merely to fill a section; topic-level curation is part of the roadmap's intended value.
