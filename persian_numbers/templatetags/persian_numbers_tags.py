from django import template

register = template.Library()

def int_to_comma(number):
    try:
        number = int(number)
        return f"{number:,}"
    except (ValueError, TypeError):
        return number

def to_persian_digits(number_str):
    persian_digits = "۰۱۲۳۴۵۶۷۸۹"
    return ''.join(persian_digits[int(ch)] if ch.isdigit() else ch for ch in str(number_str))

@register.filter
def persian_number(value):
    value_with_comma = int_to_comma(value)
    return to_persian_digits(value_with_comma)
