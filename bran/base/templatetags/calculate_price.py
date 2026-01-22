from django import template

register = template.Library()


@register.filter
def calculate_price(distance, price_per_mile):
    return round(distance * price_per_mile, 2)


@register.filter
def calculate_price_with_vat(distance, price_per_mile):
    net_price = distance * price_per_mile
    vat_price = net_price * 1.20
    return round(vat_price, 2)
