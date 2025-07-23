def validate_user_input(data, required_fields=None):
    """
    Validates that all required fields are present and non-empty in the data dictionary.
    Returns a tuple: (True, None) if valid, or (False, error_message).
    """
    if not isinstance(data, dict):
        return False, "Input data must be a JSON object"

    required_fields = required_fields or []

    for field in required_fields:
        value = data.get(field)
        if value is None or str(value).strip() == "":
            return False, f"Missing or empty field: {field}"

    return True, None
