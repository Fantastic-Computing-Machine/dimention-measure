from django import template
from decimal import Decimal
register = template.Library()


# @register.simple_tag()
# def meter_to_feet(meter, *args, **kwargs):
#     return Decimal(meter * 3.28084)


@register.simple_tag()
def meter_to_feet(meter, *args, **kwargs):
    return "{:.2f}".format(Decimal(float(meter) * 3.28084))


@register.simple_tag()
def feet_to_meter(feet, *args, **kwargs):
    return "{:.2f}".format(Decimal(float(feet) * 0.3048))
