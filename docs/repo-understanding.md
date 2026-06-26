# Repo Understanding

This repository is a work-in-progress learning roadmap for robot control. It is not currently a software package: there is no build system, package manifest, executable source tree, CI configuration, or test suite in the repo at the time this document was written.

## Current Artifact Inventory

- `README.md`: short public-facing project stub. It names the project, states that the roadmap is WIP, and contains TODO sections for motivation, audience, visualization, and usage.
- `robotics-control-roadmap.drawio`: editable diagrams.net / Draw.io source for a simple roadmap graph titled `Control For Robots!`.
- `images/Control_Map_ver5.png`: a large PNG image titled `The Map of Control Theory`. This image appears to be an external reference-style control theory map and does not match the current Draw.io roadmap source.
- `topics-and-references.md`: empty placeholder referenced by the README as the future complete reference list.
- `LICENSE`: GPL-3.0 license text.
- `docs/`: repo-facing documentation for future agents and contributors.

Only `README.md` and `LICENSE` are tracked in the initial commit. The current working tree also contains untracked roadmap artifacts and this `docs/` directory.

## Project Shape

The intended repository shape appears to be:

1. A conceptual roadmap for robot control.
2. A visual diagram showing topic progression and dependencies.
3. A companion reference list mapping topics to learning resources.

The project is currently closer to a scaffold than a complete roadmap. The README explicitly marks core sections as TODO, and the topic/reference file is empty.

## Roadmap Source Of Truth

Treat `robotics-control-roadmap.drawio` as the editable roadmap source unless the user says otherwise. It is plain XML compatible with diagrams.net.

The current Draw.io graph contains these topic nodes:

- `Control For Robots!`
- `State Estimation`
- `Linear Control`
- `Non-Linear Control`
- `Model Predictive Control`
- `Dynamic Programming`
- `Policy Iteration`
- `Value Iteration`
- `Reinforcement Learning`

Every topic node currently has three child rows named `Resource 1`, `Resource 2`, and `Resource 3`. These are placeholders, not real references.

The current directed relationships in the Draw.io graph are:

- `Control For Robots!` -> `State Estimation`
- `Control For Robots!` -> `Linear Control`
- `Control For Robots!` -> `Dynamic Programming`
- `Linear Control` -> `Non-Linear Control`
- `Non-Linear Control` -> `Model Predictive Control`
- `Dynamic Programming` -> `Policy Iteration`
- `Dynamic Programming` -> `Value Iteration`
- `Policy Iteration` -> `Reinforcement Learning`
- `Value Iteration` -> `Reinforcement Learning`

## PNG Caveat

`images/Control_Map_ver5.png` is a 5011 x 3878 PNG titled `The Map of Control Theory`, credited in-image to Brian Douglas / Engineering Media, August 2020. It has many more topics than the Draw.io file, including adaptive control, robust control, planning, system analysis, modeling and simulation, multi-agent control, and many state estimation subtopics.

Do not assume this PNG is generated from `robotics-control-roadmap.drawio`. The visible content and structure differ substantially. If the roadmap visualization should be derived from Draw.io, a new export needs to be generated from `robotics-control-roadmap.drawio`.

## Documentation Gaps

The repo does not yet define:

- The intended audience or prerequisite background.
- The exact scope boundary between robotics control, general control theory, estimation, planning, and reinforcement learning.
- A canonical topic taxonomy beyond the small Draw.io graph.
- Any real resource entries for the topic placeholders.
- A process for updating the Draw.io source and exported image together.
- Attribution/licensing details for the PNG image.
- Commands for validation, export, formatting, or link checking.

## Suggested Contribution Workflow

Because this repo has no automated validation, contributors should be explicit about manual checks.

When changing roadmap content:

1. Edit `robotics-control-roadmap.drawio` in diagrams.net or another compatible Draw.io editor.
2. Update `topics-and-references.md` with the same topic names and real resource entries.
3. Export a fresh image only if the repo intends to keep a rendered roadmap image in `images/`.
4. Verify that README links and file names still match the repo.
5. State manual validation performed, such as opening the Draw.io file, viewing the exported PNG, or checking Markdown rendering.

When adding references:

- Prefer stable, primary, or widely accepted educational sources.
- Keep topic names consistent between the diagram and `topics-and-references.md`.
- Do not replace placeholder rows with claims about prerequisites or sequence unless those relationships are also reflected in the graph.

## Agent Notes

- Be careful with the dirty working tree. At the time of this document, user changes include a modified `README.md`, untracked `robotics-control-roadmap.drawio`, untracked `topics-and-references.md`, untracked `images/`, and an editor lock/symlink named `.#README.md`.
- Do not delete or normalize untracked files unless explicitly asked.
- There are no tests to run. Validation is currently limited to file inspection and Markdown/XML sanity checks.
- If asked to “complete” the roadmap, clarify whether the user wants topic taxonomy, curated references, diagram editing, README content, or all of those.
