#!/usr/bin/env python3
"""Generate the editable and rendered robot-control roadmap.

The semantic source is a directed prerequisite graph.  The radial atlas keeps
all within-track prerequisite edges visible, while dense cross-track edges are
stored on a hidden Draw.io layer and summarized with a small set of bundled
connectors in the public SVG.  This keeps the default view readable without
discarding the underlying graph.
"""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
from math import cos, radians, sin
from pathlib import Path
from textwrap import wrap
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
DRAWIO_PATH = ROOT / "robotics-control-roadmap.drawio"
SVG_PATH = ROOT / "images" / "robotics-control-roadmap.svg"
MERMAID_PATH = ROOT / "roadmap-prerequisites.mmd"

CANVAS = 6800
CX = CY = CANVAS / 2
HUB_RADIUS = 820
TOPIC_BASE_RADIUS = 1360
TOPIC_STEP = 330
LANE_STEP = 300
TOPIC_WIDTH = 300
TOPIC_HEIGHT = 82
HUB_WIDTH = 320
HUB_HEIGHT = 102


@dataclass(frozen=True)
class Topic:
    id: str
    label: str
    depth: int
    lane: float = 0.0
    checkpoint: bool = False


@dataclass(frozen=True)
class Group:
    id: str
    title: str
    angle: float
    fill: str
    stroke: str
    topics: tuple[Topic, ...]
    edges: tuple[tuple[str, str], ...]


