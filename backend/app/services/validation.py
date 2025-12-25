from typing import Dict, Any, List


# Required fields mapping (simplified for now)
REQUIRED_FIELDS: Dict[str, List[str]] = {
    "Cheque Book Request": [
        "customer_name",
        "account_number",
        "number_of_leaves",
        "email",
    ],
}


def validate_extracted_data(data: Dict[str, Any], form_type: str) -> Dict[str, Any]:
    required = REQUIRED_FIELDS.get(form_type, [])
    missing_fields = []

    for field in required:
        value = data.get(field, "")
        if not value or str(value).strip() == "":
            missing_fields.append(field)

    is_complete = len(missing_fields) == 0

    return {
        "is_complete": is_complete,
        "missing_fields": missing_fields,
        "status": "ready" if is_complete else "pending",
    }