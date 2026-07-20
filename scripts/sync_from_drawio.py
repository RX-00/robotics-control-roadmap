#!/usr/bin/env python3
"""Synchronize roadmap artifacts from the canonical Draw.io document.

The Draw.io document is the source of truth for topic and section labels,
geometry, styling, checkpoints, and prerequisite edges.  The visible layer
contains the clean radial atlas; the hidden detail layer contains the exact
entry and cross-track prerequisite edges.

This script deliberately never writes the Draw.io source.  It validates that
source, then generates the public SVG, the exact Mermaid graph, and controlled
sections of the Markdown documentation.  Topic reference bodies are preserved
by stable topic-ID markers.
"""

from __future__ import annotations

import argparse
import base64
from dataclasses import dataclass
from html import escape
from html.parser import HTMLParser
from math import ceil
from pathlib import Path
import re
import sys
from textwrap import wrap
from typing import Iterable
from urllib.parse import unquote
import xml.etree.ElementTree as ET
import zlib


ROOT = Path(__file__).resolve().parents[1]
DRAWIO_PATH = ROOT / "robotics-control-roadmap.drawio"
SVG_PATH = ROOT / "images" / "robotics-control-roadmap.svg"
MERMAID_PATH = ROOT / "roadmap-prerequisites.mmd"
README_PATH = ROOT / "README.md"
UNDERSTANDING_PATH = ROOT / "docs" / "repo-understanding.md"
REFERENCES_PATH = ROOT / "topics-and-references.md"

VISIBLE_LAYER_NAME = "Radial atlas"
DETAIL_LAYER_NAME = "Detailed cross-domain prerequisites"
TOPIC_ID_RE = re.compile(r"^([A-Z]+)([1-9][0-9]*)$")
HUB_ID_RE = re.compile(r"^hub-([A-Z]+)$")
SECTION_PREFIX_RE = re.compile(r"^(\d+)([A-Za-z]?)\.\s*")


class RoadmapError(RuntimeError):
    """Raised when the Draw.io source or synchronized documents are invalid."""


@dataclass(frozen=True)
class Geometry:
    x: float
    y: float
    width: float
    height: float

    @property
    def center(self) -> tuple[float, float]:
        return self.x + self.width / 2, self.y + self.height / 2


@dataclass(frozen=True)
class Node:
    id: str
    label: str
    label_lines: tuple[str, ...]
    geometry: Geometry
    style: dict[str, str]
    group_id: str | None
    kind: str


@dataclass(frozen=True)
class Edge:
    id: str
    source: str
    target: str
    layer_id: str
    style: dict[str, str]
    points: tuple[tuple[float, float], ...]


@dataclass(frozen=True)
class Ring:
    id: str
    geometry: Geometry
    style: dict[str, str]


@dataclass(frozen=True)
class Group:
    id: str
    title: str
    hub: Node
    topics: tuple[Node, ...]
    internal_edges: tuple[Edge, ...]

    @property
    def fill(self) -> str:
        return self.hub.style.get("fillColor", "#ffffff")

    @property
    def stroke(self) -> str:
        return self.hub.style.get("strokeColor", "#444444")


@dataclass(frozen=True)
class Roadmap:
    canvas_width: float
    canvas_height: float
    background: str
    visible_layer_id: str
    detail_layer_id: str
    start: Node
    groups: tuple[Group, ...]
    nodes: dict[str, Node]
    rings: tuple[Ring, ...]
    visible_edges: tuple[Edge, ...]
    detail_edges: tuple[Edge, ...]

    @property
    def topics(self) -> tuple[Node, ...]:
        return tuple(topic for group in self.groups for topic in group.topics)

    @property
    def internal_edges(self) -> tuple[Edge, ...]:
        return tuple(edge for group in self.groups for edge in group.internal_edges)

    @property
    def entry_edges(self) -> tuple[Edge, ...]:
        return tuple(edge for edge in self.detail_edges if edge.source == "START")

    @property
    def cross_edges(self) -> tuple[Edge, ...]:
        return tuple(edge for edge in self.detail_edges if edge.source != "START")

    @property
    def semantic_edges(self) -> tuple[Edge, ...]:
        return self.internal_edges + self.detail_edges


@dataclass(frozen=True)
class CellRecord:
    id: str
    semantic_id: str
    attributes: dict[str, str]
    cell: ET.Element


class _DrawioLabelParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() in {"br", "p", "div"}:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {"p", "div"}:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def parse_style(raw: str | None) -> dict[str, str]:
    style: dict[str, str] = {}
    for item in (raw or "").split(";"):
        item = item.strip()
        if not item:
            continue
        if "=" in item:
            key, value = item.split("=", 1)
            style[key] = value
        else:
            style[item] = "1"
    return style


def style_number(style: dict[str, str], key: str, default: float) -> float:
    try:
        return float(style.get(key, default))
    except (TypeError, ValueError) as exc:
        raise RoadmapError(f"Style property {key!r} must be numeric") from exc