GROUPS = (
    Group(
        "F",
        "1. Foundations",
        -90,
        "#fff2cc",
        "#d6b656",
        (
            Topic("F1", "Linear algebra and geometry", 0, -0.55, True),
            Topic("F6", "Programming, algorithms, and real-time computing", 0, 0.55),
            Topic("F2", "Calculus and differential equations", 1, -0.55),
            Topic("F3", "Probability, statistics, and stochastic processes", 1, 0.55),
            Topic("F4", "Numerical methods and optimization", 2, -0.55),
            Topic("F5", "Signals, systems, and frequency response", 2, 0.55),
        ),
        (("F1", "F2"), ("F1", "F3"), ("F2", "F4"), ("F2", "F5")),
    ),
    Group(
        "M",
        "2. Robot Modeling",
        -50,
        "#d5e8d4",
        "#82b366",
        (
            Topic("M1", "Coordinate frames, SO(3), and SE(3)", 0, -0.8),
            Topic("M4", "Classical and analytical mechanics", 0, 0.0),
            Topic("M8", "Sensors, actuators, friction, and transmissions", 0, 0.8),
            Topic("M2", "Forward and inverse kinematics", 1, -0.65, True),
            Topic("M5", "Rigid-body and multibody dynamics", 1, 0.35, True),
            Topic("M3", "Jacobians, differential kinematics, and singularities", 2, -0.9),
            Topic("M6", "Constrained, contact, and hybrid dynamics", 2, 0.0),
            Topic("M7", "Continuous and discrete state-space models", 2, 0.9),
            Topic("M9", "Simulation, calibration, and system identification", 3, 0.55),
        ),
        (
            ("M1", "M2"),
            ("M2", "M3"),
            ("M4", "M5"),
            ("M5", "M6"),
            ("M5", "M7"),
            ("M7", "M9"),
            ("M8", "M9"),
        ),
    ),
    Group(
        "C",
        "3A. Feedback and Control",
        -10,
        "#dae8fc",
        "#6c8ebf",
        (
            Topic("C1", "Feedback, feedforward, and PID control", 0, -0.55, True),
            Topic("C4", "Controllability and observability", 0, 0.55),
            Topic("C2", "Transfer functions and frequency-domain control", 1, -0.55),
            Topic("C3", "Stability, Lyapunov theory, and passivity", 1, 0.55),
            Topic("C5", "Linear state-space control", 2, 0.0, True),
            Topic("C6", "Nonlinear and geometric control", 3, 0.0, True),
            Topic("C7", "Robust and adaptive control", 4, 0.0),
        ),
        (
            ("C1", "C2"),
            ("C1", "C3"),
            ("C2", "C5"),
            ("C3", "C5"),
            ("C4", "C5"),
            ("C5", "C6"),
            ("C6", "C7"),
        ),
    ),
    Group(
        "E",
        "3B. State Estimation",
        30,
        "#e1d5e7",
        "#9673a6",
        (
            Topic("E1", "Bayesian state estimation", 0, 0.0, True),
            Topic("E2", "Observers and Kalman filtering", 1),
            Topic("E3", "EKF, UKF, and particle filtering", 2),
            Topic("E4", "Smoothing and factor graphs", 3),
            Topic("E5", "Sensor fusion, localization, and SLAM", 4),
        ),
        (("E1", "E2"), ("E2", "E3"), ("E3", "E4"), ("E4", "E5")),
    ),
    Group(
        "P",
        "3C. Motion Planning",
        70,
        "#f8cecc",
        "#b85450",
        (
            Topic("P1", "Configuration spaces and collision checking", 0, 0.0),
            Topic("P2", "Graph search and sampling-based planning", 1, -0.55, True),
            Topic("P4", "Trajectory generation and time scaling", 1, 0.55),
            Topic("P3", "Kinodynamic and belief-space planning", 2, -0.55),
            Topic("P5", "Trajectory optimization", 3, 0.0, True),
        ),
        (
            ("P1", "P2"),
            ("P2", "P3"),
            ("P1", "P4"),
            ("P4", "P5"),
            ("P3", "P5"),
        ),
    ),
    Group(
        "O",
        "3D. Optimal Control",
        110,
        "#f5d6b3",
        "#c97b30",
        (
            Topic("O1", "Calculus of variations and Pontryagin principle", 0, -0.55),
            Topic("O2", "Dynamic programming and Hamilton-Jacobi theory", 0, 0.55),
            Topic("O3", "LQR, iLQR, and DDP", 1, 0.0),
            Topic("O4", "Constrained and stochastic optimal control", 2, 0.0),
            Topic("O5", "Linear, nonlinear, robust, and stochastic MPC", 3, 0.0, True),
        ),
        (("O1", "O3"), ("O2", "O3"), ("O3", "O4"), ("O4", "O5")),
    ),
    Group(
        "R",
        "4. Robot-Specific Control",
        150,
        "#d0e8e6",
        "#3f8f89",
        (
            Topic("R1", "Joint-space tracking and actuator control", 0),
            Topic("R2", "Computed torque and inverse-dynamics control", 1),
            Topic("R3", "Task-space and operational-space control", 2),
            Topic("R4", "Redundancy resolution and null-space control", 3, -0.55),
            Topic("R5", "Force, impedance, and admittance control", 3, 0.55),
            Topic("R6", "Whole-body control and hierarchical QPs", 4, 0.0, True),
            Topic("R7", "Contact scheduling, grasping, and locomotion control", 5),
        ),
        (
            ("R1", "R2"),
            ("R2", "R3"),
            ("R3", "R4"),
            ("R3", "R5"),
            ("R4", "R6"),
            ("R5", "R6"),
            ("R6", "R7"),
        ),
    ),
    Group(
        "L",
        "5. Learning-Based Control",
        190,
        "#ffe6cc",
        "#d79b00",
        (
            Topic("L1", "Supervised learning and function approximation", 0, -0.55),
            Topic("L2", "MDPs, POMDPs, and Bellman equations", 0, 0.55, True),
            Topic("L4", "Imitation and inverse reinforcement learning", 1, -0.8),
            Topic("L6", "Learned dynamics, representations, and residual models", 1, 0.0),
            Topic("L3", "Value iteration and policy iteration", 1, 0.8),
            Topic("L5", "Reinforcement learning", 2, 0.55, True),
            Topic("L7", "Model-based, model-free, and offline RL", 3, 0.25),
            Topic("L8", "Hybrid learning and model-based control", 4, 0.0),
        ),
        (
            ("L2", "L3"),
            ("L3", "L5"),
            ("L5", "L7"),
            ("L7", "L8"),
            ("L1", "L4"),
            ("L4", "L8"),
            ("L1", "L6"),
            ("L6", "L8"),
            ("L6", "L7"),
        ),
    ),
    Group(
        "D",
        "6. Safety and Deployment",
        230,
        "#e6e6e6",
        "#666666",
        (
            Topic("D1", "Constraints, saturation, and anti-windup", 0, -0.55),
            Topic("D2", "Uncertainty, robustness, and risk", 0, 0.55),
            Topic("D4", "Real-time optimization, latency, and embedded control", 1, -0.55),
            Topic("D5", "Sim-to-real, domain randomization, and adaptation", 1, 0.55),
            Topic("D3", "CLFs, CBFs, reachability, and safety filters", 2, 0.0),
            Topic("D6", "Verification, hardware-in-the-loop, and experiments", 3, 0.0),
            Topic("D7", "Deployment-ready robot autonomy", 4, 0.0, True),
        ),
        (
            ("D1", "D3"),
            ("D2", "D3"),
            ("D3", "D6"),
            ("D4", "D6"),
            ("D5", "D6"),
            ("D6", "D7"),
        ),
    ),
)


APPLICATIONS = (
    Topic("A1", "Manipulation and grasping", 0),
    Topic("A2", "Mobile robots and autonomous vehicles", 0),
    Topic("A3", "Aerial robotics", 0),
    Topic("A4", "Legged robots and humanoids", 0),
    Topic("A5", "Multi-robot and human-robot systems", 0),
)


# Exact entry edges from the accepted semantic draft.
ENTRY_EDGES = (
    ("START", "F1"),
    ("START", "F6"),
)


