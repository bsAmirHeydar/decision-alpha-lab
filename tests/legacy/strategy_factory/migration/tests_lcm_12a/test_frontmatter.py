from tools.strategy_factory.lcm.lcm_12a.frontmatter import split_frontmatter,first_heading,heading_anchors
def test_frontmatter_and_headings():
    fm,body=split_frontmatter("---\ntitle: X\nversion: 1.0\n---\n# Hello World\n")
    assert fm["title"]=="X" and first_heading(body)=="Hello World" and "hello-world" in heading_anchors(body)