def label_lines(raw: str | None) -> tuple[str, ...]:
    parser = _DrawioLabelParser()
    parser.feed(raw or "")
    lines = []
    for line in "".join(parser.parts).replace("\xa0", " ").splitlines():
        normalized = " ".join(line.split())
        if normalized:
            lines.append(normalized)
    return tuple(lines)


def plain_label(raw: str | None) -> str:
    return " ".join(label_lines(raw))


def _decode_diagram(diagram: ET.Element) -> ET.Element:
    model = diagram.find("mxGraphModel")
    if model is not None:
        return model

    encoded = "".join(diagram.itertext()).strip()
    if not encoded:
        raise RoadmapError("The Draw.io page does not contain an mxGraphModel")
    try:
        compressed = base64.b64decode(encoded)
        decoded = zlib.decompress(compressed, -15).decode("utf-8")
        return ET.fromstring(unquote(decoded))
    except (ValueError, zlib.error, ET.ParseError) as exc:
        raise RoadmapError("Could not decode the compressed Draw.io page") from exc


def _cell_records(root: ET.Element) -> list[CellRecord]:
    records: list[CellRecord] = []
    for child in root:
        wrapper = None
        if child.tag == "mxCell":
            cell = child
        else:
            cell = child.find("mxCell")
            wrapper = child
        if cell is None:
            continue

        attributes = dict(wrapper.attrib) if wrapper is not None else {}
        attributes.update(cell.attrib)
        actual_id = (wrapper.attrib.get("id") if wrapper is not None else None) or cell.get("id")
        if not actual_id:
            raise RoadmapError("Every Draw.io cell must have an ID")
        semantic_id = (
            attributes.get("roadmapId")
            or attributes.get("roadmap_id")
            or actual_id
        )
        if wrapper is not None and "value" not in attributes and wrapper.get("label"):
            attributes["value"] = wrapper.get("label", "")
        records.append(CellRecord(actual_id, semantic_id, attributes, cell))
    return records


def _geometry(record: CellRecord) -> Geometry:
    geometry = record.cell.find("mxGeometry")
    if geometry is None:
        raise RoadmapError(f"Node {record.semantic_id} has no mxGeometry")
    try:
        return Geometry(
            float(geometry.get("x", "0")),
            float(geometry.get("y", "0")),
            float(geometry.get("width", "0")),
            float(geometry.get("height", "0")),
        )
    except ValueError as exc:
        raise RoadmapError(f"Node {record.semantic_id} has invalid geometry") from exc


def _edge_points(record: CellRecord) -> tuple[tuple[float, float], ...]:
    geometry = record.cell.find("mxGeometry")
    if geometry is None:
        return ()
    points: list[tuple[float, float]] = []
    array = geometry.find("Array[@as='points']")
    if array is None:
        return ()
    for point in array.findall("mxPoint"):
        try:
            points.append((float(point.get("x", "0")), float(point.get("y", "0"))))
        except ValueError as exc:
            raise RoadmapError(f"Edge {record.semantic_id} has an invalid waypoint") from exc
    return tuple(points)


def _section_sort_key(group: Group) -> tuple[int, str, str]:
    match = SECTION_PREFIX_RE.match(group.title)
    if match:
        return int(match.group(1)), match.group(2).upper(), group.id
    return 10_000, "", group.id


def _topic_sort_key(topic: Node) -> tuple[str, int]:
    match = TOPIC_ID_RE.match(topic.id)
    if match is None:
        return topic.id, 0
    return match.group(1), int(match.group(2))


