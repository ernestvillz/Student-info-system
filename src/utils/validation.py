import re


def validate_student(
    first_name: str,
    last_name: str,
    age: str,
    course: str,
    email: str,
    phone: str
) -> int:
    """Validate user input and return age as an integer."""
    if not all(value.strip() for value in
               [first_name, last_name, age, course, email, phone]):
        raise ValueError("All fields are required.")

    try:
        age_value = int(age)
    except ValueError as exc:
        raise ValueError("Age must be a whole number.") from exc

    if age_value < 15 or age_value > 100:
        raise ValueError("Age must be between 15 and 100.")

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email.strip()):
        raise ValueError("Please enter a valid email address.")

    if len(phone.strip()) < 7:
        raise ValueError("Phone number is too short.")

    return age_value
