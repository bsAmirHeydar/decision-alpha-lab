import json
def test_archive_restore(package_root):d=json.loads((package_root/'archive_restore_sample.json').read_text());assert (d['sample_count'],d['pass_count'],d['fail_count'])==(12,12,0)