def load_roadmap(path: Path = DRAWIO_PATH) -> Roadmap:
    try:
        mxfile = ET.parse(path).getroot()
    except ET.ParseError as exc:
        raise RoadmapError(f"{path.name} is not valid XML") from exc

    diagrams = mxfile.findall("diagram")
    if not diagrams:
        raise RoadmapError("The Draw.io file has no diagram page")
    diagram = next(
        (page for page in diagrams if page.get("name") == "Radial Atlas"),
        diagrams[0],
    )
    model = _decode_diagram(diagram)
    root = model.find("root")
    if root is None:
        raise RoadmapError("The Draw.io page has no root cell collection")
    records = _cell_records(root)
    by_actual_id = {record.id: record for record in records}
    if len(by_actual_id) != len(records):
        raise RoadmapError("The Draw.io file contains duplicate cell IDs")

    layers = [record for record in records if record.attributes.get("parent") == "0"]
    visible_layer = next(
        (record for record in layers if plain_label(record.attributes.get("value")) == VISIBLE_LAYER_NAME),
        None,
    )
    detail_layer = next(
        (record for record in layers if plain_label(record.attributes.get("value")) == DETAIL_LAYER_NAME),
        None,
    )
    if visible_layer is None or detail_layer is None:
        raise RoadmapError(
            f"Draw.io must contain layers named {VISIBLE_LAYER_NAME!r} and {DETAIL_LAYER_NAME!r}"
        )
    if detail_layer.attributes.get("visible", "1") != "0":
        raise RoadmapError(f"The {DETAIL_LAYER_NAME!r} layer must remain hidden by default")

    semantic_by_actual: dict[str, str] = {}
    nodes: dict[str, Node] = {}
    rings: list[Ring] = []
    for record in records:
        if record.attributes.get("vertex") != "1":
            continue
        if record.attributes.get("parent") != visible_layer.id:
            continue
        semantic_id = record.semantic_id
        semantic_by_actual[record.id] = semantic_id
        style = parse_style(record.attributes.get("style"))
        if semantic_id.startswith("ring-"):
            rings.append(Ring(semantic_id, _geometry(record), style))
            continue

        hub_match = HUB_ID_RE.match(semantic_id)
        topic_match = TOPIC_ID_RE.match(semantic_id)
        if semantic_id == "START":
            kind = "start"
            group_id = None
        elif hub_match:
            kind = "hub"
            group_id = hub_match.group(1)
        elif topic_match:
            kind = "topic"
            group_id = topic_match.group(1)
        else:
            raise RoadmapError(
                f"Unsupported visible node ID {semantic_id!r}; use START, hub-X, or a topic ID such as F1"
            )

        lines = label_lines(record.attributes.get("value"))
        label = " ".join(lines)
        if not label:
            raise RoadmapError(f"Node {semantic_id} has an empty label")
        if semantic_id in nodes:
            raise RoadmapError(f"Duplicate semantic node ID {semantic_id}")
        nodes[semantic_id] = Node(
            semantic_id,
            label,
            lines,
            _geometry(record),
            style,
            group_id,
            kind,
        )

    if "START" not in nodes:
        raise RoadmapError("The visible layer must contain the START node")

    def semantic_endpoint(actual_id: str) -> str:
        if actual_id in semantic_by_actual:
            return semantic_by_actual[actual_id]
        record = by_actual_id.get(actual_id)
        return record.semantic_id if record is not None else actual_id

    edges: list[Edge] = []
    for record in records:
        if record.attributes.get("edge") != "1":
            continue
        parent = record.attributes.get("parent", "")
        if parent not in {visible_layer.id, detail_layer.id}:
            continue
        raw_source = record.attributes.get("source")
        raw_target = record.attributes.get("target")
        if not raw_source or not raw_target:
            raise RoadmapError(f"Edge {record.semantic_id} must connect two nodes")
        source = semantic_endpoint(raw_source)
        target = semantic_endpoint(raw_target)
        edges.append(
            Edge(
                record.semantic_id,
                source,
                target,
                parent,
                parse_style(record.attributes.get("style")),
                _edge_points(record),
            )
        )

    hubs = [node for node in nodes.values() if node.kind == "hub"]
    provisional_groups: list[Group] = []
    visible_edges = tuple(edge for edge in edges if edge.layer_id == visible_layer.id)
    detail_edges = tuple(edge for edge in edges if edge.layer_id == detail_layer.id)
    for hub in hubs:
        group_id = hub.group_id
        assert group_id is not None
        topics = tuple(
            sorted(
                (node for node in nodes.values() if node.kind == "topic" and node.group_id == group_id),
                key=_topic_sort_key,
            )
        )
        internal = tuple(
            edge
            for edge in visible_edges
            if edge.source in {topic.id for topic in topics}
            and edge.target in {topic.id for topic in topics}
        )
        provisional_groups.append(Group(group_id, hub.label, hub, topics, internal))
    groups = tuple(sorted(provisional_groups, key=_section_sort_key))

    try:
        canvas_width = float(model.get("pageWidth", "0"))
        canvas_height = float(model.get("pageHeight", "0"))
    except ValueError as exc:
        raise RoadmapError("Draw.io pageWidth and pageHeight must be numeric") from exc
    roadmap = Roadmap(
        canvas_width,
        canvas_height,
        model.get("background", "#ffffff"),
        visible_layer.id,
        detail_layer.id,
        nodes["START"],
        groups,
        nodes,
        tuple(rings),
        visible_edges,
        detail_edges,
    )
    validate(roadmap)
    return roadmap