# Exact cross-domain prerequisite edges from the accepted semantic draft.
CROSS_EDGES = (
    ("F1", "M1"),
    ("F2", "M4"),
    ("F5", "M7"),
    ("F4", "M9"),
    ("F6", "M9"),
    ("M7", "C1"),
    ("M7", "C4"),
    ("F5", "C2"),
    ("F3", "E1"),
    ("M7", "E2"),
    ("C4", "E2"),
    ("M8", "E5"),
    ("M2", "P1"),
    ("M3", "P4"),
    ("M6", "P3"),
    ("E5", "P3"),
    ("F4", "P5"),
    ("F4", "O1"),
    ("M7", "O1"),
    ("M7", "O2"),
    ("C5", "O3"),
    ("P5", "O4"),
    ("E3", "O4"),
    ("C7", "O5"),
    ("M3", "R3"),
    ("M5", "R2"),
    ("M6", "R5"),
    ("C5", "R1"),
    ("O4", "R6"),
    ("O5", "R7"),
    ("E3", "R6"),
    ("F3", "L2"),
    ("F4", "L1"),
    ("F6", "L1"),
    ("O2", "L3"),
    ("M9", "L6"),
    ("O5", "L8"),
    ("R6", "L8"),
    ("C7", "D2"),
    ("O5", "D1"),
    ("O5", "D4"),
    ("M9", "D5"),
    ("L8", "D5"),
    ("R7", "D3"),
)


APPLICATION_EDGES = (
    ("D7", "A1"),
    ("D7", "A2"),
    ("D7", "A3"),
    ("D7", "A4"),
    ("D7", "A5"),
)


# Bundled domain-level connectors used only in the clean public atlas.
SUMMARY_EDGES = (
    ("F", "M"),
    ("M", "C"),
    ("M", "E"),
    ("M", "P"),
    ("M", "O"),
    ("C", "R"),
    ("E", "R"),
    ("P", "R"),
    ("O", "R"),
    ("O", "L"),
    ("R", "L"),
    ("R", "D"),
    ("L", "D"),
)


def polar(radius: float, angle_deg: float) -> tuple[float, float]:
    angle = radians(angle_deg)
    return CX + radius * cos(angle), CY + radius * sin(angle)


def topic_center(group: Group, topic: Topic) -> tuple[float, float]:
    angle = radians(group.angle)
    radius = TOPIC_BASE_RADIUS + topic.depth * TOPIC_STEP
    tangent = topic.lane * LANE_STEP
    return (
        CX + radius * cos(angle) - tangent * sin(angle),
        CY + radius * sin(angle) + tangent * cos(angle),
    )


def node_geometry() -> dict[str, tuple[float, float, float, float]]:
    geometry: dict[str, tuple[float, float, float, float]] = {
        "START": (CX - 245, CY - 245, 490, 490)
    }
    for group in GROUPS:
        hx, hy = polar(HUB_RADIUS, group.angle)
        geometry[f"hub-{group.id}"] = (
            hx - HUB_WIDTH / 2,
            hy - HUB_HEIGHT / 2,
            HUB_WIDTH,
            HUB_HEIGHT,
        )
        for topic in group.topics:
            x, y = topic_center(group, topic)
            geometry[topic.id] = (
                x - TOPIC_WIDTH / 2,
                y - TOPIC_HEIGHT / 2,
                TOPIC_WIDTH,
                TOPIC_HEIGHT,
            )

    ax, ay = polar(2800, -90)
    geometry["hub-A"] = (ax - HUB_WIDTH / 2, ay - HUB_HEIGHT / 2, HUB_WIDTH, HUB_HEIGHT)
    for topic, angle in zip(APPLICATIONS, (-145, -117.5, -90, -62.5, -35), strict=True):
        x, y = polar(3220, angle)
        geometry[topic.id] = (
            x - TOPIC_WIDTH / 2,
            y - TOPIC_HEIGHT / 2,
            TOPIC_WIDTH,
            TOPIC_HEIGHT,
        )
    return geometry


GEOMETRY = node_geometry()


def center(node_id: str) -> tuple[float, float]:
    x, y, width, height = GEOMETRY[node_id]
    return x + width / 2, y + height / 2


def boundary_points(source: str, target: str) -> tuple[float, float, float, float]:
    sx, sy = center(source)
    tx, ty = center(target)
    dx, dy = tx - sx, ty - sy

    def clipped(
        x: float, y: float, width: float, height: float, vx: float, vy: float
    ) -> tuple[float, float]:
        candidates = []
        if abs(vx) > 1e-9:
            candidates.append((width / 2) / abs(vx))
        if abs(vy) > 1e-9:
            candidates.append((height / 2) / abs(vy))
        scale = min(candidates)
        return x + scale * vx, y + scale * vy

    length = max((dx * dx + dy * dy) ** 0.5, 1.0)
    ux, uy = dx / length, dy / length
    _, _, sw, sh = GEOMETRY[source]
    _, _, tw, th = GEOMETRY[target]
    start = clipped(sx, sy, sw, sh, ux, uy)
    end = clipped(tx, ty, tw, th, -ux, -uy)
    return start[0], start[1], end[0], end[1]


