# Business Central Payload Testing (Customer + Vendor)

This folder contains a simple **test plan** and **pytest automation**
to validate payloads before you call the Business Central API.

The goal is to catch bad JSON early (missing fields, invalid emails,
extra fields) before sending requests to the API.

## Quick start (run tests)

```bash
python -m pip install pytest
pytest business_central_testing/tests -v
```

## How to use in real code (example)

```python
from business_central_testing.validators import (
    validate_customer_create,
    validate_vendor_create,
)

payload = {"displayName": "Contoso Ltd", "email": "info@contoso.com"}
errors = validate_customer_create(payload)

if errors:
    raise ValueError(f"Payload invalid: {errors}")
# If no errors, call the BC API with this payload.
```

## Test plan

Each test case below is automated with pytest.

| ID | Entity | Action | What it checks | Expected result | Pytest test |
|---|---|---|---|---|---|
| CUST-CREATE-001 | Customer | Create | Minimal valid payload | Pass | `test_customer_create_valid_minimal` |
| CUST-CREATE-002 | Customer | Create | Missing displayName | Fail | `test_customer_create_missing_display_name` |
| CUST-CREATE-003 | Customer | Create | Invalid email | Fail | `test_customer_create_invalid_email` |
| CUST-CREATE-004 | Customer | Create | Invalid country code | Fail | `test_customer_create_invalid_country` |
| CUST-CREATE-005 | Customer | Create | Extra unexpected field | Fail | `test_customer_create_unexpected_field` |
| CUST-UPDATE-001 | Customer | Update | Valid partial update | Pass | `test_customer_update_valid_partial` |
| CUST-UPDATE-002 | Customer | Update | Empty payload | Fail | `test_customer_update_empty_payload` |
| CUST-UPDATE-003 | Customer | Update | Disallowed field `id` | Fail | `test_customer_update_disallowed_field` |
| VEND-CREATE-001 | Vendor | Create | Minimal valid payload | Pass | `test_vendor_create_valid_minimal` |
| VEND-CREATE-002 | Vendor | Create | Missing email | Fail | `test_vendor_create_missing_email` |
| VEND-CREATE-003 | Vendor | Create | Invalid email | Fail | `test_vendor_create_invalid_email` |
| VEND-CREATE-004 | Vendor | Create | Invalid country code | Fail | `test_vendor_create_invalid_country` |
| VEND-UPDATE-001 | Vendor | Update | Valid partial update | Pass | `test_vendor_update_valid_partial` |
| VEND-UPDATE-002 | Vendor | Update | Empty payload | Fail | `test_vendor_update_empty_payload` |
| VEND-UPDATE-003 | Vendor | Update | Disallowed field `@odata.etag` | Fail | `test_vendor_update_disallowed_field` |

## Step-by-step usage in a real project

1. **Decide your payload rules**
   - Update `validators.py` if you want to require more fields or add
     stricter checks.
2. **Validate before calling the API**
   - Call `validate_customer_create(payload)` or
     `validate_vendor_create(payload)` in your integration code.
3. **Stop if invalid**
   - If the validator returns errors, do not call the API.
4. **Run tests in CI**
   - Add this to your pipeline:
     ```
     pytest business_central_testing/tests -v
     ```
5. **Extend tests when new fields are added**
   - Add new test cases to keep payload rules in sync.
