from .conftest import jl
def test_all_atoms_are_packaged_once():
 rows=jl("registries/treatment_package_registry.jsonl");assert len(rows)==422;assert sum(x["atom_count"] for x in rows)==1109;assert len({x["source_path"] for x in rows})==422
