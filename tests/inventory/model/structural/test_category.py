import pytest
from django.db import models

from inventory.models import Category


def test_model_structure_table_exists():
    try:
        from inventory.models import Category  # noqa F401
    except ImportError:
        assert False
    else:
        assert True


@pytest.mark.parametrize(
    "model, field_name, expected_type",
    [
        (Category, "id", models.AutoField),
        (Category, "name", models.CharField),
        (Category, "slug", models.SlugField),
        (Category, "is_active", models.BooleanField),
        (Category, "level", models.IntegerField),
        (Category, "parent", models.ForeignKey),
    ],
)
def test_model_structure_column_data_types(model, field_name, expected_type):
    assert hasattr(
        model, field_name
    ), f"{model.name} model does not have '{field_name}' field"

    field = model._meta.get_field(field_name)

    assert isinstance(
        field, expected_type
    ), f"Field {field_name} is not type {expected_type}"
