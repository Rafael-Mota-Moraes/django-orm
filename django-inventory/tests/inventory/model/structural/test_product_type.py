import pytest
from django.db import models

from inventory.models import ProductType


def test_model_structure_table_exists():
    try:
        from inventory.models import ProductType  # noqa F401
    except ImportError:
        assert False
    else:
        assert True


@pytest.mark.parametrize(
    "model, field_name, expected_type",
    [
        (ProductType, "id", models.AutoField),
        (ProductType, "name", models.CharField),
        (ProductType, "level", models.IntegerField),
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
        (
            ProductType,
            "parent",
            models.ForeignKey,
            ProductType,
            models.PROTECT,
            True,
            True,
        ),
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


@pytest.mark.parametrize(
    "model, field_name, expected_nullable",
    [
        (ProductType, "id", False),
        (ProductType, "name", False),
        (ProductType, "level", False),
    ],
)
def test_model_structure_nullable_constraints(model, field_name, expected_nullable):
    field = model._meta.get_field(field_name)

    assert (
        field.null is expected_nullable
    ), f"Field '{field_name}' has unexpected nullable constraint"


@pytest.mark.parametrize(
    "model, field_name, expected_length",
    [
        (ProductType, "name", 100),
    ],
)
def test_model_structure_column_lenghts(model, field_name, expected_length):
    field = model._meta.get_field(field_name)

    assert (
        field.max_length == expected_length
    ), f"Field '{field_name}' has unexpected max lenght"


@pytest.mark.parametrize(
    "model, expected_field_count",
    [
        (
            ProductType,
            4,
        ),
    ],
)
def test_Model_structure_field_count(model, expected_field_count):
    field_count = len(model._meta.fields)
    assert (
        field_count == expected_field_count
    ), f"{model.__name__} model has {field_count} fields, expected {expected_field_count}"


@pytest.mark.parametrize(
    "model, field_name, is_unique",
    [
        (ProductType, "id", True),
        (ProductType, "name", False),
        (ProductType, "level", False),
    ],
)
def test_model_structure_unique_fields(model, field_name, is_unique):
    field = model._meta.get_field(field_name)

    assert field.unique == is_unique, f"Field '{field_name}' uniqueness mismatch"