def validate(roadmap: Roadmap) -> None:
    if roadmap.canvas_width <= 0 or roadmap.canvas_height <= 0:
        raise RoadmapError("Draw.io page dimensions must be positive")
    if not roadmap.groups:
        raise RoadmapError("The roadmap must contain at least one section hub")
    if not roadmap.topics:
        raise RoadmapError("The roadmap must contain at least one topic")

    group_ids = {group.id for group in roadmap.groups}
    if len(group_ids) != len(roadmap.groups):
        raise RoadmapError("Section hub IDs must be unique")
    for group in roadmap.groups:
        if not group.topics:
            raise RoadmapError(f"Section {group.id} has no topics")
        if not group.fill.startswith("#") or not group.stroke.startswith("#"):
            raise RoadmapError(f"Section {group.id} must define hexadecimal fill and stroke colors")

    assigned_topic_ids = {topic.id for topic in roadmap.topics}
    visible_topic_ids = {
        node.id for node in roadmap.nodes.values() if node.kind == "topic"
    }
    if assigned_topic_ids != visible_topic_ids:
        raise RoadmapError(
            "Every topic ID must begin with the ID of an existing section hub"
        )

    semantic_node_ids = {"START", *(topic.id for topic in roadmap.topics)}
    for edge in roadmap.visible_edges + roadmap.detail_edges:
        if edge.source not in roadmap.nodes or edge.target not in roadmap.nodes:
            raise RoadmapError(
                f"Edge {edge.id} references unknown node {edge.source!r} or {edge.target!r}"
            )

    spoke_edge_list: list[tuple[str, str]] = []
    root_edge_list: list[tuple[str, str]] = []
    internal_pairs = {(edge.source, edge.target) for edge in roadmap.internal_edges}
    for edge in roadmap.visible_edges:
        source = roadmap.nodes[edge.source]
        target = roadmap.nodes[edge.target]
        if edge.style.get("dashed") == "1":
            raise RoadmapError(
                f"Visible edge {edge.id} is dashed; cross-track edges belong on the hidden detail layer"
            )
        if source.kind == "start" and target.kind == "hub":
            spoke_edge_list.append((edge.source, edge.target))
        elif source.kind == "hub" and target.kind == "topic":
            if source.group_id != target.group_id:
                raise RoadmapError(f"Root edge {edge.id} connects different sections")
            root_edge_list.append((edge.source, edge.target))
        elif source.kind == "topic" and target.kind == "topic":
            if source.group_id != target.group_id:
                raise RoadmapError(
                    f"Cross-track edge {edge.id} must be moved to the hidden detail layer"
                )
        else:
            raise RoadmapError(f"Unsupported visible edge {edge.id}: {edge.source} -> {edge.target}")

    spoke_edges = set(spoke_edge_list)
    root_edges = set(root_edge_list)
    if len(spoke_edges) != len(spoke_edge_list) or len(root_edges) != len(root_edge_list):
        raise RoadmapError("The visible atlas contains a duplicate spoke or section-root connector")

    expected_spokes = {("START", f"hub-{group.id}") for group in roadmap.groups}
    if spoke_edges != expected_spokes:
        raise RoadmapError("Every section hub must have exactly one visible spoke from START")

    expected_roots: set[tuple[str, str]] = set()
    for group in roadmap.groups:
        incoming = {target for _, target in internal_pairs if roadmap.nodes[target].group_id == group.id}
        expected_roots.update(
            (f"hub-{group.id}", topic.id)
            for topic in group.topics
            if topic.id not in incoming
        )
    if root_edges != expected_roots:
        missing = sorted(expected_roots - root_edges)
        extra = sorted(root_edges - expected_roots)
        raise RoadmapError(f"Section-root connectors do not match graph roots; missing={missing}, extra={extra}")

    for edge in roadmap.detail_edges:
        source = roadmap.nodes[edge.source]
        target = roadmap.nodes[edge.target]
        if target.kind != "topic":
            raise RoadmapError(f"Detailed edge {edge.id} must target a topic")
        if source.kind == "start":
            continue
        if source.kind != "topic" or source.group_id == target.group_id:
            raise RoadmapError(
                f"Detailed edge {edge.id} must be START-to-topic or cross-track topic-to-topic"
            )

    semantic_pairs = [(edge.source, edge.target) for edge in roadmap.semantic_edges]
    if len(set(semantic_pairs)) != len(semantic_pairs):
        raise RoadmapError("The semantic prerequisite graph contains a duplicate edge")

    indegree = {node_id: 0 for node_id in semantic_node_ids}
    outgoing = {node_id: [] for node_id in semantic_node_ids}
    for source, target in semantic_pairs:
        if source not in semantic_node_ids or target not in semantic_node_ids:
            raise RoadmapError(f"Semantic edge references non-topic node: {source} -> {target}")
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
    if visited != len(semantic_node_ids):
        raise RoadmapError("The prerequisite graph contains a cycle")

    visible_nodes = [roadmap.start, *(group.hub for group in roadmap.groups), *roadmap.topics]
    for node in visible_nodes:
        geometry = node.geometry
        if geometry.width <= 0 or geometry.height <= 0:
            raise RoadmapError(f"Node {node.id} must have positive dimensions")
        if geometry.x < 0 or geometry.y < 0:
            raise RoadmapError(f"Node {node.id} is outside the canvas")
        if geometry.x + geometry.width > roadmap.canvas_width or geometry.y + geometry.height > roadmap.canvas_height:
            raise RoadmapError(f"Node {node.id} is clipped by the canvas")
    for index, first in enumerate(visible_nodes):
        a = first.geometry
        for second in visible_nodes[index + 1 :]:
            b = second.geometry
            overlaps = (
                a.x < b.x + b.width + 8
                and a.x + a.width + 8 > b.x
                and a.y < b.y + b.height + 8
                and a.y + a.height + 8 > b.y
            )
            if overlaps:
                raise RoadmapError(f"Layout overlap between {first.id} and {second.id}")


def _clip_toward(node: Node, toward: tuple[float, float]) -> tuple[float, float]:
    cx, cy = node.geometry.center
    dx, dy = toward[0] - cx, toward[1] - cy
    candidates: list[float] = []
    if abs(dx) > 1e-9:
        candidates.append((node.geometry.width / 2) / abs(dx))
    if abs(dy) > 1e-9:
        candidates.append((node.geometry.height / 2) / abs(dy))
    if not candidates:
        return cx, cy
    scale = min(candidates)
    return cx + scale * dx, cy + scale * dy


