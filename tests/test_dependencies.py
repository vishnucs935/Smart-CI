from scripts.dependencies import (
    build_module_map,
    get_direct_dependencies,
    get_transitive_dependencies,
)


def create_project(tmp_path):
    source = tmp_path / "src"
    source.mkdir()

    return source


def test_direct_dependency(tmp_path):
    source = create_project(tmp_path)

    pricing = source / "pricing.py"
    cart = source / "cart.py"

    pricing.write_text("def total(): return 100")
    cart.write_text("from src.pricing import total")

    module_map = build_module_map(tmp_path)

    result = get_direct_dependencies(cart, tmp_path, module_map)

    assert pricing in result


def test_transitive_dependency(tmp_path):
    source = create_project(tmp_path)

    tax = source / "tax.py"
    pricing = source / "pricing.py"
    cart = source / "cart.py"

    tax.write_text("RATE = 18")
    pricing.write_text("from src.tax import RATE")
    cart.write_text("from src.pricing import calculate")

    result = get_transitive_dependencies(cart, tmp_path)

    assert pricing in result
    assert tax in result


def test_unrelated_file_is_not_dependency(tmp_path):
    source = create_project(tmp_path)

    pricing = source / "pricing.py"
    inventory = source / "inventory.py"

    pricing.write_text("PRICE = 100")
    inventory.write_text("STOCK = 10")

    module_map = build_module_map(tmp_path)

    result = get_direct_dependencies(
        inventory, tmp_path, module_map
    )

    assert pricing not in result


def test_syntax_error_returns_empty_dependencies(tmp_path):
    source = create_project(tmp_path)

    broken = source / "broken.py"
    broken.write_text("def invalid(")

    module_map = build_module_map(tmp_path)

    result = get_direct_dependencies(
        broken, tmp_path, module_map
    )

    assert result == set()
