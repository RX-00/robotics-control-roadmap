# Robotics Control Roadmap

A prerequisite-based learning atlas for robot control. This project connects the mathematical foundations, modeling tools, control methods, estimation techniques, planning algorithms, learning methods, and deployment practices needed to build real robotic systems.

The roadmap is a work in progress. Its structure is now established, but the accompanying learning resources still need to be curated.

## Audience

The roadmap is intended for advanced undergraduates, graduate students, researchers, and practitioners who want to:

- enter robotics or robot-control research;
- identify gaps in their background;
- understand how control, planning, estimation, and learning fit together; or
- plan a learning path without losing sight of its prerequisites.

It is a reference map with multiple valid tracks, not a single course syllabus. A newcomer should begin near the center, while an experienced reader can enter at the topic closest to their current background.

## Roadmap

[![Radial robot-control prerequisite atlas](images/robotics-control-roadmap.svg)](images/robotics-control-roadmap.svg)

[Open the full-size scalable roadmap](images/robotics-control-roadmap.svg)

The atlas uses the following visual language:

- topics near the center are more foundational;
- each colored spoke is a coherent learning track;
- solid arrows show recommended prerequisite order within a track;
- thick-bordered cards are major checkpoint topics.

Cross-track connectors are omitted from the radial atlas because they obscure the topic layout. The exact edge-level graph is preserved in [`roadmap-prerequisites.mmd`](roadmap-prerequisites.mmd). The editable [`robotics-control-roadmap.drawio`](robotics-control-roadmap.drawio) also contains a hidden **Detailed cross-domain prerequisites** layer that can be enabled in diagrams.net.

## How to Use the Roadmap

1. Start with the foundational topics you do not yet know.
2. Follow solid arrows outward within a learning track.
3. Use the cross-track prerequisite graph when moving between disciplines.
4. Treat thick-bordered topics as checkpoints rather than final destinations.
5. Consult [`topics-and-references.md`](topics-and-references.md) for topic-specific learning resources as they are added.

The order is intentionally based on conceptual prerequisites rather than the historical order in which the subjects were developed.

## Roadmap Contents

<!-- roadmap-contents:start -->
The current atlas contains 59 topic nodes organized into 9 content areas:

- 1. Mathematical and Computational Foundations
- 2. Robot Modeling
- 3A. Feedback and Control Theory
- 3B. State Estimation
- 3C. Motion Planning
- 3D. Optimal Control
- 4. Contact-Rich Robot and Whole-Body Control
- 5. Learning and Learning-Based Control
- 6. Safety and Real-World Deployment
<!-- roadmap-contents:end -->

## Editing and Synchronizing

[`robotics-control-roadmap.drawio`](robotics-control-roadmap.drawio) is the canonical roadmap source. Open it in diagrams.net to move, resize, relabel, or restyle topics and to edit prerequisite arrows. Use the visible **Radial atlas** layer for within-track arrows and the hidden **Detailed cross-domain prerequisites** layer for exact entry and cross-track edges.

After saving the Draw.io file, synchronize the SVG, Mermaid graph, roadmap counts, section lists, and topic headings:

```bash
python scripts/sync_from_drawio.py
```

Existing semantic IDs such as `F1`, `R6`, and `hub-R` must remain stable. For a newly created node whose diagrams.net cell ID is arbitrary, add a custom `roadmapId` property such as `F7` or `hub-X`. New edge IDs may remain arbitrary. Topic reference content beneath the synchronized headings in [`topics-and-references.md`](topics-and-references.md) is preserved by stable ID markers.

The synchronizer uses only the Python standard library and never rewrites the Draw.io source. Verify that committed artifacts are current with:

```bash
python scripts/sync_from_drawio.py --check
```

### PNG Export

Render the synchronized SVG as a PNG with an installed SVG renderer. The script uses `rsvg-convert`, Inkscape, or ImageMagick, in that order:

```bash
python scripts/svg_to_png.py images/robotics-control-roadmap.svg images/robotics-control-roadmap.png --width 3000
```

Omit the paths to use those same roadmap defaults. `--width` is optional and preserves the SVG aspect ratio.

## References

The reference index is maintained in [`topics-and-references.md`](topics-and-references.md). References have not yet been curated.

When adding resources, prefer stable and pedagogically strong material such as authoritative textbooks, university lectures, original papers for major methods, and well-maintained practical tutorials.

## Inspiration

This project was inspired by:

- [mathematics-roadmap](https://github.com/talalalrawajfeh/mathematics-roadmap) by Talal Alrawajfeh; and
- [The Map of Control Theory](https://engineeringmedia.com/maps) by Engineering Media.

The repository retains `images/Control_Map_ver5.png` as a visual design reference. It is not an export of this roadmap.

## TODOs / Next Steps

- Get rid of numbering that's no longer used from past drafts (as seen in stuff like 3C, 3D, etc.)
- Split up real-world deployment and safety as they're different popular topics these days
- Separate contact-rich control and whole-body control
- Eventually make whole thing into an interactivate webapp where you can easily zoom and parse, with popups for the references