def _svg_edge(edge: Edge, roadmap: Roadmap, marker_id: str | None, fallback_color: str) -> str:
    source = roadmap.nodes[edge.source]
    target = roadmap.nodes[edge.target]
    intermediate = list(edge.points)
    first_target = intermediate[0] if intermediate else target.geometry.center
    last_source = intermediate[-1] if intermediate else source.geometry.center
    if marker_id is None and source.kind == "start" and target.kind == "hub":
        start = source.geometry.center
        end = target.geometry.center
    else:
        start = _clip_toward(source, first_target)
        end = _clip_toward(target, last_source)
    points = [start, *intermediate, end]
    path = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in points)
    color = edge.style.get("strokeColor", fallback_color)
    if color in {"none", "default"}:
        color = fallback_color
    width = style_number(edge.style, "strokeWidth", 2.0)
    opacity = style_number(edge.style, "opacity", 100.0) / 100.0
    marker = f' marker-end="url(#{marker_id})"' if marker_id else ""
    return (
        f'<path d="{path}" fill="none" stroke="{escape(color)}" '
        f'stroke-width="{width:g}" opacity="{opacity:.2f}"{marker}/>'
    )


def _wrapped_lines(label: str, max_chars: int, max_lines: int = 3) -> list[str]:
    lines = wrap(label, width=max_chars, break_long_words=False, break_on_hyphens=False)
    if len(lines) <= max_lines:
        return lines
    kept = lines[: max_lines - 1]
    remainder = " ".join(lines[max_lines - 1 :])
    if len(remainder) > max_chars:
        remainder = remainder[: max_chars - 1].rstrip() + "…"
    kept.append(remainder)
    return kept


def _svg_card(node: Node) -> str:
    geometry = node.geometry
    max_chars = 28 if node.kind == "hub" else max(18, int(geometry.width / 9))
    lines = _wrapped_lines(node.label, max_chars, 3)
    base_font_size = style_number(node.style, "fontSize", 14.0)
    font_size = base_font_size + (1 if node.kind in {"hub", "topic"} else 0)
    line_height = font_size * 1.25
    first_y = geometry.y + geometry.height / 2 - (len(lines) - 1) * line_height / 2
    text = "".join(
        f'<tspan x="{geometry.x + geometry.width / 2:.1f}" y="{first_y + index * line_height:.1f}">{escape(line)}</tspan>'
        for index, line in enumerate(lines)
    )
    raw_stroke_width = style_number(node.style, "strokeWidth", 1.5)
    stroke_width = ceil(raw_stroke_width) + (1 if raw_stroke_width >= 3 else 0)
    checkpoint = node.kind == "topic" and raw_stroke_width >= 3
    bold = node.kind == "hub" or checkpoint or node.style.get("fontStyle") == "1"
    radius = style_number(node.style, "arcSize", 18.0)
    fill = node.style.get("fillColor", "#ffffff")
    stroke = node.style.get("strokeColor", "#444444")
    return (
        f'<g id="node-{escape(node.id)}" class="topic"><title>{escape(node.label)}</title>'
        f'<rect x="{geometry.x:.1f}" y="{geometry.y:.1f}" width="{geometry.width:.1f}" '
        f'height="{geometry.height:.1f}" rx="{radius:g}" fill="{escape(fill)}" '
        f'stroke="{escape(stroke)}" stroke-width="{stroke_width}" filter="url(#shadow)"/>'
        f'<text text-anchor="middle" font-size="{font_size:g}" font-weight="{600 if bold else 500}">{text}</text></g>'
    )


def _svg_start(node: Node) -> str:
    cx, cy = node.geometry.center
    radius = min(node.geometry.width, node.geometry.height) / 2
    title = node.label_lines[0] if node.label_lines else node.label
    title_lines = _wrapped_lines(title, 14, 2)
    subtitle = node.label_lines[1] if len(node.label_lines) > 1 else ""
    subtitle_lines = _wrapped_lines(subtitle, 26, 2) if subtitle else []
    legend_lines = list(node.label_lines[2:4])
    title_start = cy - 40 - (len(title_lines) - 2) * 24
    title_text = "".join(
        f'<tspan x="{cx:.1f}" y="{title_start + index * 48:.1f}">{escape(line)}</tspan>'
        for index, line in enumerate(title_lines)
    )
    subtitle_text = "".join(
        f'<tspan x="{cx:.1f}" y="{cy + 78 + index * 26:.1f}">{escape(line)}</tspan>'
        for index, line in enumerate(subtitle_lines)
    )
    legend_text = "".join(
        f'<tspan x="{cx:.1f}" y="{cy + 160 + index * 21:.1f}">{escape(line)}</tspan>'
        for index, line in enumerate(legend_lines)
    )
    return (
        f'<g id="node-START"><circle cx="{cx:.1f}" cy="{cy:.1f}" r="{radius:.1f}" '
        f'fill="{escape(node.style.get("fillColor", "#ffffff"))}" '
        f'stroke="{escape(node.style.get("strokeColor", "#202124"))}" stroke-width="5" filter="url(#shadow)"/>'
        f'<text text-anchor="middle" font-size="38" font-weight="750">{title_text}</text>'
        f'<text text-anchor="middle" font-size="18" fill="#5f6368">{subtitle_text}</text>'
        f'<text text-anchor="middle" font-size="14" fill="#80868b">{legend_text}</text></g>'
    )


