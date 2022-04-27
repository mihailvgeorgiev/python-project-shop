from django.core.exceptions import ValidationError


def only_letters_validator(value):
    invalid_chars = [ch for ch in value if not ch.isalpha()]
    if invalid_chars:
        raise ValidationError(f"Field must contain only letters, but contains: {invalid_chars}")


def only_numbers(value):
    for number in value:
        if not number.isdigit():
            raise ValidationError('Phone number contains characters')
