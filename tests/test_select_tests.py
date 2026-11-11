from scripts.select_tests import select_tests


def test_pricing_change_selects_related_tests():
    mode, selected, reason = select_tests(["src/pricing.py"])

    names = {path.name for path in selected}

    assert mode == "selected"
    assert "test_pricing.py" in names
    assert "test_cart.py" in names


def test_documentation_change_selects_no_tests():
    mode, selected, reason = select_tests(["docs/README.md"])

    assert mode == "none"
    assert selected == set()


def test_test_file_change_selects_itself():
    mode, selected, reason = select_tests(
        ["tests/test_inventory.py"]
    )

    assert mode == "selected"
    assert {path.name for path in selected} == {
        "test_inventory.py"
    }


def test_unknown_file_uses_full_suite():
    mode, selected, reason = select_tests(
        ["unknown_config.txt"]
    )

    assert mode == "full"
    assert selected == set()


def test_deleted_source_uses_full_suite():
    mode, selected, reason = select_tests(
        ["src/deleted_module.py"]
    )

    assert mode == "full"


def test_changed_fixture_uses_full_suite():
    mode, selected, reason = select_tests(
        ["tests/fixtures/data.json"]
    )

    assert mode == "full"


def test_empty_change_history_uses_full_suite():
    mode, selected, reason = select_tests([])

    assert mode == "full"