def render_svg(roadmap: Roadmap) -> str:
    width = f"{roadmap.canvas_width:g}"
    height = f"{roadmap.canvas_height:g}"
    cx, _ = roadmap.start.geometry.center
    marker_colors = {group.id: group.stroke for group in roadmap.groups}
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">Robot Control Roadmap radial prerequisite atlas</title>',
        '<desc id="desc">A radial learning atlas with foundations near the center and advanced robot-control topics extending outward.</desc>',
        "<defs>",
        '<filter id="shadow" x="-20%" y="-20%" width="140%" height="150%"><feGaussianBlur in="SourceAlpha" stdDeviation="6" result="blur"/><feOffset in="blur" dx="0" dy="5" result="offsetBlur"/><feComponentTransfer in="offsetBlur" result="shadowAlpha"><feFuncA type="linear" slope="0.13"/></feComponentTransfer><feMerge><feMergeNode in="shadowAlpha"/><feMergeNode in="SourceGraphic"/></feMerge></filter>',
    ]
    for group_id, color in marker_colors.items():
        parts.append(
            f'<marker id="arrow-{group_id}" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto" markerUnits="strokeWidth"><path d="M 0 0 L 10 5 L 0 10 z" fill="{escape(color)}"/></marker>'
        )
    parts.extend(
        [
            '<style>text{font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;fill:#202124}.topic:hover rect{filter:url(#shadow);stroke-width:5}</style>',
            "</defs>",
            f'<rect width="{width}" height="{height}" fill="{escape(roadmap.background)}"/>',
        ]
    )

    for ring in roadmap.rings:
        geometry = ring.geometry
        stroke_width = style_number(ring.style, "strokeWidth", 1.0) * 2
        opacity = min(1.0, style_number(ring.style, "opacity", 20.0) / 100.0 * 0.7)
        parts.append(
            f'<ellipse cx="{geometry.x + geometry.width / 2:.1f}" cy="{geometry.y + geometry.height / 2:.1f}" '
            f'rx="{geometry.width / 2:.1f}" ry="{geometry.height / 2:.1f}" fill="none" '
            f'stroke="{escape(ring.style.get("strokeColor", "#9aa0a6"))}" stroke-width="{stroke_width:g}" opacity="{opacity:.2f}"/>'
        )

    group_by_id = {group.id: group for group in roadmap.groups}
    for edge in roadmap.visible_edges:
        source = roadmap.nodes[edge.source]
        target = roadmap.nodes[edge.target]
        if source.kind == "start" and target.kind == "hub":
            assert target.group_id is not None
            group = group_by_id[target.group_id]
            fallback = group.stroke
            adjusted_style = dict(edge.style)
            adjusted_style.setdefault("strokeColor", fallback)
            adjusted_style["strokeWidth"] = str(style_number(edge.style, "strokeWidth", 5.0) * 1.6)
            adjusted_style["opacity"] = str(style_number(edge.style, "opacity", 18.0) * 2 / 3)
            edge = Edge(edge.id, edge.source, edge.target, edge.layer_id, adjusted_style, edge.points)
            parts.append(_svg_edge(edge, roadmap, None, fallback))
        elif source.kind == "hub" and target.kind == "topic":
            assert target.group_id is not None
            group = group_by_id[target.group_id]
            adjusted_style = dict(edge.style)
            adjusted_style["strokeWidth"] = str(style_number(edge.style, "strokeWidth", 2.0) * 1.2)
            adjusted_style["opacity"] = str(style_number(edge.style, "opacity", 55.0) * 48 / 55)
            edge = Edge(edge.id, edge.source, edge.target, edge.layer_id, adjusted_style, edge.points)
            parts.append(_svg_edge(edge, roadmap, f"arrow-{group.id}", group.stroke))
        else:
            assert source.group_id is not None
            group = group_by_id[source.group_id]
            adjusted_style = dict(edge.style)
            adjusted_style["strokeWidth"] = str(style_number(edge.style, "strokeWidth", 2.0) * 1.2)
            edge = Edge(edge.id, edge.source, edge.target, edge.layer_id, adjusted_style, edge.points)
            parts.append(_svg_edge(edge, roadmap, f"arrow-{group.id}", group.stroke))

    parts.append(_svg_start(roadmap.start))
    for group in roadmap.groups:
        parts.append(_svg_card(group.hub))
        for topic in group.topics:
            parts.append(_svg_card(topic))
    parts.extend(
        [
            f'<text x="{cx:.1f}" y="{roadmap.canvas_height - 75:.1f}" text-anchor="middle" font-size="17" fill="#5f6368">The full edge-level prerequisite graph is stored in roadmap-prerequisites.mmd and in the hidden Draw.io detail layer.</text>',
            "</svg>",
        ]
    )
    output = "\n".join(parts) + "\n"
    try:
        ET.fromstring(output)
    except ET.ParseError as exc:
        raise RoadmapError("Generated SVG is invalid XML") from exc
    return output


