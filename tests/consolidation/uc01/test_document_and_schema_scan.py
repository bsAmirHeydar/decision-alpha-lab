from pathlib import Path

from tools.consolidation.uc01.document_scan import scan_documents, scan_path_references, scan_schemas


def test_document_scan_and_id_collision(tmp_path: Path) -> None:
    first = tmp_path / "docs" / "a.md"
    second = tmp_path / "docs" / "b.md"
    first.parent.mkdir(parents=True)
    content = "---\nid: SAME-ID\ntitle: A\n---\n# A\n[[docs/b]]\n"
    first.write_text(content, encoding="utf-8")
    second.write_text(content.replace("# A", "# B"), encoding="utf-8")
    result = scan_documents(tmp_path, ["docs/a.md", "docs/b.md"])
    assert len(result["documents"]) == 2
    assert result["collisions"][0]["note_id"] == "SAME-ID"
    assert result["links"][0]["kind"] == "wikilink"


def test_schema_and_path_reference_scan(tmp_path: Path) -> None:
    schema = tmp_path / "schemas" / "sample.schema.json"
    source = tmp_path / "tools" / "run.py"
    schema.parent.mkdir(parents=True)
    source.parent.mkdir(parents=True)
    schema.write_text('{"$schema":"https://json-schema.org/draft/2020-12/schema","title":"X","properties":{"a":{"type":"string"}}}', encoding="utf-8")
    source.write_text('PATH = "schemas/sample.schema.json"\n', encoding="utf-8")
    rows, issues = scan_schemas(tmp_path, ["schemas/sample.schema.json"])
    refs, ref_issues = scan_path_references(tmp_path, ["tools/run.py"])
    assert rows[0]["schema_type"] == "json_schema"
    assert rows[0]["property_count"] == 1
    assert not issues
    assert refs[0]["target_exists"] is True
    assert not ref_issues
