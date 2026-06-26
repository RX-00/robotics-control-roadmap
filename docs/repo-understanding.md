# Repo Understanding

This repository is a work-in-progress learning roadmap for robot control. It is a documentation and diagram repository, not a software package. There is no build system, package manifest, executable source tree, CI configuration, or test suite.

## Artifact Inventory

- `README.md`: public-facing project stub with sections for audience, roadmap visualization, usage, references, and inspiration.
- `robotics-control-roadmap.drawio`: editable diagrams.net / Draw.io source for the robot control roadmap.
- `topics-and-references.md`: Markdown skeleton whose sections mirror the roadmap topic nodes. Each section currently has an empty `References:` block.
- `images/Control_Map_ver5.png`: 5011 x 3878 PNG titled `The Map of Control Theory`, credited in-image to Brian Douglas / Engineering Media, August 2020.
- `LICENSE`: GPL-3.0 license text.
- `.gitignore`: ignores Emacs lock, backup, and autosave files.
- `docs/repo-understanding.md`: this repo orientation document.

## Roadmap Diagram

`robotics-control-roadmap.drawio` is uncompressed XML compatible with diagrams.net. The diagram is named `Robot Control Roadmap`.

The diagram contains 43 vertices:

- One title vertex: `Robot Control Roadmap`.
- 27 topic vertices.
- 15 legend vertices.

The 27 topic vertices are:

- `Mathematical Foundations`
- `Signals, Systems & Optimization`
- `Robot Kinematics`
- `Robot Dynamics`
- `State-Space Modeling`
- `Simulation & System Identification`
- `Feedback Control Basics`
- `Stability & Lyapunov Analysis`
- `Controllability & Observability`
- `Linear Control`
- `Nonlinear Control`
- `Robust & Adaptive Control`
- `Optimal Control`
- `State Estimation`
- `Sensor Fusion & Localization`
- `Motion Planning`
- `Trajectory Generation`
- `Trajectory Optimization`
- `Model Predictive Control`
- `Dynamic Programming`
- `Value Iteration`
- `Policy Iteration`
- `Reinforcement Learning`
- `Learning-Based Control`
- `Force & Impedance Control`
- `Operational Space & Whole-Body Control`
- `Contact & Hybrid Systems`

The diagram contains 22 directed edges. All roadmap arrows are minimal in-group learning-order links between topics of the same color.

The roadmap's in-group chains are:

- Foundations: mathematical foundations feeds signals, systems, and optimization.
- Robot modeling and control: kinematics feeds dynamics, dynamics feeds state-space modeling and force/impedance control, state-space modeling feeds simulation/system identification, force/impedance control feeds operational-space/whole-body control, and operational-space/whole-body control feeds contact/hybrid systems.
- Feedback and control theory: feedback basics feeds stability analysis, stability feeds controllability/observability, controllability/observability feeds linear control, linear control feeds nonlinear control, nonlinear control feeds robust/adaptive control, and robust/adaptive control feeds optimal control.
- Estimation and localization: state estimation feeds sensor fusion/localization.
- Planning and optimization: motion planning feeds trajectory generation, trajectory generation feeds trajectory optimization, and trajectory optimization feeds model predictive control.
- Dynamic programming and learning: dynamic programming feeds value iteration and policy iteration, both feed reinforcement learning, and reinforcement learning feeds learning-based control.

## Topics File

`topics-and-references.md` mirrors the 27 roadmap topic vertices as second-level Markdown headings. It contains no actual references yet.

## PNG Relationship

`images/Control_Map_ver5.png` is not an export of `robotics-control-roadmap.drawio`. The PNG is a dense external control-theory map with many topics that are not present in the Draw.io roadmap.

## Validation State

The Draw.io file parses as XML. There are no automated project tests or documented validation commands for this repository.