def add_geometry(cell: ET.Element, node_id: str) -> None:
    x, y, width, height = GEOMETRY[node_id]
    ET.SubElement(
        cell,
        "mxGeometry",
        {
            "x": f"{x:.1f}",
            "y": f"{y:.1f}",
            "width": f"{width:.1f}",
            "height": f"{height:.1f}",
            "as": "geometry",
        },
    )


def drawio_edge(
    root: ET.Element,
    edge_id: str,
    source: str,
    target: str,
    parent: str,
    style: str,
    points: tuple[tuple[float, float], ...] = (),
) -> None:
    cell = ET.SubElement(
        root,
        "mxCell",
        {
            "id": edge_id,
            "edge": "1",
            "parent": parent,
            "source": source,
            "target": target,
            "style": style,
        },
    )
    geometry = ET.SubElement(cell, "mxGeometry", {"relative": "1", "as": "geometry"})
    if points:
        point_array = ET.SubElement(geometry, "Array", {"as": "points"})
        for x, y in points:
            ET.SubElement(point_array, "mxPoint", {"x": f"{x:.1f}", "y": f"{y:.1f}"})


def generate_drawio() -> None:
    mxfile = ET.Element(
        "mxfile",
        {"host": "Electron", "agent": "robotics-control-roadmap generator"},
    )
    diagram = ET.SubElement(mxfile, "diagram", {"id": "radial-roadmap", "name": "Radial Atlas"})
    model = ET.SubElement(
        diagram,
        "mxGraphModel",
        {
            "dx": "2400",
            "dy": "1800",
            "grid": "1",
            "gridSize": "10",
            "guides": "1",
            "tooltips": "1",
            "connect": "1",
            "arrows": "1",
            "fold": "1",
            "page": "1",
            "pageScale": "1",
            "pageWidth": str(CANVAS),
            "pageHeight": str(CANVAS),
            "background": "#fbfaf7",
            "math": "0",
            "shadow": "0",
        },
    )
    root = ET.SubElement(model, "root")
    ET.SubElement(root, "mxCell", {"id": "0"})
    ET.SubElement(root, "mxCell", {"id": "1", "value": "Radial atlas", "parent": "0"})
    ET.SubElement(
        root,
        "mxCell",
        {
            "id": "2",
            "value": "Detailed cross-domain prerequisites",
            "parent": "0",
            "visible": "0",
        },
    )

    for radius, opacity in ((820, 35), (1360, 24), (2020, 18), (2680, 14)):
        ring = ET.SubElement(
            root,
            "mxCell",
            {
                "id": f"ring-{radius}",
                "parent": "1",
                "vertex": "1",
                "connectable": "0",
                "style": (
                    "ellipse;whiteSpace=wrap;html=1;fillColor=none;"
                    f"strokeColor=#9aa0a6;strokeWidth=1;opacity={opacity};"
                    "movable=0;resizable=0;rotatable=0;"
                ),
            },
        )
        ET.SubElement(
            ring,
            "mxGeometry",
            {
                "x": f"{CX - radius:.1f}",
                "y": f"{CY - radius:.1f}",
                "width": f"{2 * radius:.1f}",
                "height": f"{2 * radius:.1f}",
                "as": "geometry",
            },
        )

    spoke_style = "edgeStyle=none;endArrow=none;strokeWidth=5;opacity=18;"
    for group in GROUPS:
        drawio_edge(root, f"spoke-{group.id}", "START", f"hub-{group.id}", "1", spoke_style)
    drawio_edge(root, "spoke-A", "START", "hub-A", "1", spoke_style)

    summary_style = (
        "edgeStyle=none;curved=1;rounded=1;dashed=1;dashPattern=8 8;"
        "strokeColor=#59636e;strokeWidth=2;opacity=24;endArrow=blockThin;endFill=1;"
    )
    for index, (source_group, target_group) in enumerate(SUMMARY_EDGES):
        source = next(group for group in GROUPS if group.id == source_group)
        target = next(group for group in GROUPS if group.id == target_group)
        middle_angle = (source.angle + target.angle) / 2
        control_radius = 1010 + 24 * (index % 5)
        point = polar(control_radius, middle_angle)
        drawio_edge(
            root,
            f"summary-{source_group}-{target_group}",
            f"hub-{source_group}",
            f"hub-{target_group}",
            "1",
            summary_style,
            (point,),
        )

    for group in GROUPS:
        incoming = {target for _, target in group.edges}
        roots = [topic.id for topic in group.topics if topic.id not in incoming]
        root_style = (
            "edgeStyle=none;curved=0;strokeWidth=2;opacity=55;"
            f"strokeColor={group.stroke};endArrow=blockThin;endFill=1;"
        )
        for topic_id in roots:
            drawio_edge(
                root,
                f"hub-edge-{group.id}-{topic_id}",
                f"hub-{group.id}",
                topic_id,
                "1",
                root_style,
            )
        internal_style = (
            "edgeStyle=none;curved=0;rounded=1;strokeWidth=2;opacity=72;"
            f"strokeColor={group.stroke};endArrow=blockThin;endFill=1;"
        )
        for source, target in group.edges:
            drawio_edge(
                root,
                f"edge-{source}-{target}",
                source,
                target,
                "1",
                internal_style,
            )

    drawio_edge(
        root,
        "bundle-deployment-apps",
        "D7",
        "hub-A",
        "1",
        "edgeStyle=none;curved=1;strokeColor=#666666;strokeWidth=2;opacity=55;endArrow=blockThin;endFill=1;",
        (polar(2960, -130), polar(2960, -105)),
    )
    for topic in APPLICATIONS:
        drawio_edge(
            root,
            f"hub-edge-A-{topic.id}",
            "hub-A",
            topic.id,
            "1",
            "edgeStyle=none;curved=1;strokeColor=#444444;strokeWidth=2;opacity=55;endArrow=blockThin;endFill=1;",
        )

    start = ET.SubElement(
        root,
        "mxCell",
        {
            "id": "START",
            "parent": "1",
            "vertex": "1",
            "value": (
                "<b>Robot Control Roadmap</b><br>"
                "<font style=\"font-size:16px\">Start near the center and follow each track outward</font><br>"
                "<font style=\"font-size:13px;color:#5f6368\">Solid arrows: within-track prerequisites<br>"
                "Dashed arcs: bundled cross-track dependencies</font>"
            ),
            "style": (
                "ellipse;whiteSpace=wrap;html=1;align=center;verticalAlign=middle;"
                "fontSize=28;fontStyle=1;fillColor=#ffffff;strokeColor=#202124;"
                "strokeWidth=4;shadow=1;spacing=18;"
            ),
        },
    )
    add_geometry(start, "START")

    for group in GROUPS:
        hub = ET.SubElement(
            root,
            "mxCell",
            {
                "id": f"hub-{group.id}",
                "parent": "1",
                "vertex": "1",
                "value": f"<b>{escape(group.title)}</b>",
                "style": (
                    "rounded=1;arcSize=28;whiteSpace=wrap;html=1;align=center;"
                    f"verticalAlign=middle;fontSize=18;fontStyle=1;fillColor={group.fill};"
                    f"strokeColor={group.stroke};strokeWidth=3;shadow=1;spacing=10;"
                ),
            },
        )
        add_geometry(hub, f"hub-{group.id}")
        for topic in group.topics:
            width = 3 if topic.checkpoint else 1.6
            cell = ET.SubElement(
                root,
                "mxCell",
                {
                    "id": topic.id,
                    "parent": "1",
                    "vertex": "1",
                    "value": escape(topic.label),
                    "tooltip": escape(topic.label),
                    "style": (
                        "rounded=1;arcSize=18;whiteSpace=wrap;html=1;align=center;"
                        f"verticalAlign=middle;fontSize=14;fillColor={group.fill};"
                        f"strokeColor={group.stroke};strokeWidth={width};shadow=1;spacing=8;"
                    ),
                },
            )
            add_geometry(cell, topic.id)

    app_hub = ET.SubElement(
        root,
        "mxCell",
        {
            "id": "hub-A",
            "parent": "1",
            "vertex": "1",
            "value": "<b>7. Specialization Tracks</b>",
            "style": (
                "rounded=1;arcSize=28;whiteSpace=wrap;html=1;align=center;"
                "verticalAlign=middle;fontSize=18;fontStyle=1;fillColor=#ffffff;"
                "strokeColor=#444444;strokeWidth=3;shadow=1;spacing=10;"
            ),
        },
    )
    add_geometry(app_hub, "hub-A")
    for topic in APPLICATIONS:
        cell = ET.SubElement(
            root,
            "mxCell",
            {
                "id": topic.id,
                "parent": "1",
                "vertex": "1",
                "value": escape(topic.label),
                "tooltip": escape(topic.label),
                "style": (
                    "rounded=1;arcSize=18;whiteSpace=wrap;html=1;align=center;"
                    "verticalAlign=middle;fontSize=14;fillColor=#ffffff;"
                    "strokeColor=#444444;strokeWidth=1.6;shadow=1;spacing=8;"
                ),
            },
        )
        add_geometry(cell, topic.id)

    detailed_style = (
        "edgeStyle=none;curved=1;dashed=1;dashPattern=6 6;strokeColor=#5f6368;"
        "strokeWidth=1.5;opacity=45;endArrow=blockThin;endFill=1;"
    )
    detailed_solid_style = (
        "edgeStyle=none;curved=1;strokeColor=#5f6368;strokeWidth=1.5;"
        "opacity=45;endArrow=blockThin;endFill=1;"
    )
    detailed_edges = (
        [(source, target, detailed_solid_style) for source, target in ENTRY_EDGES]
        + [(source, target, detailed_style) for source, target in CROSS_EDGES]
        + [(source, target, detailed_solid_style) for source, target in APPLICATION_EDGES]
    )
    for index, (source, target, style) in enumerate(detailed_edges):
        drawio_edge(
            root,
            f"detail-{index}-{source}-{target}",
            source,
            target,
            "2",
            style,
        )

    ET.indent(mxfile, space="  ")
    DRAWIO_PATH.write_text(ET.tostring(mxfile, encoding="unicode") + "\n", encoding="utf-8")