def _mermaid_label(label: str) -> str:
    return label.replace("\\", "\\\\").replace('"', '\\"')


def render_mermaid(roadmap: Roadmap) -> str:
    lines = [
        "%% Generated from robotics-control-roadmap.drawio. Do not edit this file directly.",
        "%% Cross-domain edges are omitted from the public radial atlas for visual clarity.",
        "flowchart TB",
        f'    START["{_mermaid_label(roadmap.start.label_lines[0])}"]',
        "",
    ]
    for group in roadmap.groups:
        lines.append(f'    subgraph {group.id}["{_mermaid_label(group.title)}"]')
        lines.append("        direction TB")
        for topic in group.topics:
            lines.append(f'        {topic.id}["{_mermaid_label(topic.label)}"]')
        for edge in group.internal_edges:
            lines.append(f"        {edge.source} --> {edge.target}")
        lines.append("    end")
        lines.append("")
    for edge in roadmap.entry_edges:
        lines.append(f"    {edge.source} --> {edge.target}")
    for edge in roadmap.cross_edges:
        lines.append(f"    {edge.source} -.-> {edge.target}")
    lines.append("")
    checkpoint_ids: list[str] = []
    for group in roadmap.groups:
        lines.append(
            f"    classDef group{group.id} fill:{group.fill},stroke:{group.stroke},color:#111"
        )
        lines.append(
            "    class " + ",".join(topic.id for topic in group.topics) + f" group{group.id}"
        )
        checkpoint_ids.extend(
            topic.id
            for topic in group.topics
            if style_number(topic.style, "strokeWidth", 1.5) >= 3
        )
    lines.append("    classDef checkpoint stroke-width:3px")
    if checkpoint_ids:
        lines.append("    class " + ",".join(checkpoint_ids) + " checkpoint")
    return "\n".join(lines) + "\n"


def _replace_generated_block(
    text: str,
    heading: str,
    start_marker: str,
    end_marker: str,
    body: str,
) -> str:
    replacement = f"{start_marker}\n{body.rstrip()}\n{end_marker}"
    if start_marker in text or end_marker in text:
        if text.count(start_marker) != 1 or text.count(end_marker) != 1:
            raise RoadmapError(f"Malformed generated block markers for {heading}")
        start = text.index(start_marker)
        end = text.index(end_marker, start) + len(end_marker)
        return text[:start] + replacement + text[end:]

    heading_token = f"## {heading}\n"
    start = text.find(heading_token)
    if start < 0:
        raise RoadmapError(f"Could not find Markdown section {heading!r}")
    content_start = start + len(heading_token)
    next_heading = text.find("\n## ", content_start)
    content_end = len(text) if next_heading < 0 else next_heading + 1
    return text[:content_start] + "\n" + replacement + "\n\n" + text[content_end:]


def sync_readme(text: str, roadmap: Roadmap) -> str:
    body = [
        f"The current atlas contains {len(roadmap.topics)} topic nodes organized into {len(roadmap.groups)} content areas:",
        "",
        *(f"- {group.title}" for group in roadmap.groups),
    ]
    return _replace_generated_block(
        text,
        "Roadmap Contents",
        "<!-- roadmap-contents:start -->",
        "<!-- roadmap-contents:end -->",
        "\n".join(body),
    )


def sync_understanding(text: str, roadmap: Roadmap) -> str:
    total_nodes = len(roadmap.topics) + 1
    body = [
        f"The canonical Draw.io source contains {len(roadmap.topics)} topic nodes across {len(roadmap.groups)} content areas:",
        "",
        *(f"- {group.title}" for group in roadmap.groups),
        "",
        f"The synchronized semantic graph contains {total_nodes} nodes when the central roadmap node is included, and {len(roadmap.semantic_edges)} directed prerequisite edges:",
        "",
        f"- {len(roadmap.internal_edges)} within-track edges; and",
        f"- {len(roadmap.detail_edges)} cross-track or entry edges.",
        "",
        "The graph is acyclic.",
    ]
    return _replace_generated_block(
        text,
        "Canonical Content",
        "<!-- roadmap-canonical:start -->",
        "<!-- roadmap-canonical:end -->",
        "\n".join(body),
    )


def _meaningful_reference_body(body: str) -> bool:
    normalized = "\n".join(line.rstrip() for line in body.strip().splitlines()).strip()
    return normalized not in {"", "References:"}


