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
- faint dashed arcs summarize important dependencies between tracks; and
- thick-bordered cards are major checkpoint topics.

Displaying every cross-track edge at once would obscure the content. The exact edge-level graph is therefore preserved in [`roadmap-prerequisites.mmd`](roadmap-prerequisites.mmd). The editable [`robotics-control-roadmap.drawio`](robotics-control-roadmap.drawio) also contains a hidden **Detailed cross-domain prerequisites** layer that can be enabled in diagrams.net.

## How to Use the Roadmap

1. Start with the foundational topics you do not yet know.
2. Follow solid arrows outward within a learning track.
3. Use the cross-track prerequisite graph when moving between disciplines.
4. Treat thick-bordered topics as checkpoints rather than final destinations.
5. Consult [`topics-and-references.md`](topics-and-references.md) for topic-specific learning resources as they are added.

The order is intentionally based on conceptual prerequisites rather than the historical order in which the subjects were developed.

## Roadmap Contents

The current atlas contains 59 topic nodes organized into:

1. Mathematical and computational foundations
2. Robot modeling
3. Feedback and control theory
4. State estimation
5. Motion planning
6. Optimal control
7. Contact-rich robot and whole-body control
8. Learning and learning-based control
9. Safety and real-world deployment

## Editing and Regenerating

The editable Draw.io file, scalable SVG, and canonical Mermaid prerequisite graph are generated from one shared topic definition:

```bash
python scripts/generate_roadmap.py
```

The generator uses only the Python standard library. After changing the topic definitions or edges, regenerate the artifacts and inspect the SVG and Draw.io file before committing them.

## References

The reference index is maintained in [`topics-and-references.md`](topics-and-references.md). References have not yet been curated.

When adding resources, prefer stable and pedagogically strong material such as authoritative textbooks, university lectures, original papers for major methods, and well-maintained practical tutorials.

## Inspiration

This project was inspired by:

- [mathematics-roadmap](https://github.com/talalalrawajfeh/mathematics-roadmap) by Talal Alrawajfeh; and
- [The Map of Control Theory](https://engineeringmedia.com/maps) by Engineering Media.

The repository retains `images/Control_Map_ver5.png` as a visual design reference. It is not an export of this roadmap.

## Future Work

- Curate learning resources for every topic.
- Add topic summaries, prerequisites, and learning outcomes.
- Add interactive links or hover cards for books, lectures, and papers.
- Review the taxonomy against respected robotics and control textbook tables of contents.
- Gather feedback on topic scope and prerequisite edges from specialists in each track.
