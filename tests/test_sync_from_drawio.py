import base64
from pathlib import Path
import tempfile
import unittest
from urllib.parse import quote
import xml.etree.ElementTree as ET
import zlib

from scripts import sync_from_drawio as sync


class SyncFromDrawioTests(unittest.TestCase):
    def test_graph_inventory_is_internally_consistent(self) -> None:
        roadmap = sync.load_roadmap()

        self.assertGreater(len(roadmap.groups), 0)
        self.assertEqual(
            len(roadmap.topics),
            sum(len(group.topics) for group in roadmap.groups),
        )
        self.assertEqual(
            len(roadmap.semantic_edges),
            len(roadmap.internal_edges) + len(roadmap.detail_edges),
        )
        self.assertEqual(
            [group.order for group in roadmap.groups],
            list(range(1, len(roadmap.groups) + 1)),
        )

    def test_section_hubs_require_explicit_consecutive_ordering(self) -> None:
        tree = ET.parse(sync.DRAWIO_PATH)
        hub = tree.find(".//mxCell[@id='hub-F']")
        self.assertIsNotNone(hub)
        assert hub is not None
        del hub.attrib["roadmapOrder"]

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "missing-order.drawio"
            tree.write(path, encoding="unicode")
            with self.assertRaisesRegex(sync.RoadmapError, "roadmapOrder"):
                sync.load_roadmap(path)

    def test_hub_order_works_with_a_custom_semantic_id(self) -> None:
        tree = ET.parse(sync.DRAWIO_PATH)
        hub = tree.find(".//mxCell[@id='hub-F']")
        self.assertIsNotNone(hub)
        assert hub is not None
        hub.set("id", "drawio-hub-foundations")
        hub.set("roadmapId", "hub-F")
        for edge in tree.findall(".//mxCell[@edge='1']"):
            if edge.get("source") == "hub-F":
                edge.set("source", "drawio-hub-foundations")
            if edge.get("target") == "hub-F":
                edge.set("target", "drawio-hub-foundations")

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "custom-hub-id.drawio"
            tree.write(path, encoding="unicode")
            roadmap = sync.load_roadmap(path)

        self.assertEqual(roadmap.groups[0].id, "F")
        self.assertEqual(roadmap.groups[0].order, 1)

    def test_current_outputs_are_synchronized(self) -> None:
        roadmap = sync.load_roadmap()

        for path, expected in sync.build_outputs(roadmap).items():
            self.assertEqual(path.read_text(encoding="utf-8"), expected, path.name)

    def test_compressed_drawio_pages_are_supported(self) -> None:
        source = ET.parse(sync.DRAWIO_PATH)
        model = source.find(".//mxGraphModel")
        self.assertIsNotNone(model)
        assert model is not None
        encoded_xml = quote(ET.tostring(model, encoding="unicode"), safe="~()*!.'")
        compressor = zlib.compressobj(level=9, wbits=-15)
        compressed = compressor.compress(encoded_xml.encode("utf-8")) + compressor.flush()
        payload = base64.b64encode(compressed).decode("ascii")
        mxfile = ET.Element("mxfile")
        diagram = ET.SubElement(mxfile, "diagram", {"name": "Radial Atlas"})
        diagram.text = payload

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "compressed.drawio"
            ET.ElementTree(mxfile).write(path, encoding="unicode")
            roadmap = sync.load_roadmap(path)

        self.assertGreater(len(roadmap.topics), 0)
        self.assertGreater(len(roadmap.semantic_edges), 0)

    def test_drawio_edits_propagate_to_svg_and_mermaid(self) -> None:
        tree = ET.parse(sync.DRAWIO_PATH)
        topic = tree.find(".//mxCell[@id='F1']")
        self.assertIsNotNone(topic)
        assert topic is not None
        topic.set("value", "Linear algebra, geometry, and transforms")
        geometry = topic.find("mxGeometry")
        self.assertIsNotNone(geometry)
        assert geometry is not None
        geometry.set("x", str(float(geometry.get("x", "0")) + 10))

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "edited.drawio"
            tree.write(path, encoding="unicode")
            roadmap = sync.load_roadmap(path)

        edited = roadmap.nodes["F1"]
        self.assertEqual(edited.label, "Linear algebra, geometry, and transforms")
        self.assertIn(
            'F1["Linear algebra, geometry, and transforms"]',
            sync.render_mermaid(roadmap),
        )
        self.assertIn(f'x="{edited.geometry.x:.1f}"', sync.render_svg(roadmap))

    def test_hidden_edge_edit_propagates_to_mermaid(self) -> None:
        tree = ET.parse(sync.DRAWIO_PATH)
        root = tree.find(".//mxGraphModel/root")
        self.assertIsNotNone(root)
        assert root is not None
        edge = ET.SubElement(
            root,
            "mxCell",
            {
                "id": "test-cross-edge",
                "edge": "1",
                "parent": "2",
                "source": "F1",
                "target": "C1",
                "style": "edgeStyle=none;curved=1;dashed=1;",
            },
        )
        ET.SubElement(edge, "mxGeometry", {"relative": "1", "as": "geometry"})

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "edited.drawio"
            tree.write(path, encoding="unicode")
            roadmap = sync.load_roadmap(path)

        self.assertIn("F1 -.-> C1", sync.render_mermaid(roadmap))

    def test_reference_body_survives_a_drawio_rename(self) -> None:
        tree = ET.parse(sync.DRAWIO_PATH)
        topic = tree.find(".//mxCell[@id='F1']")
        self.assertIsNotNone(topic)
        assert topic is not None
        topic.set("value", "Linear algebra, geometry, and transforms")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "edited.drawio"
            tree.write(path, encoding="unicode")
            roadmap = sync.load_roadmap(path)

        source = sync.REFERENCES_PATH.read_text(encoding="utf-8")
        source = source.replace(
            "<!-- roadmap-topic:F1 -->\n### Linear algebra and geometry\n\nReferences:",
            "<!-- roadmap-topic:F1 -->\n### Linear algebra and geometry\n\nReferences:\n\n- Example reference",
            1,
        )

        synchronized = sync.sync_references(source, roadmap)

        self.assertIn("<!-- roadmap-topic:F1 -->", synchronized)
        self.assertIn("### Linear algebra, geometry, and transforms", synchronized)
        self.assertIn("- Example reference", synchronized)


if __name__ == "__main__":
    unittest.main()
