import pytest
from django.db import models

from inventory.models import (
    Category,
    Product,
    Product_ProductType,
    ProductType,
    SeasonalEvent,
)


def test_model_structure_table_exists():
    try:
        from inventory.models import Product  # noqa F401
    except ImportError:
        assert False
    else:
        assert True


@pytest.mark.parametrize(
    "model, field_name, expected_type",
    [
        (Product, "id", models.AutoField),
        (Product, "pid", models.CharField),
        (Product, "name", models.CharField),
        (Product, "slug", models.SlugField),
        (Product, "description", models.TextField),
        (Product, "is_digitial", models.BooleanField),
        (Product, "created_at", models.DateTimeField),
        (Product, "updated_at", models.DateTimeField),
        (Product, "is_active", models.BooleanField),
        (Product, "stock_status", models.CharField),
        # (Product, "category", models.ForeignKey),
        # (Product, "seasonal_event", models.ForeignKey),
        # (Product, "product_type", models.ManyToManyField),
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
        (Product, "category", models.ForeignKey, Category, models.SET_NULL, True, True),
        (
            Product,
            "seasonal_event",
            models.ForeignKey,
            SeasonalEvent,
            models.SET_NULL,
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
    "model, field_name, expected_type, related_model, through, through_fields, allow_blank",
    [
        (
            Product,
            "product_type",
            models.ManyToManyField,
            ProductType,
            Product_ProductType,
            None,
            False,
        ),
    ],
)
def test_model_structure_many_to_many(
    model,
    field_name,
    expected_type,
    related_model,
    through,
    through_fields,
    allow_blank,
):
    assert hasattr(
        model, field_name
    ), f"{model.__name__} models does not have '{field_name}' field"

    field = model._meta.get_field(field_name)
    assert isinstance(field, expected_type), f"Field is not type {expected_type}"

    assert (
        field.related_model == related_model
    ), f"'{field_name}' field does not relate to {related_model.__name__} model."

    if through is not None:
        assert (
            field.remote_field.through == through
        ), f"'{field_name}' field does not use the expected through model"

    assert (
        field.blank == allow_blank
    ), f"'{field_name}' field does not allow blank values as expected."


@pytest.mark.parametrize(
    "model, field_name, expected_nullable",
    [
        (Product, "id", False),
        (Product, "pid", False),
        (Product, "name", False),
        (Product, "slug", False),
        (Product, "description", True),
        (Product, "is_digitial", False),
        (Product, "created_at", False),
        (Product, "updated_at", False),
        (Product, "is_active", False),
        (Product, "stock_status", False),
    ],
)
def test_model_structure_nullable_constraints(model, field_name, expected_nullable):
    field = model._meta.get_field(field_name)

    assert (
        field.null is expected_nullable
    ), f"Field '{field_name}' has unexpected nullable constraint"


@pytest.mark.parametrize(
    "model, field_name, expected_default_value",
    [
        (Product, "is_digitial", False),
        (Product, "is_active", False),
        (Product, "stock_status", "OOS"),
    ],
)
def test_model_structure_default_values(model, field_name, expected_default_value):
    field = model._meta.get_field(field_name)
    default_value = field.default

    assert default_value == expected_default_value


@pytest.mark.parametrize(
    "model, field_name, expected_length",
    [
        (Product, "pid", 255),
        (Product, "name", 200),
        (Product, "slug", 220),
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
            Product,
            12,
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
        (Product, "id", True),
        (Product, "pid", True),
        (Product, "name", True),
        (Product, "slug", True),
        (Product, "description", False),
        (Product, "is_digitial", False),
        (Product, "created_at", False),
        (Product, "updated_at", False),
        (Product, "is_active", False),
        (Product, "stock_status", False),
    ],
)
def test_model_structure_unique_fields(model, field_name, is_unique):
    field = model._meta.get_field(field_name)

    assert field.unique == is_unique, f"Field '{field_name}' uniqueness mismatch"