def svg_text_lines(label: str, max_chars: int, max_lines: int = 3) -> list[str]:
    lines = wrap(label, width=max_chars, break_long_words=False, break_on_hyphens=False)
    if len(lines) <= max_lines:
        return lines
    kept = lines[: max_lines - 1]
    remainder = " ".join(lines[max_lines - 1 :])
    if len(remainder) > max_chars:
        remainder = remainder[: max_chars - 1].rstrip() + "…"
    kept.append(remainder)
    return kept


def svg_card(
    node_id: str,
    label: str,
    fill: str,
    stroke: str,
    font_size: int,
    checkpoint: bool = False,
    radius: int = 18,
) -> str:
    x, y, width, height = GEOMETRY[node_id]
    lines = svg_text_lines(label, 34 if width <= TOPIC_WIDTH else 28, 3)
    line_height = font_size * 1.25
    first_y = y + height / 2 - (len(lines) - 1) * line_height / 2
    text = []
    for index, line in enumerate(lines):
        text.append(
            f'<tspan x="{x + width / 2:.1f}" y="{first_y + index * line_height:.1f}">{escape(line)}</tspan>'
        )
    stroke_width = 4 if checkpoint else 2
    return (
        f'<g id="node-{node_id}" class="topic"><title>{escape(label)}</title>'
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height:.1f}" '
        f'rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}" '
        'filter="url(#shadow)"/>'
        f'<text text-anchor="middle" font-size="{font_size}" font-weight="{600 if checkpoint else 500}">'
        + "".join(text)
        + "</text></g>"
    )