def _legacy_topic_bodies(text: str, roadmap: Roadmap) -> dict[str, str]:
    matches = list(re.finditer(r"^### (.+)$", text, flags=re.MULTILINE))
    by_label = {topic.label: topic.id for topic in roadmap.topics}
    bodies: dict[str, str] = {}
    for index, match in enumerate(matches):
        label = match.group(1).strip()
        topic_id = by_label.get(label)
        if topic_id is None:
            raise RoadmapError(
                f"Legacy reference heading {label!r} does not match any Draw.io topic; add stable markers before renaming it"
            )
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        next_group = text.find("\n## ", match.end(), end)
        if next_group >= 0:
            end = next_group
        body = text[match.end():end].strip("\n")
        bodies[topic_id] = body
    return bodies


def _marked_reference_bodies(text: str) -> tuple[dict[str, str], dict[str, str]]:
    marker_re = re.compile(r"^<!-- roadmap-(group|topic):([A-Za-z0-9_-]+) -->$", re.MULTILINE)
    matches = list(marker_re.finditer(text))
    topic_bodies: dict[str, str] = {}
    group_bodies: dict[str, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        segment = text[match.end():end].lstrip("\n")
        heading_match = re.match(r"#{2,3} .+\n?", segment)
        if heading_match is None:
            raise RoadmapError(f"Reference marker {match.group(2)} is not followed by a heading")
        body = segment[heading_match.end():].strip("\n")
        destination = group_bodies if match.group(1) == "group" else topic_bodies
        marker_id = match.group(2)
        if marker_id in destination:
            raise RoadmapError(f"Duplicate reference marker {marker_id}")
        destination[marker_id] = body
    return topic_bodies, group_bodies


def sync_references(text: str, roadmap: Roadmap) -> str:
    has_markers = "<!-- roadmap-topic:" in text
    if has_markers:
        topic_bodies, group_bodies = _marked_reference_bodies(text)
    else:
        topic_bodies = _legacy_topic_bodies(text, roadmap)
        group_bodies = {}

    current_topic_ids = {topic.id for topic in roadmap.topics}
    for removed_id in sorted(set(topic_bodies) - current_topic_ids):
        if _meaningful_reference_body(topic_bodies[removed_id]):
            raise RoadmapError(
                f"Topic {removed_id} was removed from Draw.io but still has curated reference content"
            )

    current_group_ids = {group.id for group in roadmap.groups}
    for removed_id in sorted(set(group_bodies) - current_group_ids):
        if group_bodies[removed_id].strip():
            raise RoadmapError(
                f"Section {removed_id} was removed from Draw.io but still has introductory content"
            )

    lines = [
        "# Topics and References",
        "",
        "<!-- roadmap-reference-index:start -->",
        f"This index mirrors the {len(roadmap.topics)} topic nodes in the robot-control roadmap. Topic headings are synchronized from Draw.io; content beneath each heading is preserved.",
        "<!-- roadmap-reference-index:end -->",
    ]
    for group in roadmap.groups:
        lines.extend(["", f"<!-- roadmap-group:{group.id} -->", f"## {group.title}"])
        group_body = group_bodies.get(group.id, "").strip("\n")
        if group_body:
            lines.extend(["", group_body])
        for topic in group.topics:
            body = topic_bodies.get(topic.id, "References:").strip("\n") or "References:"
            lines.extend(
                [
                    "",
                    f"<!-- roadmap-topic:{topic.id} -->",
                    f"### {topic.label}",
                    "",
                    body,
                ]
            )
    return "\n".join(lines).rstrip() + "\n"


def build_outputs(roadmap: Roadmap) -> dict[Path, str]:
    return {
        SVG_PATH: render_svg(roadmap),
        MERMAID_PATH: render_mermaid(roadmap),
        README_PATH: sync_readme(README_PATH.read_text(encoding="utf-8"), roadmap),
        UNDERSTANDING_PATH: sync_understanding(
            UNDERSTANDING_PATH.read_text(encoding="utf-8"), roadmap
        ),
        REFERENCES_PATH: sync_references(
            REFERENCES_PATH.read_text(encoding="utf-8"), roadmap
        ),
    }


def _relative(paths: Iterable[Path]) -> str:
    return ", ".join(str(path.relative_to(ROOT)) for path in paths)


def synchronize(check: bool = False) -> int:
    roadmap = load_roadmap()
    outputs = build_outputs(roadmap)
    stale = [
        path
        for path, expected in outputs.items()
        if not path.exists() or path.read_text(encoding="utf-8") != expected
    ]
    if check:
        if stale:
            print(f"Out-of-date generated files: {_relative(stale)}", file=sys.stderr)
            return 1
        print(
            f"Roadmap is synchronized: {len(roadmap.topics)} topics, "
            f"{len(roadmap.semantic_edges)} prerequisite edges"
        )
        return 0

    for path in stale:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(outputs[path], encoding="utf-8")
        print(f"Synchronized {path.relative_to(ROOT)}")
    if not stale:
        print("All generated roadmap files are already synchronized")
    print(
        f"Validated {len(roadmap.topics)} topics, {len(roadmap.groups)} sections, "
        f"and {len(roadmap.semantic_edges)} prerequisite edges"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate robotics-control-roadmap.drawio and synchronize generated artifacts."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate and report stale generated files without writing them",
    )
    args = parser.parse_args()
    try:
        return synchronize(check=args.check)
    except (OSError, RoadmapError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
