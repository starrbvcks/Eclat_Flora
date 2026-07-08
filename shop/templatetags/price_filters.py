from django import template

from shop.price_utils import format_price_value


register = template.Library()


@register.filter
def format_price(value):
    return format_price_value(value)
