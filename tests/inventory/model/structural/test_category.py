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


@pytest.mark.parametrize(
    "model, field_name, expected_type, related_model, on_delete_behavior, allow_null, allow_blank",
    [
        (Category, "parent", models.ForeignKey, Category, models.PROTECT, True, True),
    ],
)
def test_model_structure_relationship(
    model,
    field_name,
    expected_type,
    related_model,
    on_delete_behavior,
    allow_null,
    allow_blank,
):
    assert hasattr(
        model, field_name
    ), f"{model.name} model does not have '{field_name}' field"

    field = model._meta.get_field(field_name)

    assert isinstance(
        field, expected_type
    ), f"Field {field_name} is not type {expected_type}"

    assert field.related_model == related_model

    assert (
        field.remote_field.on_delete == on_delete_behavior
    ), f"'{field_name}' field does not have on_delete={on_delete_behavior}"

    assert field.null == allow_null
    assert field.blank == allow_blank
