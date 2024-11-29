import pytest  # noqa F401
from django.db import models

from inventory.models import SeasonalEvent


def test_model_structure_table_exists():
    try:
        from inventory.models import SeasonalEvent  # noqa F401
    except ImportError:
        assert False
    else:
        assert True


@pytest.mark.parametrize(
    "model, field_name, expected_type",
    [
        (SeasonalEvent, "id", models.AutoField),
        (SeasonalEvent, "start_date", models.DateTimeField),
        (SeasonalEvent, "end_date", models.DateTimeField),
        (SeasonalEvent, "name", models.CharField),
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
    "model, expected_field_count",
    [
        (
            SeasonalEvent,
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
    "model, field_name, expected_nullable",
    [
        (SeasonalEvent, "id", False),
        (SeasonalEvent, "start_date", False),
        (SeasonalEvent, "end_date", False),
        (SeasonalEvent, "name", False),
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
        (SeasonalEvent, "name", 100),
    ],
)
def test_model_structure_column_lenghts(model, field_name, expected_length):
    field = model._meta.get_field(field_name)

    assert (
        field.max_length == expected_length
    ), f"Field '{field_name}' has unexpected max lenght"


@pytest.mark.parametrize(
    "model, field_name, is_unique",
    [
        (SeasonalEvent, "id", True),
        (SeasonalEvent, "start_date", False),
        (SeasonalEvent, "end_date", False),
        (SeasonalEvent, "name", True),
    ],
)
def test_model_structure_unique_fields(model, field_name, is_unique):
    field = model._meta.get_field(field_name)

    assert field.unique == is_unique, f"Field '{field_name}' uniqueness mismatch"