def svg_edge(source: str, target: str, stroke: str, marker: str, opacity: float = 0.7) -> str:
    sx, sy, tx, ty = boundary_points(source, target)
    return (
        f'<path d="M {sx:.1f} {sy:.1f} L {tx:.1f} {ty:.1f}" fill="none" '
        f'stroke="{stroke}" stroke-width="2.4" opacity="{opacity}" marker-end="url(#{marker})"/>'
    )


def svg_summary_edge(source_group: str, target_group: str, index: int) -> str:
    source_group_obj = next(group for group in GROUPS if group.id == source_group)
    target_group_obj = next(group for group in GROUPS if group.id == target_group)
    source = f"hub-{source_group}"
    target = f"hub-{target_group}"
    sx, sy = center(source)
    tx, ty = center(target)
    middle_angle = (source_group_obj.angle + target_group_obj.angle) / 2
    control_radius = 1010 + 24 * (index % 5)
    qx, qy = polar(control_radius, middle_angle)
    return (
        f'<path d="M {sx:.1f} {sy:.1f} Q {qx:.1f} {qy:.1f} {tx:.1f} {ty:.1f}" '
        'fill="none" stroke="#59636e" stroke-width="2" stroke-dasharray="12 12" '
        'opacity="0.18" marker-end="url(#arrow-summary)"/>'
    )


