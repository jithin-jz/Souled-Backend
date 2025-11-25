"""
Custom validators for the eCommerce application.
These validators can be reused across different serializers.
"""
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


# Phone number validator (Indian format: 10 digits)
phone_validator = RegexValidator(
    regex=r'^\d{10}$',
    message='Phone number must be exactly 10 digits.',
    code='invalid_phone'
)

# Pincode validator (Indian format: 6 digits)
pincode_validator = RegexValidator(
    regex=r'^\d{6}$',
    message='Pincode must be exactly 6 digits.',
    code='invalid_pincode'
)


def validate_positive_number(value):
    """Validate that a number is positive."""
    if value <= 0:
        raise ValidationError(
            f'{value} is not a positive number. Value must be greater than 0.',
            code='invalid_positive'
        )


def validate_stock_quantity(value):
    """Validate stock quantity is non-negative."""
    if value < 0:
        raise ValidationError(
            'Stock quantity cannot be negative.',
            code='invalid_stock'
        )


def validate_price_range(value):
    """Validate price is within reasonable range."""
    if value < 0:
        raise ValidationError(
            'Price cannot be negative.',
            code='invalid_price'
        )
    if value > 1000000:  # 10 lakh max
        raise ValidationError(
            'Price cannot exceed ₹10,00,000.',
            code='price_too_high'
        )


def validate_quantity_range(value):
    """Validate quantity is within allowed range (1-99)."""
    if value < 1:
        raise ValidationError(
            'Quantity must be at least 1.',
            code='quantity_too_low'
        )
    if value > 99:
        raise ValidationError(
            'Maximum quantity per item is 99.',
            code='quantity_too_high'
        )
