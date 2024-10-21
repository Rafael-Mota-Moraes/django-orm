import pytest
from django.db import models

from inventory.models import (
    AttributeValue,
    Product,
    ProductLine,
    ProductLine_AttributeValue,
)


def test_model_structure_table_exists():
    try:
        from inventory.models import ProductLine  # noqa F401
    except ImportError:
        assert False
    else:
        assert True


@pytest.mark.parametrize(
    "model, field_name, expected_type",
    [
        (ProductLine, "id", models.AutoField),
        (ProductLine, "price", models.DecimalField),
        (ProductLine, "sku", models.UUIDField),
        (ProductLine, "stock_qty", models.IntegerField),
        (ProductLine, "is_active", models.BooleanField),
        (ProductLine, "order", models.IntegerField),
        (ProductLine, "weight", models.FloatField),
        (ProductLine, "product", models.ForeignKey),
        (ProductLine, "attribute_values", models.ManyToManyField),
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
            ProductLine,
            "product",
            models.ForeignKey,
            Product,
            models.PROTECT,
            False,
            False,
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
            ProductLine,
            "attribute_values",
            models.ManyToManyField,
            AttributeValue,
            ProductLine_AttributeValue,
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
        (ProductLine, "id", False),
        (ProductLine, "price", False),
        (ProductLine, "sku", False),
        (ProductLine, "stock_qty", False),
        (ProductLine, "is_active", False),
        (ProductLine, "order", False),
        (ProductLine, "weight", False),
        (ProductLine, "product", False),
        (ProductLine, "attribute_values", False),
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
        (ProductLine, "is_active", False),
        (ProductLine, "stock_qty", 0),
    ],
)
def test_model_structure_default_values(model, field_name, expected_default_value):
    field = model._meta.get_field(field_name)
    default_value = field.default

    assert default_value == expected_default_value


@pytest.mark.parametrize(
    "model, field_name, expected_max_digits, expected_decimal_places",
    [
        (ProductLine, "price", 5, 2),
    ],
)
def test_model_structure_decimal_field(
    model, field_name, expected_max_digits, expected_decimal_places
):
    field = model._meta.get_field(field_name)

    assert (
        field.max_digits == expected_max_digits
    ), f"Field '{field_name}' has unexpected max_digits. Expected {expected_max_digits} got {field.max_digits}"

    assert (
        field.decimal_places == expected_decimal_places
    ), f"Field '{field_name}' has unexpected decimal_places. Expected {expected_decimal_places}, got {field.decimal_places}"


@pytest.mark.parametrize(
    "model, expected_field_count",
    [
        (
            ProductLine,
            8,
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
        (ProductLine, "id", True),
        (ProductLine, "price", False),
        (ProductLine, "sku", True),
        (ProductLine, "stock_qty", False),
        (ProductLine, "is_active", False),
        (ProductLine, "order", False),
        (ProductLine, "weight", False),
        (ProductLine, "product", False),
        (ProductLine, "attribute_values", False),
    ],
)
def test_model_structure_unique_fields(model, field_name, is_unique):
    field = model._meta.get_field(field_name)

    assert field.unique == is_unique, f"Field '{field_name}' uniqueness mismatch"