def generate_svg() -> None:
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS}" height="{CANVAS}" viewBox="0 0 {CANVAS} {CANVAS}" role="img" aria-labelledby="title desc">',
        '<title id="title">Robot Control Roadmap radial prerequisite atlas</title>',
        '<desc id="desc">A radial learning atlas with foundations near the center and advanced robot-control topics extending outward.</desc>',
        "<defs>",
        '<filter id="shadow" x="-20%" y="-20%" width="140%" height="150%"><feGaussianBlur in="SourceAlpha" stdDeviation="6" result="blur"/><feOffset in="blur" dx="0" dy="5" result="offsetBlur"/><feComponentTransfer in="offsetBlur" result="shadowAlpha"><feFuncA type="linear" slope="0.13"/></feComponentTransfer><feMerge><feMergeNode in="shadowAlpha"/><feMergeNode in="SourceGraphic"/></feMerge></filter>',
        '<marker id="arrow-summary" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto" markerUnits="strokeWidth"><path d="M 0 0 L 10 5 L 0 10 z" fill="#59636e"/></marker>',
    ]
    for group in GROUPS:
        parts.append(
            f'<marker id="arrow-{group.id}" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto" markerUnits="strokeWidth"><path d="M 0 0 L 10 5 L 0 10 z" fill="{group.stroke}"/></marker>'
        )
    parts.extend(
        [
            '<marker id="arrow-A" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto" markerUnits="strokeWidth"><path d="M 0 0 L 10 5 L 0 10 z" fill="#444444"/></marker>',
            '<style>text{font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;fill:#202124}.ring-label{fill:#80868b;letter-spacing:.08em;text-transform:uppercase}.topic:hover rect{filter:url(#shadow);stroke-width:5}</style>',
            "</defs>",
            f'<rect width="{CANVAS}" height="{CANVAS}" fill="#fbfaf7"/>',
        ]
    )

    for radius, opacity in ((820, 0.25), (1360, 0.17), (2020, 0.12), (2680, 0.09)):
        parts.append(
            f'<circle cx="{CX}" cy="{CY}" r="{radius}" fill="none" stroke="#9aa0a6" stroke-width="2" opacity="{opacity}"/>'
        )

    for group in GROUPS:
        hx, hy = center(f"hub-{group.id}")
        parts.append(
            f'<path d="M {CX:.1f} {CY:.1f} L {hx:.1f} {hy:.1f}" stroke="{group.stroke}" stroke-width="8" opacity="0.12"/>'
        )
    ax, ay = center("hub-A")
    parts.append(
        f'<path d="M {CX:.1f} {CY:.1f} L {ax:.1f} {ay:.1f}" stroke="#444444" stroke-width="8" opacity="0.08"/>'
    )

    for index, (source_group, target_group) in enumerate(SUMMARY_EDGES):
        parts.append(svg_summary_edge(source_group, target_group, index))

    for group in GROUPS:
        incoming = {target for _, target in group.edges}
        roots = [topic.id for topic in group.topics if topic.id not in incoming]
        for topic_id in roots:
            parts.append(svg_edge(f"hub-{group.id}", topic_id, group.stroke, f"arrow-{group.id}", 0.48))
        for source, target in group.edges:
            parts.append(svg_edge(source, target, group.stroke, f"arrow-{group.id}", 0.72))

    sx, sy = center("D7")
    ax, ay = center("hub-A")
    qx, qy = polar(3000, -130)
    parts.append(
        f'<path d="M {sx:.1f} {sy:.1f} Q {qx:.1f} {qy:.1f} {ax:.1f} {ay:.1f}" fill="none" stroke="#666666" stroke-width="2.5" opacity="0.45" marker-end="url(#arrow-A)"/>'
    )
    for topic in APPLICATIONS:
        parts.append(svg_edge("hub-A", topic.id, "#444444", "arrow-A", 0.5))

    parts.append(
        f'<g id="node-START"><circle cx="{CX}" cy="{CY}" r="245" fill="#ffffff" stroke="#202124" stroke-width="5" filter="url(#shadow)"/>'
        f'<text x="{CX}" y="{CY - 40}" text-anchor="middle" font-size="38" font-weight="750"><tspan x="{CX}" dy="0">Robot Control</tspan><tspan x="{CX}" dy="48">Roadmap</tspan></text>'
        f'<text x="{CX}" y="{CY + 78}" text-anchor="middle" font-size="18" fill="#5f6368"><tspan x="{CX}">Start near the center</tspan><tspan x="{CX}" dy="26">and follow tracks outward</tspan></text>'
        f'<text x="{CX}" y="{CY + 160}" text-anchor="middle" font-size="14" fill="#80868b"><tspan x="{CX}">Solid: within-track order</tspan><tspan x="{CX}" dy="21">Dashed: bundled cross-track links</tspan></text></g>'
    )

    for group in GROUPS:
        parts.append(
            svg_card(
                f"hub-{group.id}",
                group.title,
                group.fill,
                group.stroke,
                19,
                True,
                25,
            )
        )
        for topic in group.topics:
            parts.append(
                svg_card(
                    topic.id,
                    topic.label,
                    group.fill,
                    group.stroke,
                    15,
                    topic.checkpoint,
                )
            )

    parts.append(svg_card("hub-A", "7. Specialization Tracks", "#ffffff", "#444444", 19, True, 25))
    for topic in APPLICATIONS:
        parts.append(svg_card(topic.id, topic.label, "#ffffff", "#444444", 15))

    parts.extend(
        [
            f'<text x="{CX:.1f}" y="{CANVAS - 75}" text-anchor="middle" font-size="17" fill="#5f6368">The full edge-level prerequisite graph is stored in roadmap-prerequisites.mmd and in the hidden Draw.io detail layer.</text>',
            "</svg>",
        ]
    )
    SVG_PATH.write_text("\n".join(parts) + "\n", encoding="utf-8")


