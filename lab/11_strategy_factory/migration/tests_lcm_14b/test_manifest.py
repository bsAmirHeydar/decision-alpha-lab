def test_manifest(load):
 m=load("output_manifest.json")
 assert m["file_count"]==len(m["files"]) and m["file_count"]>500
