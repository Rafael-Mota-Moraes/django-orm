def test_model_structure_table_exists():
    try:
        from inventory.models import Category  # noqa F401
    except ImportError:
        assert False
    else:
        assert True


def test_model_1():
    return True


def test_structure_2():
    return True