def generate_mermaid() -> None:
    lines = [
        "%% Canonical edge-level prerequisite graph.",
        "%% The radial atlas bundles cross-domain edges only for visual clarity.",
        "flowchart TB",
        '    START["Robot Control Roadmap"]',
        "",
    ]
    for group in GROUPS:
        lines.append(f'    subgraph {group.id}["{group.title}"]')
        lines.append("        direction TB")
        for topic in group.topics:
            lines.append(f'        {topic.id}["{topic.label}"]')
        for source, target in group.edges:
            lines.append(f"        {source} --> {target}")
        lines.append("    end")
        lines.append("")

    lines.append('    subgraph A["7. Specialization Tracks"]')
    lines.append("        direction TB")
    for topic in APPLICATIONS:
        lines.append(f'        {topic.id}["{topic.label}"]')
    lines.append("    end")
    lines.append("")
    for source, target in ENTRY_EDGES:
        lines.append(f"    {source} --> {target}")
    for source, target in CROSS_EDGES:
        lines.append(f"    {source} -.-> {target}")
    for source, target in APPLICATION_EDGES:
        lines.append(f"    {source} --> {target}")
    lines.append("")

    for group in GROUPS:
        lines.append(
            f"    classDef group{group.id} fill:{group.fill},stroke:{group.stroke},color:#111"
        )
        lines.append(
            "    class " + ",".join(topic.id for topic in group.topics) + f" group{group.id}"
        )
    lines.append("    classDef groupA fill:#ffffff,stroke:#444444,color:#111")
    lines.append("    class " + ",".join(topic.id for topic in APPLICATIONS) + " groupA")
    lines.append("    classDef checkpoint stroke-width:3px")
    checkpoint_ids = [
        topic.id for group in GROUPS for topic in group.topics if topic.checkpoint
    ]
    lines.append("    class " + ",".join(checkpoint_ids) + " checkpoint")
    MERMAID_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate() -> None:
    topic_ids = {topic.id for group in GROUPS for topic in group.topics}
    topic_ids.update(topic.id for topic in APPLICATIONS)
    all_ids = topic_ids | {"START"}
    assert len(topic_ids) == 64, f"Expected 64 topics, found {len(topic_ids)}"
    assert len(all_ids) == 65

    internal_edges = [edge for group in GROUPS for edge in group.edges]
    nonlocal_edges = list(ENTRY_EDGES) + list(CROSS_EDGES) + list(APPLICATION_EDGES)
    semantic_edges = internal_edges + nonlocal_edges
    assert len(internal_edges) == 53
    assert len(ENTRY_EDGES) == 2
    assert len(CROSS_EDGES) == 44
    assert len(APPLICATION_EDGES) == 5
    assert len(nonlocal_edges) == 51
    assert len(semantic_edges) == 104
    assert len(set(semantic_edges)) == len(semantic_edges), "Duplicate prerequisite edge"

    for group in GROUPS:
        for source, target in group.edges:
            assert source in all_ids and target in all_ids
    for source, target in nonlocal_edges:
        assert source in all_ids and target in all_ids

    indegree = {node_id: 0 for node_id in all_ids}
    outgoing = {node_id: [] for node_id in all_ids}
    for source, target in semantic_edges:
        outgoing[source].append(target)
        indegree[target] += 1
    queue = [node_id for node_id, degree in indegree.items() if degree == 0]
    visited = 0
    while queue:
        source = queue.pop()
        visited += 1
        for target in outgoing[source]:
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)
    assert visited == len(all_ids), "Prerequisite graph contains a cycle"

    geometry_ids = list(GEOMETRY)
    for node_id, (x, y, width, height) in GEOMETRY.items():
        assert x >= 0 and y >= 0, f"{node_id} is outside the canvas"
        assert x + width <= CANVAS and y + height <= CANVAS, f"{node_id} is clipped"
    for index, first in enumerate(geometry_ids):
        ax, ay, aw, ah = GEOMETRY[first]
        for second in geometry_ids[index + 1 :]:
            bx, by, bw, bh = GEOMETRY[second]
            overlaps = (
                ax < bx + bw + 8
                and ax + aw + 8 > bx
                and ay < by + bh + 8
                and ay + ah + 8 > by
            )
            assert not overlaps, f"Layout overlap between {first} and {second}"

    ET.parse(DRAWIO_PATH)
    ET.parse(SVG_PATH)


def main() -> None:
    generate_drawio()
    generate_svg()
    generate_mermaid()
    validate()
    print(f"Generated {DRAWIO_PATH.relative_to(ROOT)}")
    print(f"Generated {SVG_PATH.relative_to(ROOT)}")
    print(f"Generated {MERMAID_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
