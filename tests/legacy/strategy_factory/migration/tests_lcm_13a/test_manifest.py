def test_output_manifest_matches_files(dual_root):
    import json
    manifest = json.loads((dual_root / "output_manifest.json").read_text(encoding="utf-8"))
    actual = sorted(p.relative_to(dual_root).as_posix() for p in dual_root.rglob("*") if p.is_file() and p.name != "output_manifest.json")
    assert manifest["files"] == actual
    assert manifest["file_count"] == len(actual)
