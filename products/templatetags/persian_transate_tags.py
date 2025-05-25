from  django import template

register = template.Library()

@register.filter
def persian_number_translate(value):
    value = str(value)
    english_to_persian_table=value.maketrans('1234567890','۱۲۳۴۵۶۷۸۹۰')
    return value.translate(english_to_persian_table)

