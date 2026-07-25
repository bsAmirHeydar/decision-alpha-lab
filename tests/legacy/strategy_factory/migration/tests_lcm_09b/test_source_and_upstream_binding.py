from tools.strategy_factory.lcm.lcm_09b.canonical import digest_object
from tools.strategy_factory.lcm.lcm_09b.source_digest import source_binding_matches

from .conftest import REPO, j


def test_exact_upstream_handoff_and_zero_authorized_implementations():
    binding = j("input/lcm09a_binding.json")
    assert (
        binding["handoff_digest"]
        == "sha256:9010023f1b182049cc9f7e0601689827c062f2dbb15e21a98d652744c625d2fb"
    )
    assert binding["implementation_authorized_setup_ids"] == []
    assert digest_object(binding, "binding_digest") == binding["binding_digest"]


def test_every_source_binding_still_matches_repository_content():
    """Verify source content independently of Windows CRLF checkout policy."""

    for row in j("canonical_setup_registry.json")["packages"]:
        package = j(row["package_path"])
        source = REPO / package["source_binding"]["path"]
        assert source.is_file()
        assert source_binding_matches(source, package["source_binding"]["sha256"])
        assert package["source_binding"]["source_move_performed"] is False
        assert package["source_binding"]["source_delete_performed"] is False
