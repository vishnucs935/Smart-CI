from scripts import cache_build


def test_pricing_change_rebuilds_dependants(tmp_path, monkeypatch):
    source = tmp_path / "src"
    source.mkdir()
    pricing = source / "pricing.py"
    pricing.write_text("def price(): return 10")
    (source / "__init__.py").touch()
    (source / "cart.py").write_text("from src.pricing import price")
    (source / "inventory.py").write_text("stock = 20")
    cache = tmp_path / ".smartci-cache"
    for name, path in {
        "ROOT": tmp_path, "SOURCE_DIR": source, "ARTIFACT_DIR": cache / "artifacts",
        "RECEIPT_FILE": cache / "receipt.json",
    }.items():
        monkeypatch.setattr(cache_build, name, path)

    assert cache_build.build_cache()["misses"] == 4
    assert cache_build.build_cache()["hits"] == 4
    pricing.write_text("def price(): return 12")
    assert cache_build.build_cache() == {"hits": 2, "misses": 2, "total": 4}
