"""Tests for vendor payload validation."""

from business_central_testing.validators import (
    validate_vendor_create,
    validate_vendor_update,
)


def test_vendor_create_valid_minimal():
    # Minimal valid payload should pass with no errors.
    payload = {"displayName": "Fabrikam Co", "email": "contact@fabrikam.com"}
    errors = validate_vendor_create(payload)
    assert errors == []


def test_vendor_create_missing_email():
    # Missing email should produce an error.
    payload = {"displayName": "Fabrikam Co"}
    errors = validate_vendor_create(payload)
    assert any("email" in error for error in errors)


def test_vendor_create_invalid_email():
    # Invalid email format should produce an error.
    payload = {"displayName": "Fabrikam Co", "email": "bad-email"}
    errors = validate_vendor_create(payload)
    assert any("email must be a valid email address" in error for error in errors)


def test_vendor_create_invalid_country():
    # Country must be a 2-letter code.
    payload = {
        "displayName": "Fabrikam Co",
        "email": "contact@fabrikam.com",
        "country": "USA",
    }
    errors = validate_vendor_create(payload)
    assert any("country must be a 2-letter code" in error for error in errors)


def test_vendor_update_valid_partial():
    # Update payloads can be partial.
    payload = {"addressLine1": "1 Vendor St"}
    errors = validate_vendor_update(payload)
    assert errors == []


def test_vendor_update_empty_payload():
    # Empty update payload should fail.
    payload = {}
    errors = validate_vendor_update(payload)
    assert any("payload must contain at least one field" in error for error in errors)


def test_vendor_update_disallowed_field():
    # "@odata.etag" is not allowed by this validator.
    payload = {"@odata.etag": "W/\"123\""}
    errors = validate_vendor_update(payload)
    assert any("unexpected field: @odata.etag" in error for error in errors)
