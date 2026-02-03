"""Tests for customer payload validation."""

from business_central_testing.validators import (
    validate_customer_create,
    validate_customer_update,
)


def test_customer_create_valid_minimal():
    # Minimal valid payload should pass with no errors.
    payload = {"displayName": "Contoso Ltd", "email": "info@contoso.com"}
    errors = validate_customer_create(payload)
    assert errors == []


def test_customer_create_missing_display_name():
    # Missing displayName should produce an error.
    payload = {"email": "info@contoso.com"}
    errors = validate_customer_create(payload)
    assert any("displayName" in error for error in errors)


def test_customer_create_invalid_email():
    # Invalid email format should produce an error.
    payload = {"displayName": "Contoso Ltd", "email": "bad-email"}
    errors = validate_customer_create(payload)
    assert any("email must be a valid email address" in error for error in errors)


def test_customer_create_invalid_country():
    # Country must be a 2-letter code.
    payload = {
        "displayName": "Contoso Ltd",
        "email": "info@contoso.com",
        "country": "USA",
    }
    errors = validate_customer_create(payload)
    assert any("country must be a 2-letter code" in error for error in errors)


def test_customer_create_unexpected_field():
    # Unexpected fields should be rejected.
    payload = {"displayName": "Contoso Ltd", "email": "info@contoso.com", "foo": "bar"}
    errors = validate_customer_create(payload)
    assert any("unexpected field: foo" in error for error in errors)


def test_customer_update_valid_partial():
    # Update payloads can be partial.
    payload = {"phoneNumber": "555-0101"}
    errors = validate_customer_update(payload)
    assert errors == []


def test_customer_update_empty_payload():
    # Empty update payload should fail.
    payload = {}
    errors = validate_customer_update(payload)
    assert any("payload must contain at least one field" in error for error in errors)


def test_customer_update_disallowed_field():
    # "id" is not an allowed update field in this validator.
    payload = {"id": "123"}
    errors = validate_customer_update(payload)
    assert any("unexpected field: id" in error for error in errors)
