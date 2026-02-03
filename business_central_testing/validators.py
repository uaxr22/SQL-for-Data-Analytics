"""
Payload validators for Business Central Customer and Vendor APIs.
Each validator returns a list of error messages (empty list means valid).
"""


# Allowed fields for customer and vendor payloads.
CUSTOMER_ALLOWED_FIELDS = {
    "number",
    "displayName",
    "email",
    "addressLine1",
    "city",
    "country",
    "postalCode",
    "phoneNumber",
}
VENDOR_ALLOWED_FIELDS = set(CUSTOMER_ALLOWED_FIELDS)

# Required fields for create requests.
CUSTOMER_REQUIRED_FIELDS = {"displayName", "email"}
VENDOR_REQUIRED_FIELDS = {"displayName", "email"}


def _is_empty(value):
    """Return True if a value is None or an empty string."""
    return value is None or (isinstance(value, str) and value.strip() == "")


def _validate_email(value, errors, field_name):
    """Basic email validation to catch obvious mistakes."""
    if not isinstance(value, str) or "@" not in value or value.startswith("@"):
        errors.append(f"{field_name} must be a valid email address")


def _validate_country(value, errors):
    """Check country code is a 2-letter ISO code."""
    if not isinstance(value, str) or len(value) != 2 or not value.isalpha():
        errors.append("country must be a 2-letter code")


def _validate_payload(payload, required_fields, allowed_fields, partial_allowed):
    """
    Validate payload shape and basic field values.
    - required_fields must exist when partial_allowed is False.
    - allowed_fields is the list of accepted keys.
    - partial_allowed lets update payloads contain only changed fields.
    """
    errors = []

    # Payload must be a dictionary.
    if not isinstance(payload, dict):
        return ["payload must be a JSON object"]

    # Update payload must not be empty.
    if partial_allowed and not payload:
        return ["payload must contain at least one field"]

    # Required field checks for create payloads.
    if not partial_allowed:
        for field in required_fields:
            if _is_empty(payload.get(field)):
                errors.append(f"missing required field: {field}")

    # Check for unexpected keys.
    for key in payload.keys():
        if key not in allowed_fields:
            errors.append(f"unexpected field: {key}")

    # Basic format validation.
    if "email" in payload and not _is_empty(payload.get("email")):
        _validate_email(payload["email"], errors, "email")
    if "country" in payload and not _is_empty(payload.get("country")):
        _validate_country(payload["country"], errors)

    return errors


def validate_customer_create(payload):
    """Validate a customer CREATE payload."""
    return _validate_payload(
        payload=payload,
        required_fields=CUSTOMER_REQUIRED_FIELDS,
        allowed_fields=CUSTOMER_ALLOWED_FIELDS,
        partial_allowed=False,
    )


def validate_customer_update(payload):
    """Validate a customer UPDATE (PATCH) payload."""
    return _validate_payload(
        payload=payload,
        required_fields=CUSTOMER_REQUIRED_FIELDS,
        allowed_fields=CUSTOMER_ALLOWED_FIELDS,
        partial_allowed=True,
    )


def validate_vendor_create(payload):
    """Validate a vendor CREATE payload."""
    return _validate_payload(
        payload=payload,
        required_fields=VENDOR_REQUIRED_FIELDS,
        allowed_fields=VENDOR_ALLOWED_FIELDS,
        partial_allowed=False,
    )


def validate_vendor_update(payload):
    """Validate a vendor UPDATE (PATCH) payload."""
    return _validate_payload(
        payload=payload,
        required_fields=VENDOR_REQUIRED_FIELDS,
        allowed_fields=VENDOR_ALLOWED_FIELDS,
        partial_allowed=True,
    )
